@echo off
REM ============================================================
REM INSTALADOR — diag-ia-pppm (Windows)
REM Duplo-clique neste arquivo para instalar.
REM ============================================================

cd /d "%~dp0"

echo.
echo ================================================================
echo   Instalando diag-ia-pppm
echo   App do metodo de IA aplicada ao PPPM — Aula 1 Prof. Bezerra
echo ================================================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo ERRO: Python 3 nao esta instalado.
    echo.
    echo Baixe e instale em: https://www.python.org/downloads/
    echo IMPORTANTE: Na instalacao, marque a opcao "Add Python to PATH".
    echo Depois rode este instalador novamente.
    echo.
    pause
    exit /b 1
)

echo [1/4] Descompactando o app...
if not exist "diag-ia-pppm\" (
    powershell -Command "Expand-Archive -Path diag-ia-pppm.zip -DestinationPath . -Force"
)

echo [2/4] Criando ambiente Python...
cd diag-ia-pppm
python -m venv .venv

echo [3/4] Instalando dependencias (streamlit + reportlab)...
.venv\Scripts\pip.exe install --quiet --upgrade pip
.venv\Scripts\pip.exe install --quiet -r requirements.txt

echo [4/4] Testando instalacao...
.venv\Scripts\python.exe -c "import streamlit, reportlab; print('OK: dependencias instaladas')"

echo.
echo ================================================================
echo   Instalacao concluida com sucesso!
echo.
echo   Para usar o app, de duplo-clique em:
echo      2-RODAR-windows.bat
echo ================================================================
echo.
pause
