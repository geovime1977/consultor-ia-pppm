#!/bin/bash
# ============================================================
# INSTALADOR — diag-ia-pppm (Mac)
# Duplo-clique neste arquivo para instalar.
# ============================================================

set -e
cd "$(dirname "$0")"

echo ""
echo "================================================================"
echo "  Instalando diag-ia-pppm"
echo "  App do método de IA aplicada ao PPPM — Aula 1 Prof. Bezerra"
echo "================================================================"
echo ""

if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python 3 não está instalado."
    echo ""
    echo "Baixe e instale em: https://www.python.org/downloads/"
    echo "Depois rode este instalador novamente."
    echo ""
    read -p "Pressione ENTER para fechar..."
    exit 1
fi

echo "[1/4] Descompactando o app..."
if [ ! -d "diag-ia-pppm" ]; then
    unzip -q diag-ia-pppm.zip
fi

echo "[2/4] Criando ambiente Python..."
cd diag-ia-pppm
python3 -m venv .venv

echo "[3/4] Instalando dependências (streamlit + reportlab)..."
.venv/bin/pip install --quiet --upgrade pip
.venv/bin/pip install --quiet -r requirements.txt

echo "[4/4] Testando instalação..."
.venv/bin/python3 -c "import streamlit, reportlab; print('OK: dependências instaladas')"

echo ""
echo "================================================================"
echo "  Instalação concluída com sucesso!"
echo ""
echo "  Para usar o app, dê duplo-clique em:"
echo "     2-RODAR-mac.command"
echo "================================================================"
echo ""
read -p "Pressione ENTER para fechar..."
