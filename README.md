# Resumidor de Textos con Conversión a Audio

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Una aplicación web que permite resumir textos y convertirlos a audio en diferentes idiomas (español, inglés, francés e italiano). La aplicación puede procesar tanto texto directo como extraer contenido de URLs.

## Características

- Resumen de textos en múltiples idiomas
- Conversión de texto a voz
- Soporte para entrada de texto directo o desde URL
- Interfaz web intuitiva
- Fácil de usar y configurar

## Requisitos

- Python 3.7 o superior
- Conexión a Internet (para ciertas funcionalidades)
- Navegador web moderno

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

1. Inicia la aplicación:
   ```bash
   python app.py
   ```

2. Abre tu navegador y ve a:
   ```
   http://localhost:5000
   ```

3. Selecciona el idioma, ingresa tu texto o URL y haz clic en "Resumir".

## Estructura del Proyecto

- `app.py` - Aplicación principal de Flask
- `templates/` - Plantillas HTML
- `static/` - Archivos estáticos (CSS, JS, audios)
- `requirements.txt` - Dependencias del proyecto

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, lee nuestras pautas de contribución antes de enviar pull requests.

## Contacto

Si tienes preguntas o sugerencias, no dudes en abrir un issue en el repositorio.
