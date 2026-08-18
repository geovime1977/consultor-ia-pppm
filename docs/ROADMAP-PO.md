# Roadmap — Reativar Pesquisa Operacional no app

## Estado atual (2026-08-18)

- `src/config.py::MOSTRAR_PO_UI = False` — flag global oculta PO da interface para a turma da Aula 2 do Prof. Bezerra.
- **Nada de PO é executado hoje** — o que existia era apenas texto estático curado (colunas IA+PO em `pmbok_processos.json`, campos IA+PO nos 16 pilotos de `pilotos.json`). Zero solver, zero otimização.
- Dados de curadoria ficam intactos nos JSONs (não foram apagados).

## O que reativar quando quiser voltar a mostrar PO estático

Trocar `MOSTRAR_PO_UI = True` em `src/config.py`. Em 1 linha:

- Título e sidebar voltam a exibir "× IA × IA+PO".
- Aba 1 mostra as 4 colunas IA+PO na tabela + a coluna "🧮 IA + PO" nas fichas.
- Aba 8 volta a mostrar a dimensão IA+PO no heatmap e a métrica "IA + PO" no ranking.

## O que construir para o PO **calcular de verdade** (Motor PO integrado)

Isto exige código novo, não flag. Escopo previsto para reativação futura:

### Módulos determinísticos (Python, zero LLM)

1. `src/po/milp.py` — solver de otimização de portfólio (PuLP ou OR-Tools) usando os pilotos como candidatos, restrições de orçamento/capacidade e função-objetivo de valor esperado.
2. `src/po/ahp.py` — decisão multi-critério (Analytic Hierarchy Process) para priorização hierárquica de pilotos, alternativa/complemento ao score executivo da Aula 2.
3. `src/po/sapevo_m.py` — SAPEVO-M para casos em que critérios são ordenados sem par-a-par (rápido para reuniões).
4. `src/po/monte_carlo.py` — simulação estocástica de cenários (prazo, custo, ROI) para o "Valor potencial" da matriz de priorização.
5. `src/po/dea.py` — Data Envelopment Analysis para comparar eficiência entre projetos do portfólio (aba 8).
6. `src/po/mmc.py` — teoria de filas M/M/c para dimensionar squads de execução dos pilotos aprovados.

### Integrações no app

- **Aba 9 (Priorização):** botão "Reprocessar com AHP" ao lado do score executivo — comparação entre método Bezerra (ponderação fixa 30/20/20/15/15) e AHP calibrado pelo aluno.
- **Aba 10 (Governança):** botão "Simulação Monte Carlo do valor esperado" — gera distribuição do ROI antes de aprovar escalar o piloto.
- **Nova aba 12 (Portfólio ótimo):** MILP que combina restrições de budget/pessoas e retorna carteira ótima de pilotos.
- **Aba 8 (Comparar):** DEA para eficiência relativa entre projetos.

### Fontes/documentação

- Motor PO da Eixo Estratégico — código de referência em `~/projetos/*` (procurar `po-analyst`, `or-decision-engine`, `po-interrogator` como agentes/skills)
- MBA em Pesquisa Operacional (Geovane) — base teórica dos 6 modelos acima
- Skill `or-decision-engine` (`~/.claude/skills/`) — sabe modelar cada método

## Público-alvo do PO real

- Uso interno da Eixo Estratégico em consultoria PME (Fase 3 do funil, `dados/cliente.json` → Motor PO → PDF)
- Alunos avançados de MBA em PO / mestrado (não a turma introdutória da Aula 2 do Bezerra)
- Cliente corporativo que contratar workshop PO

## Estimativa

- Reativar UI (flag → True): **1 minuto**
- Construir 1 módulo PO real (ex: AHP integrado à aba 9): **4-6 horas**
- Construir todos os 6 módulos + integrações: **3-5 dias**
