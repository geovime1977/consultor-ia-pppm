# Tutorial Técnico — consultor-ia-pppm

Documentação para desenvolvedor que precisa rodar, entender, testar ou estender o app.

Para arquitetura completa (schemas, pseudo-código do recomendador, layout do PDF), leia `docs/ARQUITETURA.md`. Este documento é o quick-start técnico.

---

## Arquitetura e decisões de design

**Single-page com `st.tabs()` — não multipage.**
Método é sequencial e curto (5 etapas, ~10 minutos). Multipage do Streamlit fragmenta `session_state` entre reruns e obriga navegação por sidebar, quebrando o fluxo pedagógico. Com abas o participante vê o percurso inteiro desde o início e volta livremente para ajustar respostas.

**Zero LLM na v1.**
Recomendador é 100% determinístico: score baseado em (gargalo × dimensões-alvo dos pilotos) + (categorias de dor extraídas por matching literal × categorias dos pilotos) + ajustes por nível de maturidade. Toda a lógica está em `src/recomendador.py` — inspecionável, testável e sem custo por execução.

**Dados versionados em JSON, não hard-coded.**
`data/pilotos.json` (catálogo de 12 pilotos), `data/niveis.json` (5 níveis + templates de leitura executiva) e `data/keywords_dor.json` (15 categorias de dor com palavras-chave). Editáveis sem tocar em Python.

**PDF por ReportLab puro.**
Sem WeasyPrint (evita deps binárias), sem HTML→PDF. Layout definido programaticamente em `src/pdf_export.py`.

---

## Stack e dependências

**Produção (`requirements.txt`):**
- `streamlit>=1.40.0`
- `reportlab>=4.2.0`

**Desenvolvimento (`requirements-dev.txt`):**
- `pytest>=8.0.0`
- `pypdf>=4.0.0` (usado só nos testes que inspecionam PDF gerado)

Python 3.14 testado. Deve funcionar em 3.10+.

---

## Como rodar localmente

```bash
cd ~/projetos/consultor-ia-pppm

# Setup (uma vez)
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt -r requirements-dev.txt

# Rodar app
.venv/bin/streamlit run app.py --server.port 8512

# Rodar testes
.venv/bin/pytest tests/ -v
```

Porta 8512 é reservada no ecossistema Eixo (portas 8501–8510 usadas por outros apps).

Smoke test end-to-end sem UI (útil em CI):
```bash
.venv/bin/python3 -c "
from src.recomendador import recomendar
from src.pdf_export import gerar_pdf
ctx={'nome':'Teste','empresa':'X','porte':'Média','n_projetos':10,'pmo_ativo':True,'cargo':'PM'}
diag={'estrategia':4,'dados':3,'casos_uso':2,'governanca':1,'beneficios':2}
mapa={'contexto':'ok'*20,'dor':'atraso status'*5,'dados':'atas'*10,'riscos':'lgpd'*10,'valor':'sla'*10}
from src.diagnostico import calcular_total, calcular_nivel, identificar_gargalo
p=recomendar(diag, mapa, 3)
dados={'contexto':ctx,'diagnostico':diag,'mapa':mapa,'pilotos_selecionados':p,'total':calcular_total(diag),'nivel':calcular_nivel(calcular_total(diag)),'gargalo':identificar_gargalo(diag)}
print(gerar_pdf(dados, '/tmp/smoke.pdf'))
"
```

---

## Como rodar em produção

**Local (cliente final ou sala de aula):**
Basta o setup acima. App roda em `localhost:8512`. Sem servidor, sem SSL, sem exposição pública. Este é o modo de uso principal.

**Não recomendado deploy VPS/Coolify** — o app é ferramenta de demo pontual, não serviço 24/7. Se algum dia precisar, adicionar `Dockerfile` (base `python:3.14-slim`), expor porta 8512, configurar `CMD ["streamlit","run","app.py","--server.port","8512","--server.address","0.0.0.0"]`.

---

## Estrutura do código

```
src/
├── state.py         # gerencia st.session_state (init, is_step_complete, get_all_data)
├── contexto.py      # aba 1 — formulário de contexto
├── diagnostico.py   # aba 2 — 5 sliders, cálculo de total/nível/gargalo
├── niveis.py        # loader de data/niveis.json (get_nivel(total))
├── mapa_blocos.py   # aba 3 — 5 text_area com validação de min-chars
├── recomendador.py  # aba 4 — matching determinístico + scoring
├── pdf_export.py    # aba 5 — geração do PDF via ReportLab
└── validators.py    # validação de campos entre abas
```

Fluxo entre módulos:
```
app.py ──▶ state.init_state()
   │
   ├─▶ contexto.render()       ──▶ st.session_state["contexto"]
   ├─▶ diagnostico.render()    ──▶ st.session_state["diagnostico"]
   ├─▶ mapa_blocos.render()    ──▶ st.session_state["mapa"]
   ├─▶ recomendador.recomendar(diag, mapa, 3)  ──▶ st.session_state["pilotos_selecionados"]
   └─▶ pdf_export.gerar_pdf(state.get_all_data(), path)
```

---

## Regra determinística do recomendador (resumo)

```
score(piloto) = 10 se gargalo em piloto.dimensoes_alvo
             + 3 por cada dimensão < 3 do participante coberta pelo piloto
             + 5 × |categorias_dor_participante ∩ categorias_piloto|
             + 4 se nível ≤ 2 e viabilidade_base = alto
             + 4 se nível ≥ 4 e impacto_base = alto
             − 5 se nível ≤ 2 e risco_base = alto

Fallback: se retorno < top_n, completa com pilotos viabilidade=alto + risco=baixo.
Scoring final: ajusta labels do piloto conforme nível (ex: nível baixo derruba viabilidade alta para média).
```

Pseudo-código completo: `docs/ARQUITETURA.md` seção 4.
Cobertura de testes: `tests/test_recomendador.py` (8 casos).

---

## Como estender

**Adicionar um novo piloto ao catálogo:**
1. Editar `data/pilotos.json` — copiar objeto existente e ajustar campos (schema em `docs/ARQUITETURA.md` seção 3).
2. Se o piloto atacar dor nova, adicionar categoria em `data/keywords_dor.json`.
3. Rodar `pytest tests/test_recomendador.py -v` para garantir que nada quebrou.
4. Não precisa mudar Python.

**Mudar a regra de scoring:**
- Editar `src/recomendador.py::recomendar()` (regra principal) e `scoring_piloto()` (labels finais).
- Ajustar testes em `tests/test_recomendador.py` para refletir nova regra.

**Adicionar nova dimensão ao diagnóstico:**
1. Adicionar chave no schema de `st.session_state["diagnostico"]` em `src/state.py`.
2. Adicionar slider em `src/diagnostico.py::render()`.
3. Atualizar `identificar_gargalo()` para incluir a nova dimensão na ordem de desempate.
4. Atualizar faixas de nível em `data/niveis.json` (se o total máximo mudar).
5. Atualizar `src/pdf_export.py` para incluir a nova linha na tabela do diagnóstico.
6. Atualizar testes.

**Mudar layout do PDF:**
- `src/pdf_export.py` — estilos no topo do módulo (constantes `H1_STYLE`, `H2_STYLE` etc.).
- Estrutura das páginas em `gerar_pdf()`.
- Header/footer em `_header()` / `_footer()`.

**Substituir recomendador por LLM (futuro):**
- Trocar a implementação de `recomendador.recomendar()` mantendo a assinatura `(diagnostico, mapa, top_n) -> list[dict]`.
- Injetar via variável de ambiente `DIAG_IA_PPPM_USE_LLM=true` para manter caminho determinístico como default.
- Adicionar dep `anthropic` ou `openai` em `requirements-optional.txt`.

---

## Variáveis de ambiente

Nenhuma obrigatória na v1. O app roda sem `.env`, sem chaves de API e sem secrets. Toda a lógica é local e determinística.

Se você configurar Streamlit customizado, use `.streamlit/config.toml` na raiz do projeto (não versionado).

---

## Testes

28 testes cobrindo:
- **`test_diagnostico.py`** — cálculo de total, 5 faixas de nível, gargalo com 3 tipos de empate.
- **`test_recomendador.py`** — match direto por gargalo, match por dor, fallback completando top-N, ajuste de scoring por nível baixo/alto, normalização de acentos.
- **`test_pdf_export.py`** — geração de arquivo, contagem de páginas (≥5), slugificação do nome.

Rodar: `.venv/bin/pytest tests/ -v`
Cobertura mínima esperada: recomendador e diagnóstico 100%, pdf_export smoke-only.

---

## Convenções do projeto

- Textos de UI e PDF em pt-BR
- Sem comentários no código salvo quando o "porquê" for não óbvio
- Sem error handling defensivo para cenários impossíveis (validação de entrada em `validators.py`)
- Sem abstrações prematuras
- Textos-guia dos formulários e template de leitura executiva vieram do vocabulário do Prof. Bezerra (PDF da aula em `~/Downloads/Aula_1_Formacao_Consultores_IA_PPPM_BSBr (1).pdf`)

---

## Créditos

- Método pedagógico: **Prof. Dr. José Bezerra** — BSBr
- Base normativa: **PMI — The Standard for Artificial Intelligence in Portfolio, Program and Project Management (2026)**
- Implementação: **Geovane Virmecati** — Eixo Estratégico
