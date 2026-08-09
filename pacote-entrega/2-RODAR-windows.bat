@echo off
REM ============================================================
REM RODAR — diag-ia-pppm (Windows)
REM Duplo-clique neste arquivo para abrir o app.
REM ============================================================

cd /d "%~dp0\diag-ia-pppm"

echo.
echo ================================================================
echo   Abrindo diag-ia-pppm no seu navegador...
echo   Endereco: http://localhost:8511
echo.
echo   Para encerrar o app, feche esta janela ou pressione Ctrl+C.
echo ================================================================
echo.

timeout /t 2 /nobreak >nul
start "" "http://localhost:8511"

.venv\Scripts\streamlit.exe run app.py --server.port 8511 --browser.gatherUsageStats false
