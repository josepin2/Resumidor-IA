@ECHO OFF
TITLE Lanzador de Resumidor con Ollama y Gemma 3

:: --- CONFIGURACION ---
:: Modifica estas variables si tu proyecto tiene nombres diferentes.
SET VENV_NAME=venv
SET PYTHON_APP=app.py
SET FLASK_URL=http://localhost:5001
SET OLLAMA_SERVER=http://localhost:11434

ECHO.
ECHO ===================================================
ECHO  Lanzador de la Aplicacion de Resumen con Ollama
ECHO ===================================================
ECHO.

:: --- 1. VERIFICAR SI OLLAMA ESTÁ EN EJECUCIÓN ---
ECHO Verificando si Ollama está en ejecución...
curl --connect-timeout 3 -s -o nul %OLLAMA_SERVER%/api/tags
IF %ERRORLEVEL% NEQ 0 (
    ECHO.
    ECHO [ATENCIÓN] Ollama no parece estar en ejecución.
    ECHO Intentando iniciar Ollama...
    start "" /B ollama serve
    timeout /t 5 /nobreak > nul
    
    :: Verificar nuevamente después de intentar iniciar
    curl --connect-timeout 3 -s -o nul %OLLAMA_SERVER%/api/tags
    IF %ERRORLEVEL% NEQ 0 (
        ECHO.
        ECHO [ERROR] No se pudo conectar con Ollama.
        ECHO Por favor, asegúrate de que Ollama esté instalado y en ejecución.
        ECHO Puedes descargarlo desde: https://ollama.ai/
        ECHO.
        PAUSE
        GOTO :EOF
    )
)

:: --- 2. VERIFICAR SI EL MODELO ESTÁ DESCARGADO ---
ECHO Verificando el modelo gemma3:4b-it-qat...
curl --connect-timeout 3 -s -o model_check.tmp %OLLAMA_SERVER%/api/tags
findstr /C:"gemma3:4b-it-qat" model_check.tmp >nul
IF %ERRORLEVEL% NEQ 0 (
    ECHO.
    ECHO [INFORMACIÓN] El modelo gemma3:4b-it-qat no está descargado.
    ECHO Se descargará automáticamente la primera vez que se use.
    ECHO Esto puede tomar varios minutos dependiendo de tu conexión a Internet.
    ECHO.
)
del model_check.tmp >nul 2>&1

:: --- 3. VERIFICACION DEL ENTORNO VIRTUAL ---
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

:: --- 4. ACTIVACION DEL ENTORNO VIRTUAL ---
ECHO Activando el entorno virtual...
CALL "%VENV_NAME%\Scripts\activate.bat"
ECHO Entorno virtual activado.
ECHO.

:: --- 5. INICIO DE LA APLICACION Y EL NAVEGADOR ---
ECHO Abriendo la aplicacion en tu navegador en: %FLASK_URL%
START "" %FLASK_URL%

ECHO.
ECHO Iniciando el servidor de Flask...
ECHO (Para detener el servidor, presiona CTRL+C en esta ventana)
ECHO.
python %PYTHON_APP%

:: --- FIN ---
:: Cerrar la ventana de Ollama si se abrió automáticamente
TASKKILL /F /IM ollama.exe /T >nul 2>&1
ECHO.
ECHO Servidor detenido.
PAUSE