Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Smart Price Tracker - Web Interface" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verifica se Python está instalado
try {
    python --version | Out-Null
} catch {
    Write-Host "❌ Python não encontrado! Instale Python 3.10+" -ForegroundColor Red
    Read-Host "Pressione ENTER para sair"
    exit 1
}

# Instala dependências
Write-Host "📦 Verificando dependências..." -ForegroundColor Yellow
pip install -q -r requirements.txt

# Inicia o servidor
Write-Host "✅ Iniciando Smart Price Tracker na web..." -ForegroundColor Green
Write-Host "🌐 Acesse: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "⏹️  Pressione CTRL+C para parar o servidor" -ForegroundColor Yellow
Write-Host ""

python app_web.py

Read-Host "Pressione ENTER para sair"
