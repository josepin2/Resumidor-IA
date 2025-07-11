@ECHO OFF
TITLE Lanzador de Resumidor Flask

:: --- CONFIGURACION ---
:: Modifica estas variables si tu proyecto tiene nombres diferentes.
SET VENV_NAME=venv
SET PYTHON_APP=app.py
SET FLASK_URL=http://localhost:5001

ECHO.
ECHO ===================================================
ECHO  Lanzador de la Aplicacion de Resumen con Ollama
ECHO ===================================================
ECHO.

:: --- 1. VERIFICACION DEL ENTORNO VIRTUAL ---
ECHO Buscando el entorno virtual en la carpeta '%VENV_NAME%'...
IF NOT EXIST "%VENV_NAME%\Scripts\activate.bat" (
    ECHO.
    ECHO [ERROR] No se encuentra el entorno virtual en la carpeta '%VENV_NAME%'.
    ECHO Por favor, asegurate de que la carpeta del entorno virtual existe y tiene el nombre correcto.
    ECHO Si no lo has creado, abre una terminal y ejecuta: python -m venv %VENV_NAME%
    ECHO.
    PAUSE
    GOTO :EOF
)

:: --- 2. ACTIVACION DEL ENTORNO VIRTUAL ---
ECHO Activando el entorno virtual...
CALL "%VENV_NAME%\Scripts\activate.bat"
ECHO Entorno virtual activado.
ECHO.

:: --- 3. INICIO DE LA APLICACION Y EL NAVEGADOR ---
ECHO Abriendo la aplicacion en tu navegador en: %FLASK_URL%
START "" %FLASK_URL%

ECHO.
ECHO Iniciando el servidor de Flask...
ECHO (Para detener el servidor, presiona CTRL+C en esta ventana)
ECHO.
python %PYTHON_APP%

:: --- FIN ---
ECHO.
ECHO Servidor detenido.
PAUSE