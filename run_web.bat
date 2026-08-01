@echo off
echo ========================================
echo Smart Price Tracker - Web Interface
echo ========================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado! Instale Python 3.10+
    pause
    exit /b 1
)

REM Instala dependências se necessário
echo 📦 Verificando dependências...
pip install -q -r requirements.txt

REM Inicia o servidor Flask
echo ✅ Iniciando Smart Price Tracker na web...
echo 🌐 Acesse: http://localhost:5000
echo.
echo ⏹️  Pressione CTRL+C para parar o servidor
echo.

python app_web.py

pause
