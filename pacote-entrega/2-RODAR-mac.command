#!/bin/bash
# ============================================================
# RODAR — diag-ia-pppm (Mac)
# Duplo-clique neste arquivo para abrir o app.
# ============================================================

set -e
cd "$(dirname "$0")/diag-ia-pppm"

echo ""
echo "================================================================"
echo "  Abrindo diag-ia-pppm no seu navegador..."
echo "  Endereço: http://localhost:8511"
echo ""
echo "  Para encerrar o app, feche esta janela ou pressione Ctrl+C."
echo "================================================================"
echo ""

sleep 2
open "http://localhost:8511" &

.venv/bin/streamlit run app.py --server.port 8511 --browser.gatherUsageStats false
