# app.py
import flask
import ollama
import requests
from bs4 import BeautifulSoup
import re
import asyncio
import edge_tts
import io

app = flask.Flask(__name__)

# --- CONFIGURACIÓN ---
MODELO_OLLAMA = "gemma3:4b-it-qat"
VOICE_MAP = {
    "Spanish": "es-ES-ElviraNeural",
    "English": "en-US-AriaNeural",
    "French":  "fr-FR-DeniseNeural",
    "Italian": "it-IT-ElsaNeural"
}
DEFAULT_VOICE = VOICE_MAP["Spanish"]


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
        return "El texto proporcionado estaba vacío."
    
    prompt = (
        f"IMPORTANT: First, translate the following text into {idioma_destino}. "
        f"Then, summarize the translated text in a single, concise paragraph, also in {idioma_destino}. "
        f"Provide ONLY the final summary in {idioma_destino}."
        f"\n\n--- TEXT TO PROCESS ---\n{texto_a_resumir}\n--- END OF TEXT ---"
    )

    try:
        print(f"Generando resumen en {idioma_destino}...")
        response = ollama.chat(model=MODELO_OLLAMA, messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content']
    except Exception as e:
        print(f"Error conectando con Ollama: {e}")
        return f"Error conectando con Ollama: {e}"

# --- Rutas de Flask ---

@app.route('/', methods=['GET', 'POST'])
def index():
    # Inicializamos las variables fuera del bloque if
    resumen = ""
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
            
            resumen = generar_resumen_con_ollama(texto_a_resumir, idioma_seleccionado)
        else:
            # Opcional: podrías mostrar un mensaje de error si el texto está vacío
            print("El formulario se envió con el campo de texto vacío.")

    # Siempre renderizamos el template, con las variables vacías o con los resultados
    return flask.render_template('index.html', 
                                 texto_original=texto_original, 
                                 resumen=resumen, 
                                 idioma_seleccionado=idioma_seleccionado)


async def generate_audio_for(text, lang):
    voice_id = VOICE_MAP.get(lang, DEFAULT_VOICE)
    communicate = edge_tts.Communicate(text, voice_id)
    audio_buffer = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_buffer += chunk["data"]
    return audio_buffer, voice_id

@app.route('/speak')
async def speak():
    text = flask.request.args.get('text', 'No se proporcionó texto.')
    lang = flask.request.args.get('lang', 'Spanish')
    if not text:
        return "Texto vacío", 400
    
    try:
        audio_buffer, voice_id = await generate_audio_for(text, lang)
        print(f"Audio para streaming generado con la voz '{voice_id}'")
        return flask.Response(audio_buffer, mimetype='audio/mpeg')
    except Exception as e:
        print(f"Error durante la generación de voz con edge-tts: {e}")
        return "Error generando audio", 500

@app.route('/download_audio')
async def download_audio():
    text = flask.request.args.get('text', 'No se proporcionó texto.')
    lang = flask.request.args.get('lang', 'Spanish')
    if not text:
        return "Texto vacío", 400

    try:
        audio_buffer, voice_id = await generate_audio_for(text, lang)
        print(f"Audio para descarga generado con la voz '{voice_id}'")
        
        audio_stream = io.BytesIO(audio_buffer)

        return flask.send_file(
            audio_stream,
            as_attachment=True,
            download_name='resumen.mp3',
            mimetype='audio/mpeg'
        )
    except Exception as e:
        print(f"Error durante la generación de voz con edge-tts para descarga: {e}")
        return "Error generando audio", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)