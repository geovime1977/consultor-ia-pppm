# consultor-ia-pppm

App Streamlit para **consultores de IA aplicada ao PPPM** (Portfólio, Programa e Projeto), evolução do MVP `diag-ia-pppm` apresentado na Aula 1 do curso BSBr do Prof. Dr. José Bezerra em 2026-08-08.

Transforma uma demanda vaga de IA em **mapa inicial estruturado** — contexto, diagnóstico de maturidade em 5 dimensões, Mapa 5 Blocos, 3 pilotos recomendados com **KPI benchmark auditável + plano 30d + casos reais** e PDF final para o cliente.

## Diferença para o projeto-mãe (`diag-ia-pppm`)

O `diag-ia-pppm` é o snapshot congelado da versão apresentada ao Bezerra na Aula 1. Este projeto (`consultor-ia-pppm`) recebe todas as melhorias pós-aula:

- Benchmark KPI auditável por piloto (PMI, Gartner, McKinsey, papers) — arquivos `data/benchmark_lote_*.json`
- Plano de projeto 30d por piloto com EAP + cronograma + papéis (backlog Giancarlo aprovado por Bezerra)
- 5 casos reais para storytelling em `data/cases_bezerra.json`
- Taglines Bezerra no header e PDF
- Preset Empresa Alfa como projeto seed
- Documentação dos 5 frameworks proprietários do Bezerra

## Stack
- Streamlit + ReportLab + Python 3.14
- 100% determinístico (sem LLM)

## Como rodar

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run app.py --server.port 8512
```

Abre em `http://localhost:8512`.

## Como rodar os testes

```bash
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/pytest tests/ -v
```

## Estrutura

- `app.py` — entrypoint Streamlit (8 abas)
- `src/` — módulos (state, contexto, diagnostico, mapa_blocos, recomendador, pdf_export, niveis, projetos, comparar, mapa_pmbok, db, validators)
- `data/` — pilotos enriquecidos, benchmarks, cases, níveis, dicionário de dor, mapa PMBOK
- `docs/` — arquitetura, fontes primárias Bezerra (PDFs + extrações), tutoriais
- `output/` — PDFs gerados (ignorado pelo git)
