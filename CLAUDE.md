# Diretiva de Contexto Global

Sempre consulte as configurações, comandos e subagentes definidos em `~/.claude/` antes de executar tarefas complexas.

---

# CLAUDE.md — consultor-ia-pppm

## Sobre este projeto

Fork/evolução do `diag-ia-pppm` (MVP apresentado na Aula 1 do curso BSBr em 2026-08-08).
Enquanto `diag-ia-pppm` fica preservado como **snapshot histórico** da versão demonstrada em aula,
`consultor-ia-pppm` é o **produto comercial em evolução** — recebe benchmark KPI auditável por piloto,
plano de projeto 30d com EAP (backlog Giancarlo aprovado por Bezerra em [02:48:54]),
casos reais para storytelling, taglines Bezerra, preset Empresa Alfa e documentação dos 5 frameworks
(5 Porquês, Pareto 80/20, 50 dores, 3 opções, Framework-vs-Metodologia).

- **O que faz:** App Streamlit que transforma demanda vaga de IA em mapa inicial estruturado — contexto, diagnóstico de maturidade em 5 dimensões, Mapa 5 Blocos, 3 pilotos recomendados **com KPI benchmark auditável + plano 30d + case reais** e PDF final para o cliente. Herda de diag-ia-pppm as abas Mapa PMBOK × IA × PO, Projetos (CRUD SQLite) e Comparar (radar + heatmap Plotly).
- **Stack:** Streamlit 1.40+, ReportLab 4.2+, openpyxl 3.1+, pandas 2.2+, plotly 5.20+, SQLite, Python 3.14. Zero LLM (100% determinístico).
- **Como rodar:** `.venv/bin/streamlit run app.py --server.port 8512`
- **Status:** em-desenvolvimento (upgrade pós-Aula 1)

## Localização

- **Local:** `~/projetos/consultor-ia-pppm/`
- **Backup:** `onedrive-eixoestrategico10:repos/consultor-ia-pppm`
- **Projeto-mãe (snapshot Aula 1):** `~/projetos/diag-ia-pppm/` (não modificar — congelado)
- **Nota no vault:** `01 - Profissional/Projetos/consultor-ia-pppm.md`

## Comandos principais

```bash
# Instalar
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt -r requirements-dev.txt

# Rodar
.venv/bin/streamlit run app.py --server.port 8512

# Testar
.venv/bin/pytest tests/ -v

# Backup
rclone copy . onedrive-eixoestrategico10:repos/consultor-ia-pppm
```

## Fontes primárias (voz do Bezerra)

Lidas e catalogadas em `docs/`:
- `BEZERRA-AULA1-R4.pdf` — deck oficial (39 slides, versão R4)
- `BEZERRA-AULA1-TRANSCRICAO-RAW.pdf` — transcrição completa da aula (99 páginas)
- `FONTES-BEZERRA-AULA1.md` — âncoras quantitativas com timestamp
- `FONTES-BEZERRA-AULA1-TRANSCRICAO-RAW.md` — extração cirúrgica (números novos, casos reais, frases-copy, frameworks)

## Dados curados

- `data/pilotos.json` — 12 pilotos com `metricas` (KPI + fontes) e `plano_projeto_30d` (EAP + cronograma + papéis)
- `data/benchmark_lote_A.json`, `B`, `C` — benchmark por lote, auditável (PMI, Gartner, McKinsey, papers)
- `data/cases_bezerra.json` — 5 casos reais para storytelling (SUS R$5M, Detran, 11k funcionários, oficina Felipe R$30k/mês, Marielle 8k docs)
- `data/niveis.json`, `keywords_dor.json`, `pmbok_processos.json` — herdados do diag-ia-pppm

## Portas reservadas do portfólio

8501 mestrado · 8502 study · 8503 casos-reais · 8504 prospec · 8506 concurso-radar · 8507 juridica · 8510 dashboard-win · **8511 diag-ia-pppm (snapshot)** · **8512 consultor-ia-pppm (este)**
