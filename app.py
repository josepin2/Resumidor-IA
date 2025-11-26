# app.py
import flask
import ollama
import requests
from bs4 import BeautifulSoup
import re
import asyncio
import edge_tts
import io
import os
from gtts import gTTS
import json
import tempfile
from werkzeug.utils import secure_filename
try:
    from mutagen.mp3 import MP3
    HAS_MUTAGEN = True
except Exception:
    HAS_MUTAGEN = False
try:
    from faster_whisper import WhisperModel
    HAS_ASR = True
except Exception:
    HAS_ASR = False

app = flask.Flask(__name__)

# --- CONFIGURACIÓN ---
MODELO_OLLAMA = "gemma3:12b-it-qat"
VOICE_MAP = {
    "Spanish": "es-ES-ElviraNeural",
    "English": "en-US-AriaNeural",
    "French":  "fr-FR-DeniseNeural",
    "Italian": "it-IT-ElsaNeural",
    "Portuguese": "pt-BR-FranciscaNeural",
    "German": "de-DE-KatjaNeural",
    "Japanese": "ja-JP-NanamiNeural",
    "Chinese": "zh-CN-XiaoxiaoNeural"
}
DEFAULT_VOICE = VOICE_MAP["Spanish"]
ASR_MODEL = None
ASR_MODEL_SIZE = os.getenv('ASR_MODEL_SIZE', 'small')


# --- Funciones de la App ---
def es_url(texto):
    regex = re.compile(
        r'^(?:http|ftp)s?://' 
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, texto) is not None

def extraer_texto_de_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
        texto = soup.get_text()
        lineas = (line.strip() for line in texto.splitlines())
        chunks = (phrase.strip() for line in lineas for phrase in line.split("  "))
        texto_limpio = '\n'.join(chunk for chunk in chunks if chunk)
        return texto_limpio
    except Exception as e:
        print(f"Error al acceder a la URL: {e}")
        return f"Error al acceder a la URL: {e}"

def generar_resumen_con_ollama(texto_a_resumir, idioma_destino):
    if not texto_a_resumir.strip():
        return "El texto proporcionado estaba vacío.", []
    prompt = (
        f"Traduce el texto a {idioma_destino}. Luego, escribe el resumen en tono neutral e impersonal (sin primera persona ni referencias en tercera persona), claro y directo, sin comillas ni markdown. "
        f"Genera exactamente 5 puntos clave. "
        f"Responde SOLO en JSON con esta forma exacta (en {idioma_destino}): {{\"summary\": \"...\", \"key_points\": [\"...\", \"...\", \"...\", \"...\", \"...\"]}}. "
        f"No añadas nada fuera del JSON.\n\n--- TEXTO ---\n{texto_a_resumir}\n--- FIN ---"
    )

    def _clean_text(s):
        s = (s or "").strip()
        if s.startswith('```'):
            s = re.sub(r"^```[a-zA-Z]*\n?", "", s)
            s = re.sub(r"\n?```$", "", s)
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1].strip()
        return s
    try:
        response = ollama.chat(model=MODELO_OLLAMA, messages=[{'role': 'user', 'content': prompt}])
        content = response.get('message', {}).get('content', '')
        s = (content or '').strip()
        if s.startswith('```'):
            m = re.search(r"\{[\s\S]*\}", s)
            if m:
                s = m.group(0)
        try:
            data = json.loads(s)
            summary = _clean_text(data.get('summary') or data.get('resumen') or '')
            key_points = data.get('key_points') or data.get('puntos_clave') or data.get('puntos') or []
            if isinstance(key_points, str):
                key_points = [kp.strip() for kp in re.split(r"[\n;•\-]+", key_points) if kp.strip()]
            key_points = [_clean_text(kp) for kp in key_points if isinstance(kp, str) and kp.strip()]
            if len(key_points) > 5:
                key_points = key_points[:5]
            return summary or s, key_points
        except Exception:
            return content, []
    except Exception as e:
        return f"Error conectando con Ollama: {e}", []

def map_lang_to_whisper(lang):
    m = {
        "Spanish": "es",
        "English": "en",
        "French": "fr",
        "Italian": "it",
        "Portuguese": "pt",
        "German": "de",
        "Japanese": "ja",
        "Chinese": "zh"
    }
    return m.get(lang, "es")

def get_asr_model():
    global ASR_MODEL
    if ASR_MODEL is None and HAS_ASR:
        ASR_MODEL = WhisperModel(ASR_MODEL_SIZE, device="cpu", compute_type="int8")
    return ASR_MODEL

# --- Rutas de Flask ---

@app.route('/', methods=['GET', 'POST'])
def index():
    # Inicializamos las variables fuera del bloque if
    resumen = ""
    puntos_clave = []
    texto_original = ""
    idioma_seleccionado = "Spanish"  # Valor por defecto

    if flask.request.method == 'POST':
        # SOLO intentamos leer los datos del formulario si es un POST
        texto_original = flask.request.form.get('texto', '') # Usamos .get() para evitar errores si no existe
        idioma_seleccionado = flask.request.form.get('language', 'Spanish')
        
        # Procesamos el texto solo si el usuario ha escrito algo
        if texto_original.strip():
            if es_url(texto_original):
                print(f"Detectada URL: {texto_original}")
                texto_a_resumir = extraer_texto_de_url(texto_original)
            else:
                print("Detectado texto plano.")
                texto_a_resumir = texto_original
            
            resumen, puntos_clave = generar_resumen_con_ollama(texto_a_resumir, idioma_seleccionado)
        else:
            # Opcional: podrías mostrar un mensaje de error si el texto está vacío
            print("El formulario se envió con el campo de texto vacío.")

    # Siempre renderizamos el template, con las variables vacías o con los resultados
    return flask.render_template('index.html', 
                                 texto_original=texto_original, 
                                 resumen=resumen, 
                                 puntos_clave=puntos_clave,
                                 idioma_seleccionado=idioma_seleccionado)

@app.route('/transcribe_audio', methods=['POST'])
def transcribe_audio():
    if not HAS_ASR:
        return flask.jsonify({"error": "ASR no disponible. Instala faster-whisper y ffmpeg."}), 500
    f = flask.request.files.get('audio')
    if not f:
        return flask.jsonify({"error": "Archivo no proporcionado"}), 400
    filename = secure_filename(f.filename or "")
    if not filename.lower().endswith('.mp3'):
        return flask.jsonify({"error": "Formato no soportado. Solo MP3."}), 400
    fd, tmp_path = tempfile.mkstemp(suffix='.mp3')
    os.close(fd)
    try:
        f.save(tmp_path)
        if not HAS_MUTAGEN:
            return flask.jsonify({"error": "Validación de duración requiere 'mutagen'. Ejecuta pip install -r requirements.txt"}), 500
        audio = MP3(tmp_path)
        duration = getattr(audio.info, 'length', 0)
        if duration and duration > 300:
            return flask.jsonify({"error": "Duración máxima 5 minutos"}), 400
        lang = flask.request.form.get('language', 'Spanish')
        lang_code = map_lang_to_whisper(lang)
        model = get_asr_model()
        if model is None:
            return flask.jsonify({"error": "No se pudo inicializar el modelo ASR"}), 500
        segments, info = model.transcribe(tmp_path, language=lang_code)
        text = " ".join([s.text.strip() for s in segments])
        return flask.jsonify({"transcription": text})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500
    finally:
        try:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass


async def generate_audio_for(text, lang, voice_id=None):
    voice_id = voice_id or VOICE_MAP.get(lang, DEFAULT_VOICE)
    communicate = edge_tts.Communicate(text, voice_id)
    audio_buffer = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_buffer += chunk["data"]
    return audio_buffer, voice_id
 
def generate_audio_with_azure(text, lang, voice_id=None):
    """
    Genera audio usando Azure Speech si las credenciales están presentes.
    Devuelve (audio_buffer, voice_id) o None si no hay credenciales.
    """
    key = os.getenv('AZURE_SPEECH_KEY')
    region = os.getenv('AZURE_SPEECH_REGION')
    if not key or not region:
        return None

def map_lang_to_gtts(lang):
    mapping = {
        "Spanish": "es",
        "English": "en",
        "French": "fr",
        "Italian": "it",
        "Portuguese": "pt",
        "German": "de",
        "Japanese": "ja",
        "Chinese": "zh-CN",
    }
    return mapping.get(lang, "es")

def generate_audio_with_gtts(text, lang):
    """
    Genera audio usando gTTS (Google TTS) sin necesidad de credenciales.
    Devuelve (audio_buffer, voice_id) o None si falla.
    """
    try:
        tts_lang = map_lang_to_gtts(lang)
        tts = gTTS(text=text, lang=tts_lang)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        audio_buffer = buf.getvalue()
        # voice_id sintético para identificar el proveedor
        voice_id = f"gtts-{tts_lang}"
        print(f"Audio gTTS generado para idioma '{lang}' ({tts_lang})")
        return audio_buffer, voice_id
    except Exception as e:
        print(f"Error generando audio con gTTS: {e}")
        return None
    voice_id = voice_id or VOICE_MAP.get(lang, DEFAULT_VOICE)
    # Derivar el locale (p.ej., es-ES) a partir del nombre de la voz
    try:
        locale = "-".join(voice_id.split('-')[:2])
    except Exception:
        locale = 'es-ES'
    url = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'audio-24khz-48kbitrate-mono-mp3'
    }
    ssml = f"""
    <speak version='1.0' xml:lang='{locale}'>
        <voice xml:lang='{locale}' name='{voice_id}'>
            {text}
        </voice>
    </speak>
    """.strip()
    try:
        resp = requests.post(url, headers=headers, data=ssml.encode('utf-8'), timeout=20)
        resp.raise_for_status()
        print(f"Audio Azure generado con la voz '{voice_id}'")
        return resp.content, voice_id
    except Exception as e:
        print(f"Error generando audio con Azure Speech: {e}")
        return None

@app.route('/speak')
def speak():
    text = flask.request.args.get('text', 'No se proporcionó texto.')
    lang = flask.request.args.get('lang', 'Spanish')
    voice_override = flask.request.args.get('voice')
    if not text:
        return "Texto vacío", 400

    try:
        # 1) Intentar Azure si hay credenciales
        azure_result = generate_audio_with_azure(text, lang, voice_override)
        if azure_result:
            audio_buffer, voice_id = azure_result
            resp = flask.Response(audio_buffer, mimetype='audio/mpeg')
            resp.headers['X-TTS-Provider'] = 'Azure'
            resp.headers['X-Voice-Id'] = voice_id
            return resp
        # 2) Fallback: Edge TTS
        audio_buffer, voice_id = asyncio.run(generate_audio_for(text, lang, voice_override))
        print(f"Audio para streaming (Edge TTS) generado con la voz '{voice_id}'")
        resp = flask.Response(audio_buffer, mimetype='audio/mpeg')
        resp.headers['X-TTS-Provider'] = 'Edge'
        resp.headers['X-Voice-Id'] = voice_id
        return resp
    except Exception as e:
        print(f"Error durante la generación de voz con edge-tts: {e}")
        return "Error generando audio", 500

@app.route('/download_audio')
def download_audio():
    text = flask.request.args.get('text', 'No se proporcionó texto.')
    lang = flask.request.args.get('lang', 'Spanish')
    voice_override = flask.request.args.get('voice')
    if not text:
        return "Texto vacío", 400

    try:
        # 1) Intentar Azure si hay credenciales
        azure_result = generate_audio_with_azure(text, lang, voice_override)
        provider = None
        if azure_result:
            audio_buffer, voice_id = azure_result
            provider = 'Azure'
            print(f"Audio para descarga (Azure) generado con la voz '{voice_id}'")
        else:
            # 2) Intentar Edge TTS; si falla, hacer fallback a gTTS
            try:
                audio_buffer, voice_id = asyncio.run(generate_audio_for(text, lang, voice_override))
                provider = 'Edge'
                print(f"Audio para descarga (Edge TTS) generado con la voz '{voice_id}'")
            except Exception as edge_err:
                print(f"Edge TTS falló, intentando gTTS como fallback: {edge_err}")
                gtts_result = generate_audio_with_gtts(text, lang)
                if not gtts_result:
                    raise edge_err
                audio_buffer, voice_id = gtts_result
                provider = 'gTTS'
                print(f"Audio para descarga (gTTS) generado para idioma '{lang}'")

        audio_stream = io.BytesIO(audio_buffer)
        response = flask.send_file(
            audio_stream,
            as_attachment=True,
            download_name='resumen.mp3',
            mimetype='audio/mpeg'
        )
        if provider:
            response.headers['X-TTS-Provider'] = provider
            response.headers['X-Voice-Id'] = voice_id
        return response
    except Exception as e:
        print(f"Error durante la generación de voz (descarga): {e}")
        return "Error generando audio", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
