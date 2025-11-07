# Resumidor de Textos Multilingüe con Voz

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Ollama](https://img.shields.io/badge/Powered%20by-Ollama-FFD43B.svg)
![Gemma](https://img.shields.io/badge/Model-Gemma%203%2012B%20IT%20QAT-7950F3.svg)

Aplicación web que transforma textos extensos en resúmenes concisos y los convierte a voz natural en múltiples idiomas. Ideal para estudiantes, investigadores o cualquiera que necesite procesar información rápidamente. La aplicación puede extraer contenido directamente de URLs o procesar texto ingresado manualmente, ofreciendo una experiencia auditiva en el idioma de tu preferencia.

## Características

- **Resumen de textos** en el idioma que elijas
- **Conversión de texto a voz** integrada
- **Soporte de voz en 8 idiomas**:
  - Español, Inglés, Francés, Italiano
  - Portugués, Alemán, Japonés, Chino
- **Múltiples formatos de entrada**:
  - Texto directo
  - Extracción de contenido desde URL
- Interfaz web intuitiva y fácil de usar
- Reproducción y descarga de audio directamente desde el navegador
- Selección de voz (Edge TTS) cuando esté disponible

## Requisitos

- Python 3.8 o superior (requerido por Flask 3)
- [Ollama](https://ollama.ai/) instalado y en ejecución
- Modelo Gemma 3 12B IT QAT (se descargará automáticamente la primera vez que se use)
- Conexión a Internet (para la descarga inicial del modelo y ciertas funcionalidades)
- Navegador web moderno

## Modelo de Lenguaje

Esta aplicación utiliza **Gemma 3 12B IT QAT** (Quantization-Aware Training) a través de Ollama, lo que permite:

- **Alta calidad** en la generación de resúmenes
- **Eficiencia** gracias a la cuantización que optimiza el rendimiento
- **Funcionamiento local** para mayor privacidad de los datos
- **Soporte multilingüe** con excelentes resultados en español, inglés, francés, italiano, portugués, alemán, japonés y chino

Para usar la aplicación, asegúrate de tener Ollama instalado y en ejecución. El modelo se descargará automáticamente la primera vez que lo uses.

### Instalación de Ollama

1. Descarga e instala Ollama desde [https://ollama.ai/](https://ollama.ai/)
2. Inicia el servicio de Ollama
3. La primera vez que ejecutes la aplicación, descargará automáticamente el modelo `gemma3:12b-it-qat`

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/josepin2/Resumidor-IA.git
   cd Resumidor-IA
   ```

2. Crea un entorno virtual (recomendado):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # En Windows
   # O en Linux/Mac: source venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

### Opción 1: Usando el lanzador de Windows (recomendado para usuarios de Windows)

1. Simplemente haz doble clic en el archivo `arrancar.bat`
2. El script hará lo siguiente automáticamente:
   - Verificará el entorno virtual
   - Lo activará si es necesario
   - Abrirá tu navegador predeterminado en la dirección correcta
   - Iniciará el servidor Flask

### Opción 2: Método manual

1. Inicia la aplicación manualmente:
   ```bash
   python app.py
   ```

2. Abre tu navegador y ve a:
```
http://localhost:5001
```

### Para todos los métodos:
- Selecciona el idioma deseado
- Ingresa tu texto o URL
- Haz clic en "Resumir"
- Escucha el audio del resumen usando los controles de reproducción

### Proveedores de voz (TTS)
- Si existen las variables de entorno `AZURE_SPEECH_KEY` y `AZURE_SPEECH_REGION`, el audio se generará con **Azure Speech**.
- En caso contrario, la reproducción en el navegador usa **Edge TTS**.
- Para la descarga de audio, si Edge TTS no está disponible, se usa **gTTS** como fallback.

Variables de entorno opcionales:
- `AZURE_SPEECH_KEY`: clave de Azure Speech
- `AZURE_SPEECH_REGION`: región de Azure (por ejemplo, `eastus`)

## Estructura del Proyecto

- `app.py` - Aplicación principal de Flask y endpoints (`/`, `/speak`, `/download_audio`)
- `arrancar.bat` - Lanzador automático para Windows (configura el entorno y abre el navegador)
- `templates/` - Plantillas HTML (UI con selección de idioma y voz)
- `static/` - Archivos estáticos
- `requirements.txt` - Dependencias del proyecto

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, lee nuestras pautas de contribución antes de enviar pull requests.

## Contacto

Si tienes preguntas o sugerencias, no dudes en abrir un issue en el repositorio.
