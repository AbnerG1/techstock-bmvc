@echo off
setlocal
cd /d "%~dp0"
title TechStock - Inicializacao

if not exist ".venv\Scripts\python.exe" (
    echo Criando o ambiente do TechStock...
    py -m venv .venv
    if errorlevel 1 goto erro
)

".venv\Scripts\python.exe" -c "import bottle" >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 goto erro
)

echo Iniciando o TechStock. O navegador sera aberto automaticamente.
echo Para encerrar, pressione Ctrl+C nesta janela.
".venv\Scripts\python.exe" route.py
if errorlevel 1 goto erro
exit /b 0

:erro
echo.
echo Nao foi possivel iniciar o TechStock. Confira se o Python esta instalado.
pause
exit /b 1
