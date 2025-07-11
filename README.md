# Resumidor de Textos Multilingüe con Voz

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Ollama](https://img.shields.io/badge/Powered%20by-Ollama-FFD43B.svg)
![Gemma](https://img.shields.io/badge/Model-Gemma%203%204B%20QAT-7950F3.svg)

Una potente aplicación web que transforma textos extensos en resúmenes concisos y los convierte a voz natural en 4 idiomas: español, inglés, francés e italiano. Ideal para estudiantes, investigadores o cualquiera que necesite procesar información rápidamente. La aplicación puede extraer contenido directamente de URLs o procesar texto ingresado manualmente, ofreciendo una experiencia de aprendizaje auditivo en el idioma de tu preferencia.

## Características

- **Resumen de textos** en múltiples idiomas (español, inglés, francés e italiano)
- **Conversión de texto a voz** en el mismo idioma del resumen
- **Soporte para 4 idiomas** en la generación de voz:
  - Español (voz natural)
  - Inglés (voz natural)
  - Francés (voz natural)
  - Italiano (voz natural)
- **Múltiples formatos de entrada**:
  - Texto directo
  - Extracción de contenido desde URL
- Interfaz web intuitiva y fácil de usar
- Reproducción de audio directamente en el navegador
- Control de reproducción para pausar, reanudar o detener la reproducción

## Requisitos

- Python 3.7 o superior
- [Ollama](https://ollama.ai/) instalado y en ejecución
- Modelo Gemma 3 4B QAT descargado (se descargará automáticamente la primera vez que se use)
- Conexión a Internet (para la descarga inicial del modelo y ciertas funcionalidades)
- Navegador web moderno

## Modelo de Lenguaje

Esta aplicación utiliza **Gemma 3 4B IT QAT** (Quantization-Aware Training) a través de Ollama, lo que permite:

- **Alta calidad** en la generación de resúmenes
- **Eficiencia** gracias a la cuantización que optimiza el rendimiento
- **Funcionamiento local** para mayor privacidad de los datos
- **Soporte multilingüe** con excelentes resultados en español, inglés, francés e italiano

Para usar la aplicación, asegúrate de tener Ollama instalado y en ejecución. El modelo se descargará automáticamente la primera vez que lo uses.

### Instalación de Ollama

1. Descarga e instala Ollama desde [https://ollama.ai/](https://ollama.ai/)
2. Inicia el servicio de Ollama
3. La primera vez que ejecutes la aplicación, descargará automáticamente el modelo `gemma3:4b-it-qat`

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

## Estructura del Proyecto

- `app.py` - Aplicación principal de Flask
- `arrancar.bat` - Lanzador automático para Windows (configura el entorno y abre el navegador)
- `templates/` - Plantillas HTML
- `static/` - Archivos estáticos (CSS, JS, audios)
- `requirements.txt` - Dependencias del proyecto
- `arrancar.bat` - Lanzador para Windows que asegura que Ollama esté en ejecución

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, lee nuestras pautas de contribución antes de enviar pull requests.

## Contacto

Si tienes preguntas o sugerencias, no dudes en abrir un issue en el repositorio.
