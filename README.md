# consultor-ia-pppm

App Streamlit para **consultores de IA aplicada ao PPPM** (Portfólio, Programa e Projeto), evolução do MVP `diag-ia-pppm` apresentado na Aula 1 do curso BSBr do Prof. Dr. José Bezerra em 2026-08-08 e estendido com o método da Aula 2 (2026-08-17).

Transforma uma demanda vaga de IA em **mapa inicial estruturado** — contexto, diagnóstico de maturidade em 5 dimensões, Mapa 5 Blocos, 3 pilotos recomendados com **KPI benchmark auditável + plano 30d + casos reais** e PDF final para o cliente. A partir da Aula 2, também **prioriza casos de uso** (score 30/20/20/15/15), **detecta os 5 erros clássicos** e aplica **governança + HITL**.

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

## Módulos da Aula 2 (adicionados em 2026-08-18)

Baseados no deck oficial da Aula 2 do Prof. Bezerra ("Casos de Uso, Priorização e Governança"):

- **Aba 9 · Priorização** — score ponderado em 5 critérios (Impacto 30% · Viabilidade 20% · Dados 20% · Risco 15% · Valor 15%), matriz Impacto × Viabilidade, ranking Fazer agora / Preparar / Não priorizar. Corte obrigatório: caso sem dono humano da decisão não está pronto (slide 30). Vem com o preset Empresa Alfa (slide 37) já carregado.
- **Aba 9 (embutido) · Validador dos 5 Erros** — cada caso passa por 5 regras determinísticas (começar pela ferramenta, fascínio técnico, ignorar dados, confundir automação com decisão, não medir valor/risco). Alertas em tempo real.
- **Aba 10 · Governança + HITL** — política em 4 blocos de segurança + fluxo de rastreabilidade de 5 passos + nível HITL (leve/moderada/alta) puxado da nota de impacto pelo princípio de ouro: *quanto maior o impacto da decisão, maior a validação humana*.

## Estrutura

- `app.py` — entrypoint Streamlit (10 abas)
- `src/` — módulos (state, contexto, diagnostico, mapa_blocos, recomendador, pdf_export, niveis, projetos, comparar, mapa_pmbok, db, validators, **priorizacao, priorizacao_ui, validador_erros, governanca, governanca_ui**)
- `data/` — pilotos enriquecidos, benchmarks, cases, níveis, dicionário de dor, mapa PMBOK, **criterios_priorizacao.json, regras_5_erros.json, politica_governanca.json**
- `docs/` — arquitetura, fontes primárias Bezerra (PDFs + extrações), tutoriais
- `output/` — PDFs gerados (ignorado pelo git)

## Deploy público para alunos (Streamlit Community Cloud)

Passos manuais (ação humana obrigatória — o Streamlit Cloud precisa da autenticação do dono do repo):

1. Acesse https://share.streamlit.io/ e faça login com a conta GitHub `geovime1977`.
2. Clique **New app** → **Deploy a public app from GitHub**.
3. Preencha:
   - **Repository:** `geovime1977/consultor-ia-pppm`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL** (opcional): `consultor-ia-pppm` — resulta em `https://consultor-ia-pppm.streamlit.app`
4. Em **Advanced settings** confirme **Python version = 3.11** (o repo já traz `runtime.txt` fixando).
5. **Deploy!** — primeira build leva ~2 min. Nenhum secret necessário (app 100% determinístico).
6. Copie a URL final e distribua no folder do Drive da turma.

Para atualizar após novos commits: o Streamlit Cloud re-deploya automaticamente a cada push em `main`.
