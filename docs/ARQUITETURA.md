# ARQUITETURA — consultor-ia-pppm

App Streamlit que operacionaliza a Aula 1 do Prof. Dr. José Bezerra (BSBr) — "Formação de Consultores em IA aplicada ao PPPM (Portfólio, Programa e Projeto)".

- **Porta:** 8512
- **Stack:** Streamlit + ReportLab + Python 3.14
- **LLM:** nenhum na v1 (100% determinístico)
- **Localização:** `/Users/virmecati/projetos/consultor-ia-pppm/`
- **Execução:** `streamlit run app.py --server.port 8512`

---

## 1. Estrutura de pastas

```
consultor-ia-pppm/
├── app.py                          # entrypoint Streamlit (roteador de abas)
├── requirements.txt
├── README.md
├── CLAUDE.md                       # copiado do template do vault
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── state.py                    # gerencia st.session_state (schema único)
│   ├── contexto.py                 # etapa 1 — formulário de contexto
│   ├── diagnostico.py              # etapa 2 — 5 dimensões, cálculo do nível
│   ├── mapa_blocos.py              # etapa 3 — 5 blocos de texto
│   ├── recomendador.py             # etapa 4 — regra determinística de matching
│   ├── pdf_export.py               # etapa 5 — geração ReportLab
│   ├── niveis.py                   # tabela de níveis + leituras executivas
│   └── validators.py               # validação de campos obrigatórios entre abas
├── data/
│   ├── pilotos.json                # catálogo de pilotos-tipo (editável)
│   ├── niveis.json                 # 5 níveis de maturidade + descrição
│   └── keywords_dor.json           # dicionário de palavras-chave por categoria
├── assets/
│   └── logo_bsbr.png               # opcional, header do PDF
├── output/                         # PDFs gerados (gitignore)
├── tests/
│   ├── test_recomendador.py
│   ├── test_diagnostico.py
│   └── test_pdf_export.py
└── docs/
    └── ARQUITETURA.md              # este documento
```

---

## 2. Módulos Python

### `app.py`
- Cria layout single-page com `st.tabs()` (5 abas + 1 export).
- Inicializa `st.session_state` chamando `state.init_state()`.
- Cada aba delega para o módulo correspondente.
- Sidebar mostra progresso: check em cada etapa concluída.

### `src/state.py`
- `init_state()` — cria chaves do session_state se não existirem.
- `is_step_complete(step: int) -> bool` — checa se etapa tem dados.
- `get_all_data() -> dict` — retorna dict consolidado para PDF.
- Schema único do state:
  ```python
  {
    "contexto": {"nome": "", "empresa": "", "porte": "", "n_projetos": 0, "pmo_ativo": False, "cargo": ""},
    "diagnostico": {"estrategia": 0, "dados": 0, "casos_uso": 0, "governanca": 0, "beneficios": 0},
    "mapa": {"contexto": "", "dor": "", "dados": "", "riscos": "", "valor": ""},
    "pilotos_selecionados": []  # preenchido pelo recomendador
  }
  ```

### `src/contexto.py`
- `render()` — formulário Streamlit com nome, empresa, porte (selectbox: PME/Média/Grande/Governo), nº projetos ativos, PMO ativo (radio), cargo do participante.
- Grava em `st.session_state["contexto"]`.

### `src/diagnostico.py`
- `render()` — 5 sliders (0–6) para as dimensões, mostra total e nível calculado em tempo real.
- `calcular_total(diag: dict) -> int`
- `calcular_nivel(total: int) -> dict` — chama `niveis.get_nivel(total)`.
- `identificar_gargalo(diag: dict) -> str` — retorna a dimensão de menor pontuação (empate → prioriza `governanca` > `dados` > `estrategia` > `casos_uso` > `beneficios`).
- Exibe leitura executiva textual explicando o gargalo.

### `src/niveis.py`
- Carrega `data/niveis.json` no import.
- `get_nivel(total: int) -> dict` — retorna `{numero, rotulo, faixa, descricao, leitura_executiva_template}`.
- Faixas: 0-6 Ausente · 7-12 Reativo · 13-18 Experimental · 19-24 Definido · 25-30 Otimizado.

### `src/mapa_blocos.py`
- `render()` — 5 `st.text_area` guiados (Contexto, Dor, Dados, Riscos, Valor), cada um com placeholder e helper text tirado da aula.
- Valida mínimo de 30 caracteres em cada bloco antes de liberar próxima aba.

### `src/recomendador.py`
- `carregar_catalogo() -> list` — lê `data/pilotos.json`.
- `carregar_keywords() -> dict` — lê `data/keywords_dor.json`.
- `extrair_categorias_dor(texto_dor: str) -> list[str]` — matching literal case-insensitive de palavras-chave.
- `recomendar(diagnostico: dict, mapa: dict, top_n: int = 3) -> list[dict]` — devolve os 3 pilotos ranqueados.
- `scoring_piloto(piloto: dict, nivel: int, categorias_dor: list) -> dict` — devolve `{impacto, viabilidade, risco}` como labels alto/médio/baixo, seguindo a regra do bloco 4.

### `src/pdf_export.py`
- `gerar_pdf(dados: dict, output_path: str) -> str` — usa ReportLab (`SimpleDocTemplate` + `Paragraph` + `Table`).
- `_header(canvas, doc)` — logo BSBr + título + data.
- `_footer(canvas, doc)` — rodapé com número da página + "Método Aula 1 — Prof. Dr. José Bezerra".
- Estilos definidos em constantes no topo do módulo (font family Helvetica, cores neutras).
- Retorna path final; nome do arquivo: `Mapa_Inicial_IA-PPPM_<slug_nome>_<YYYYMMDD>.pdf`.

### `src/validators.py`
- `validar_contexto(ctx: dict) -> tuple[bool, list[str]]`
- `validar_diagnostico(diag: dict) -> tuple[bool, list[str]]`
- `validar_mapa(mapa: dict) -> tuple[bool, list[str]]`
- Cada função retorna `(ok, [mensagens de erro])`.

---

## 3. Schema de `data/pilotos.json`

Arquivo raiz é uma lista de objetos. Campos por piloto:

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | str (kebab-case) | identificador único |
| `nome` | str | rótulo curto |
| `descricao` | str | 1-2 frases sobre o piloto |
| `dimensoes_alvo` | list[str] | quais dimensões do diagnóstico ele endereça (subset de `estrategia`, `dados`, `casos_uso`, `governanca`, `beneficios`) |
| `categorias_dor` | list[str] | categorias que ele resolve (bate com `keywords_dor.json`) |
| `impacto_base` | str | `alto` \| `medio` \| `baixo` |
| `viabilidade_base` | str | idem |
| `risco_base` | str | idem |
| `pre_requisitos` | list[str] | dados/sistemas necessários |
| `ganho_esperado` | str | frase única com valor esperado |
| `tempo_estimado_semanas` | int | prazo típico do piloto |

### Exemplos preenchidos (3)

```json
[
  {
    "id": "assistente-status-executivo",
    "nome": "Assistente de Status Executivo",
    "descricao": "Gera automaticamente resumos executivos semanais consolidando status de múltiplos projetos do portfólio, com destaque para desvios e riscos.",
    "dimensoes_alvo": ["estrategia", "governanca"],
    "categorias_dor": ["comunicacao_stakeholder", "reporting", "visibilidade_portfolio"],
    "impacto_base": "alto",
    "viabilidade_base": "alto",
    "risco_base": "baixo",
    "pre_requisitos": ["Planilha ou ferramenta de status atualizada semanalmente", "Modelo de resumo padrão"],
    "ganho_esperado": "Redução de 70% no tempo de consolidação de status executivo semanal",
    "tempo_estimado_semanas": 3
  },
  {
    "id": "radar-riscos-projeto",
    "nome": "Radar de Riscos de Projeto",
    "descricao": "Classifica automaticamente riscos registrados em atas e relatórios, priorizando pela combinação probabilidade × impacto e sinalizando riscos emergentes.",
    "dimensoes_alvo": ["governanca", "casos_uso"],
    "categorias_dor": ["risco", "atraso", "estouro_orcamento"],
    "impacto_base": "alto",
    "viabilidade_base": "medio",
    "risco_base": "medio",
    "pre_requisitos": ["Histórico de atas e RAIDs dos últimos 6 meses", "Taxonomia de riscos aprovada"],
    "ganho_esperado": "Antecipação de 40% dos riscos críticos antes do ciclo de status mensal",
    "tempo_estimado_semanas": 5
  },
  {
    "id": "priorizacao-portfolio-ia",
    "nome": "Priorização de Portfólio via IA",
    "descricao": "Score automático de projetos candidatos ao portfólio combinando critérios estratégicos, financeiros e de risco, com explicação da decisão (HITL).",
    "dimensoes_alvo": ["estrategia", "beneficios"],
    "categorias_dor": ["priorizacao", "alocacao_recursos", "roi"],
    "impacto_base": "alto",
    "viabilidade_base": "medio",
    "risco_base": "medio",
    "pre_requisitos": ["Critérios de priorização definidos", "Base histórica de projetos entregues", "Aprovação do PMO"],
    "ganho_esperado": "Aumento de 25% na aderência do portfólio à estratégia corporativa",
    "tempo_estimado_semanas": 6
  }
]
```

Catálogo final deve conter **12 pilotos** (produção fica a cargo do builder). Sugestões de nomes: Assistente de Status Executivo, Radar de Riscos, Análise de SLA, Base de Lições Aprendidas, Priorização de Portfólio, Consolidador de Atas, Auditor de Cronograma, Estimador de Esforço, Detector de Dependências, Sumarizador de Discovery, Classificador de Requisitos, Análise de Satisfação de Stakeholder.

### Schema de `data/niveis.json`

```json
[
  {
    "numero": 1,
    "rotulo": "Ausente",
    "faixa": [0, 6],
    "descricao": "Sem iniciativas de IA em PPPM. Processos manuais e reativos.",
    "leitura_executiva_template": "A organização ainda não possui iniciativas estruturadas de IA em PPPM. O gargalo em {gargalo} indica que o primeiro passo deve ser {acao_gargalo}."
  }
]
```
(uma entrada por nível, 5 entradas totais)

### Schema de `data/keywords_dor.json`

```json
{
  "comunicacao_stakeholder": ["status", "reporte", "reunião", "executivo", "diretoria"],
  "reporting": ["relatório", "consolidação", "dashboard"],
  "risco": ["risco", "incerteza", "problema", "issue"],
  "atraso": ["atraso", "prazo", "cronograma", "deadline"],
  "priorizacao": ["priorizar", "escolher", "backlog", "portfólio"]
}
```

---

## 4. Regra determinística de priorização (pseudo-código)

```
funcao recomendar(diagnostico, mapa, top_n=3):
    gargalo = identificar_gargalo(diagnostico)          # ex: "governanca"
    nivel = calcular_nivel(sum(diagnostico.values()))    # 1..5
    categorias_dor = extrair_categorias_dor(mapa.dor)    # ex: ["risco", "reporting"]

    candidatos = []
    para cada piloto em catalogo:
        score = 0

        # Match direto com gargalo (peso alto)
        se gargalo em piloto.dimensoes_alvo:
            score += 10

        # Match parcial com outras dimensões fracas (< 3)
        para cada dim em piloto.dimensoes_alvo:
            se diagnostico[dim] <= 3 e dim != gargalo:
                score += 3

        # Match com categorias de dor extraídas
        intersecao = piloto.categorias_dor ∩ categorias_dor
        score += len(intersecao) * 5

        # Ajuste por nível de maturidade
        se nivel <= 2 e piloto.viabilidade_base == "alto":
            score += 4                          # organização imatura → viabilidade importa mais
        se nivel >= 4 e piloto.impacto_base == "alto":
            score += 4                          # organização madura → impacto importa mais

        # Penalização por risco em orgs imaturas
        se nivel <= 2 e piloto.risco_base == "alto":
            score -= 5

        se score > 0:
            candidatos.append((piloto, score))

    # Fallback: se nada casou, devolve top-3 pilotos com viabilidade alta e risco baixo
    se len(candidatos) < top_n:
        fallback = filtrar(catalogo, viabilidade="alto", risco="baixo")
        candidatos.extend([(p, 1) para p em fallback])

    ordenar_desc(candidatos, por=score)
    resultado = []
    para cada (piloto, score) em candidatos[:top_n]:
        scoring_final = scoring_piloto(piloto, nivel, categorias_dor)
        resultado.append({...piloto, "scoring": scoring_final, "score_bruto": score})

    retornar resultado


funcao scoring_piloto(piloto, nivel, categorias_dor):
    # Ajusta o label base do piloto conforme contexto do participante
    impacto = piloto.impacto_base
    viabilidade = piloto.viabilidade_base
    risco = piloto.risco_base

    # Se nivel baixo, viabilidade cai um degrau
    se nivel <= 2 e viabilidade == "alto":
        viabilidade = "medio"

    # Se dor bate forte, impacto sobe um degrau
    se len(piloto.categorias_dor ∩ categorias_dor) >= 2 e impacto == "medio":
        impacto = "alto"

    # Se nivel baixo e piloto exige base histórica, risco sobe
    se nivel <= 2 e "histórico" em join(piloto.pre_requisitos).lower():
        risco = subir_grau(risco)

    retornar {impacto, viabilidade, risco}
```

---

## 5. Fluxo das telas Streamlit

**Recomendação: single-page com `st.tabs()`.**

**Justificativa:** o método é sequencial mas curto (5 etapas, ~10 minutos). Multipage do Streamlit fragmenta session_state entre reruns e obriga navegação por sidebar, o que quebra a sensação de fluxo pedagógico. Com `st.tabs()`:
- O usuário vê o percurso completo desde o início.
- Session_state persiste naturalmente.
- Fica trivial pular para trás e ajustar uma resposta.
- O botão "Gerar PDF" na última aba age como fecho natural.

### Estrutura das abas

```
[1. Contexto] [2. Diagnóstico] [3. Mapa 5 Blocos] [4. Pilotos Recomendados] [5. Exportar PDF]
```

- **Aba 1 — Contexto:** formulário curto (6 campos). Botão "Salvar contexto" ativa próxima aba.
- **Aba 2 — Diagnóstico:** 5 sliders 0–6. Cálculo em tempo real. Painel lateral mostra total, nível e gargalo com leitura executiva.
- **Aba 3 — Mapa 5 Blocos:** 5 text_area em coluna única. Contador de caracteres em cada. Botão "Salvar mapa" só habilita quando todos passam de 30 chars.
- **Aba 4 — Pilotos Recomendados:** ao entrar, chama `recomendador.recomendar()`. Mostra 3 cards com nome, descrição, scoring visual (badges coloridas), pré-requisitos e ganho esperado. Usuário pode substituir manualmente um piloto por outro do catálogo via selectbox.
- **Aba 5 — Exportar PDF:** preview textual do que vai no PDF + botão "Gerar PDF". Após geração, mostra `st.download_button`.

### Sidebar
- Progresso visual: check verde em cada etapa concluída, círculo cinza nas pendentes.
- Botão "Reiniciar sessão" (limpa session_state).
- Rodapé: "Método Aula 1 — Prof. Dr. José Bezerra | BSBr".

---

## 6. Layout do PDF gerado

Nome do arquivo: `Mapa_Inicial_IA-PPPM_<slug_nome>_<YYYYMMDD>.pdf`

### Estrutura de páginas

**Página 1 — Capa**
- Logo BSBr (topo, centralizado)
- Título: **"Mapa Inicial de Oportunidades de IA-PPPM"**
- Subtítulo: nome do participante + empresa
- Data de geração
- Rodapé: "Método Aula 1 — Prof. Dr. José Bezerra"

**Página 2 — Contexto do Participante**
- H1: "1. Contexto"
- Tabela 2 colunas (Campo | Valor) com todos os 6 campos da aba 1.

**Página 3 — Diagnóstico de Maturidade IA-PPPM**
- H1: "2. Diagnóstico de Maturidade"
- Tabela com 5 dimensões e pontuação (0–6).
- Linha de total (0–30).
- Box destacado: **Nível X — Rótulo** (ex: "Nível 3 — Experimental").
- Parágrafo: leitura executiva (texto do template do nível, com {gargalo} e {acao_gargalo} substituídos).

**Página 4 — Mapa 5 Blocos**
- H1: "3. Mapa 5 Blocos"
- 5 subseções (H2), uma por bloco: Contexto · Dor · Dados · Riscos · Valor.
- Cada uma exibe o texto do participante em bloco justificado.

**Página 5-6 — Pilotos Recomendados**
- H1: "4. Pilotos Recomendados"
- 3 subseções (H2), uma por piloto. Cada uma contém:
  - Nome + descrição
  - Tabela de scoring (Impacto | Viabilidade | Risco)
  - Lista de pré-requisitos (bullets)
  - Ganho esperado (destacado)
  - Tempo estimado

**Página final — Próximos Passos**
- H1: "5. Próximos Passos"
- Texto padrão (não vem do formulário):
  1. Validar viabilidade técnica com TI.
  2. Priorizar 1 dos 3 pilotos para MVP em 30 dias.
  3. Definir métrica de sucesso quantitativa.
  4. Agendar checkpoint em 60 dias.
- Rodapé em todas as páginas: "Método Aula 1 — Prof. Dr. José Bezerra" + número da página.

### Estilo ReportLab
- Font family: Helvetica.
- H1: 18pt bold, cor `#1f4e79`.
- H2: 14pt bold, cor `#2e75b6`.
- Body: 11pt, cor `#333333`, line spacing 1.4.
- Tabelas com borda fina cinza, header em fundo `#d9e1f2`.
- Margem: 2.5 cm em todos os lados.

---

## 7. `requirements.txt` proposto

```
streamlit>=1.40.0
reportlab>=4.2.0
```

**Justificativa da lista mínima:**
- `streamlit` — UI.
- `reportlab` — geração de PDF, puro Python, sem deps binárias.
- **Não incluir** `pandas` (não precisa — o volume de dados é trivial).
- **Não incluir** `openai`/qualquer LLM (v1 é 100% determinística).
- **Não incluir** `python-dotenv` (não há segredos).
- **Não incluir** `pydantic` (validação simples via funções puras em `validators.py`).

Testes usam `pytest` (dev-only, não vai no requirements.txt de produção — sugerir `requirements-dev.txt` com `pytest>=8.0.0`).

---

## Notas finais para o builder

- Todos os textos-guia do formulário (placeholders, helper texts, template de leitura executiva) devem sair do PDF da aula — o builder precisa abrir `/Users/virmecati/Downloads/Aula_1_Formacao_Consultores_IA_PPPM_BSBr (1).pdf` e extrair o vocabulário do Prof. Bezerra literalmente.
- O catálogo de 12 pilotos em `data/pilotos.json` deve ser inteiramente derivado de exemplos práticos citados na aula — não inventar.
- Não adicionar comentários no código salvo quando o "porquê" for não óbvio (regra de projeto).
- Executar `uv pip install -r requirements.txt` após criação.
- Após build, seguir procedimento padrão de projetos: backup OneDrive + análise no vault + tutorial em `Tino/COMO USAR.md`.
