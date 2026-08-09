# FAQ — consultor-ia-pppm

Perguntas registradas durante os primeiros testes do app (2026-08-06). Cada uma vira uma orientação de uso ou um ponto de evolução do produto.

---

## 1. De onde vem a numeração do diagnóstico (5 dimensões × 0–6)?

**Vem direto da Aula 1 do Prof. Dr. José Bezerra (BSBr).** No slide 15 (caso Empresa Alfa), ele apresenta as 5 dimensões pontuadas 0–6, total 0–30, e 5 níveis derivados (Ausente / Reativo / Experimental / Definido / Otimizado).

A base normativa é o **PMI Standard for AI in PPPM (2026)** — os 5 domínios de prática (Stakeholders, Escopo, Arquitetura, Execução estratégica, Riscos) que o professor cita no slide 6.

Escala 0–6 é padrão em maturity models (CMMI, COBIT, PMI OPM3): reduz viés de resposta e força decisão, ao contrário de escalas 0–10 onde o respondente "empata em 5" por preguiça.

## 2. O professor explica o critério de pontuação na Aula 1?

**Não.** Ele mostra o método aplicado (Empresa Alfa dá 12/30, Nível 2), mas o slide 22 avisa: "cada encontro vai aprofundar uma etapa do método consultivo". Ou seja, a rubrica de scoring fica para as próximas aulas.

**Consequência:** hoje, cada aluno pontua no achismo. Duas pessoas na mesma empresa podem dar notas diferentes para "Governança". Isso é oportunidade de evolução do app (rubrica embutida em cada slider — ver seção 6).

## 3. Como preencher os 5 blocos do Mapa?

Cada bloco responde **uma pergunta única**:

| Bloco | Pergunta | Truque |
|---|---|---|
| Contexto | Onde estamos hoje? | Nomeie projeto/PMO + escala (nº projetos, tempo) |
| Dor | O que dói agora? | Comece por verbo: "atrasa", "erra", "conflita" |
| Dados | Que informação existe? | Liste fontes concretas (planilha X, sistema Y) |
| Riscos | O que exige validação humana? | LGPD, viés, alucinação, resistência, HITL |
| Valor | Que benefício executivo aparece? | Número + verbo: "reduzir X em 25%" |

Regra de bolso: 30–300 caracteres por bloco. Se passa disso, é relatório.

## 4. Os 3 pilotos recomendados são fixos? Posso trocar?

Os 3 são **os que melhor cruzam** seu gargalo (dimensão de menor pontuação) com as palavras-chave do seu bloco "Dor". Não são fixos: cada combinação de diagnóstico + dor devolve um top 3 diferente.

Você **pode substituir** qualquer um dos 3 pelo dropdown na aba 4. Faça isso quando:
- Seu cliente pediu explicitamente algo que não bate com a dor genérica
- Você já rodou piloto parecido e prefere variar
- O contexto tem uma restrição que o algoritmo não conhece (ex: sem histórico de dados)

## 5. Para que servem os outros 9 pilotos do catálogo?

O catálogo tem 12 pilotos. Organização por tipo de dor:

**Governança e comunicação executiva** — Assistente de Status Executivo, Consolidador de Atas, Análise de Satisfação de Stakeholder
**Risco e atraso** — Radar de Riscos e Atrasos, Auditor de Cronograma, Detector de Dependências
**Escopo e requisitos** — Sumarizador de Discovery, Classificador de Requisitos
**Dados operacionais** — Análise de SLA, Estimador de Esforço
**Estratégia e portfólio** — Priorização de Portfólio
**Aprendizado organizacional** — Base de Lições Aprendidas

O catálogo é editável — arquivo `data/pilotos.json` na raiz do projeto. Adicionar piloto novo: copiar objeto existente, ajustar campos (schema em `docs/ARQUITETURA.md` seção 3), rodar `pytest tests/test_recomendador.py` para garantir que nada quebrou.

## 6. Ideias para evoluir o app (backlog v2)

**Camada 1 (crítica) — Rubrica embutida em cada slider**
Helper text abaixo de cada slider explicando o que significa 0, 3 e 6 em cada dimensão. Resolve inconsistência de respostas.

**Camada 2 (importante) — Aba "Sobre o método"**
Nova aba com: origem (PMI 2026 + Aula Bezerra), por que 5 dimensões, por que IA precisa de método antes de ferramenta, como o app decide os pilotos.

**Camada 3 (opcional) — Roteiro de fala de 90 segundos**
Abertura da apresentação: "por que IA aplicada ao PPPM importa" — pode ficar em `docs/APRESENTACAO.md`.

**Camada 4 (futuro) — LLM opcional para refinar texto dos pilotos**
Variável `DIAG_IA_PPPM_USE_LLM=true` que, se ativa, chama LLM só para reescrever o campo "descricao" e "ganho_esperado" com vocabulário adaptado ao setor do participante. Caminho determinístico continua sendo o default.

---

## 7. Observações do primeiro teste real (2026-08-06)

**Caso testado:** João da Silva · Consultor · ConstruBase Engenharia · PME · 18 projetos · PMO ativo.
Diagnóstico: 4/3/3/2/2 = 14/30 → Nível 3 Experimental · Gargalo: Governança e HITL.

**PDF gerado:** 7 páginas, layout funcional. Nome: `Mapa_Inicial_IA-PPPM_joao-da-silva_20260806.pdf`.

### O que cada página entrega
- **P1 Capa** — nome + empresa + data, frase âncora "do diagnóstico à recomendação consultiva"
- **P2 Contexto** — tabela dos 6 campos, cabeçalho de proposta comercial
- **P3 Diagnóstico** — tabela + total + nível + leitura executiva que cita o gargalo pelo nome e prescreve próximo passo consultivo (replica slide 15 da aula)
- **P4 Mapa 5 Blocos** — os 5 blocos preenchidos como documento
- **P5-6 Pilotos** — 3 pilotos com scoring visual, pré-requisitos, ganho e tempo
- **P7 Próximos Passos** — 4 passos padrão (validar TI → escolher 1 piloto → definir métrica → checkpoint 60 dias)

### 2 cenários de uso na palestra
1. **Ao vivo:** aluno da sala descreve empresa dele, você preenche o app em 3 min, projeta o PDF gerado
2. **Seguro:** levar 2-3 PDFs pré-gerados de perfis diferentes (Experimental + Otimizado + Ausente) para mostrar variação

### Pontos de polimento pendentes (v1.1 — opcionais)
1. **Normalização de input do nome** — acentos digitados errado ("JOÀO" em vez de "JOÃO") passam intactos para o PDF. Avaliar se aplicar `.title()` ou deixar como o usuário digitou
2. **Slugificação do nome do arquivo** — funciona corretamente ("JOÀO DA SILVA" → `joao-da-silva`), sem ação necessária
3. **PageBreak entre pilotos** — o 3º piloto parte no meio (descrição na p.5, tabela na p.6). Se quiser cada piloto em uma página inteira, adicionar `PageBreak()` entre eles em `src/pdf_export.py`

---

## Créditos

- Método pedagógico: **Prof. Dr. José Bezerra** — BSBr
- Base normativa: **PMI Standard for AI in PPPM (2026)**
- Implementação e adaptação: **Geovane Virmecati** — Eixo Estratégico
