# Script PowerShell para iniciar Olhar Literário
# Execute com: .\iniciar.ps1

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                        ║" -ForegroundColor Cyan
Write-Host "║           OLHAR LITERÁRIO - SERVIDOR DJANGO            ║" -ForegroundColor Cyan
Write-Host "║                                                        ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
Write-Host "[1/4] Verificando Python..." -NoNewline
try {
    $pythonVersion = python --version 2>&1
    Write-Host " OK" -ForegroundColor Green
    Write-Host "      $pythonVersion" -ForegroundColor Gray
} catch {
    Write-Host " ERRO" -ForegroundColor Red
    Write-Host ""
    Write-Host "Python não encontrado!" -ForegroundColor Red
    Write-Host "Instale em: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Pressione Enter para sair"
    exit 1
}
Write-Host ""

# Verificar Django
Write-Host "[2/4] Verificando Django..." -NoNewline
$djangoInstalled = python -c "import django" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host " Não encontrado" -ForegroundColor Yellow
    Write-Host "      Instalando dependências..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "Erro ao instalar dependências!" -ForegroundColor Red
        Read-Host "Pressione Enter para sair"
        exit 1
    }
    Write-Host "      Instalação concluída!" -ForegroundColor Green
} else {
    Write-Host " OK" -ForegroundColor Green
}
Write-Host ""

# Configurar banco de dados
Write-Host "[3/4] Configurando banco de dados..." -NoNewline
Set-Location olhar_literario_django
python manage.py makemigrations books 2>$null | Out-Null
python manage.py migrate 2>$null | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host " OK" -ForegroundColor Green
} else {
    Write-Host " Tentando sincronizar..." -ForegroundColor Yellow
    python manage.py migrate --run-syncdb | Out-Null
    Write-Host " OK" -ForegroundColor Green
}
Write-Host ""

# Iniciar servidor
Write-Host "[4/4] Iniciando servidor..." -ForegroundColor Green
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                  SERVIDOR ATIVO!                       ║" -ForegroundColor Green
Write-Host "╠════════════════════════════════════════════════════════╣" -ForegroundColor Green
Write-Host "║                                                        ║" -ForegroundColor White
Write-Host "║  Frontend:  " -NoNewline -ForegroundColor White
Write-Host "http://localhost:8000" -NoNewline -ForegroundColor Cyan
Write-Host "                     ║" -ForegroundColor White
Write-Host "║  Admin:     " -NoNewline -ForegroundColor White
Write-Host "http://localhost:8000/admin" -NoNewline -ForegroundColor Cyan
Write-Host "               ║" -ForegroundColor White
Write-Host "║                                                        ║" -ForegroundColor White
Write-Host "║  Pressione Ctrl+C para parar o servidor               ║" -ForegroundColor White
Write-Host "║                                                        ║" -ForegroundColor White
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# Abrir navegador automaticamente após 2 segundos
Start-Sleep -Seconds 2
Start-Process "http://localhost:8000"

# Iniciar servidor
python manage.py runserver 0.0.0.0:8000

# Retornar à pasta original
Set-Location ..
Write-Host ""
Write-Host "Servidor encerrado." -ForegroundColor Yellow
Read-Host "Pressione Enter para sair"
