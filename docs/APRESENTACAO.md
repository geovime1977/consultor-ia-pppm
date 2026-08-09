# Apresentação — Como o consultor-ia-pppm foi feito

Material de apoio para Geovane Virmecati apresentar o app na palestra "Formação de Consultores em IA aplicada ao PPPM" do Prof. Dr. José Bezerra (BSBr).

Objetivo: mostrar aos alunos que o app **não é só sobre IA — foi feito COM IA**, e o próprio processo de construção é um caso vivo do método que a aula ensina.

---

## O que é o consultor-ia-pppm (30 segundos de fala)

Um mini-app que transforma o método da Aula 1 do Prof. Bezerra em ferramenta usável em 5 minutos. O aluno responde o diagnóstico de maturidade (5 dimensões × 0-6), preenche o Mapa 5 Blocos (Contexto, Dor, Dados, Riscos, Valor) e recebe um PDF com 3 pilotos priorizados. Roda no notebook, funciona offline, sem custo por uso.

**Não substitui a aula.** Materializa o que ela ensina.

---

## Como foi construído — o processo real (5 minutos de fala)

Tudo aqui é reproduzível. Nenhuma etapa foi milagre.

### Etapa 1 — Entender a aula
Li o PDF da Aula 1 (22 slides) do começo ao fim antes de escrever qualquer linha. Extraí:
- O método pedagógico (5 blocos + 5 dimensões + 5 níveis)
- O caso Empresa Alfa como referência de aplicação
- O vocabulário do professor (para o app "falar a mesma língua")

### Etapa 2 — Especificar antes de codar
Rodei o pipeline `/meu-pipeline --tipo app`. Isso obrigou o processo a passar por:
1. **Backlog** — priorização vs. outras demandas
2. **Triagem** — classificação (novo projeto, tipo app, Área AIIA "Projetos & PMO")
3. **Especificação** — o que exatamente será construído
4. **Arquitetura** — estrutura de pastas, módulos, schemas JSON, regra determinística de priorização, layout do PDF (documento `ARQUITETURA.md` de 17 KB antes de escrever código)
5. **Construção** — implementação seguindo a arquitetura
6. **Validação** — 28 testes automatizados
7. **Deploy** — GitHub privado + backup OneDrive
8. **Documentação** — 2 tutoriais (usuário + técnico) + FAQ + esta apresentação

### Etapa 3 — Delegar para agentes especializados
Não fiz tudo sozinho. Deleguei para agentes com papéis específicos:
- **`agente-architect`** — desenhou a arquitetura
- **`agente-builder`** — implementou o código (24 arquivos)
- **`vault-writer`** — registrou no meu segundo cérebro (Obsidian)
- **`obsidian-librarian`** — validou o registro

Cada agente teve **uma responsabilidade única**. Nenhum sabia o que o outro estava fazendo. Isso é **arquitetura de decisão** — não é IA fazendo tudo, é IA fazendo cada coisa no lugar certo, com validação humana entre etapas (HITL).

### Etapa 4 — Regra crítica: zero LLM em produção
Aqui está o ponto que vale a discussão da palestra: **o app em si NÃO usa IA para decidir**. O recomendador de pilotos é 100% determinístico — regra matemática, transparente, auditável, gratuita por execução.

**Por que essa escolha?** Porque a aula ensina que IA sem governança vira ferramenta. O app precisa ser **explicável** para servir de exemplo do método. Se cada execução fizesse uma chamada LLM que muda de resposta, ele seria caixa-preta — exatamente o oposto do que o professor quer formar.

**IA foi usada NA construção. Não na operação.**

---

## O que foi usado — stack completa

| Categoria | Ferramenta | Papel |
|---|---|---|
| **Modelo de IA** | Claude Opus 4.7 (Anthropic) | Escrita de código, arquitetura, documentação |
| **Interface** | Claude Code (CLI da Anthropic) | Ambiente onde o modelo executou tarefas |
| **Orquestração** | Pipeline `/meu-pipeline` (custom) | Sequência backlog → spec → build → deploy |
| **Agentes especializados** | 4 agentes customizados | architect, builder, vault-writer, librarian |
| **Linguagem** | Python 3.14 | Runtime do app |
| **UI** | Streamlit 1.40 | Interface web local |
| **PDF** | ReportLab 4.2 | Geração do entregável |
| **Testes** | pytest | 28 testes automatizados |
| **Versionamento** | Git + GitHub privado | Rastreabilidade |
| **Backup** | rclone → OneDrive | Segurança |
| **Método pedagógico** | PMI Standard for AI in PPPM (2026) + Aula 1 Prof. Bezerra | Base normativa |

---

## Por que fazer COM IA é a mensagem — a camada meta (2 minutos de fala)

Aqui está o ponto que **transforma o app em argumento consultivo**.

A aula prega 3 coisas centrais:
1. **IA sem método vira ferramenta. IA com método vira valor.** (slide 22)
2. **O gargalo não é acesso à IA. É governança e validação humana.** (slide 15)
3. **Diagnóstico bom não vende ferramenta. Revela oportunidade.** (slide 12)

Este app é essas 3 frases materializadas. Olha:

**Sobre "IA com método":** o app não foi feito jogando prompt aleatório para o Claude e copiando saída. Passou por pipeline formal com 8 etapas, arquitetura documentada em 17 KB de markdown antes da primeira linha de código, e 28 testes automatizados para garantir que nenhuma alteração futura quebra a regra determinística. **Isso é método.**

**Sobre "governança e HITL":** cada agente teve escopo restrito e retorno para revisão humana antes da próxima etapa. O commit final foi feito com validação. O código do recomendador é inspecionável linha a linha. Se algum piloto sair errado, dá para debugar sem precisar "perguntar para a IA". **Isso é HITL de verdade.**

**Sobre "diagnóstico revela oportunidade":** o app existe porque, quando li o PDF da aula, notei que o professor **deliberadamente deixou espaço** para as próximas aulas (slide 22 diz: "cada encontro vai aprofundar uma etapa"). O que eu fiz foi **respeitar esse espaço** e agregar exatamente onde não invade. **Isso é postura consultiva** — enxergar o que o cliente ainda não sabe que precisa.

**Provocação para a sala:** *"Se eu usasse LLM em produção neste app, ele seria mais 'inteligente' — e menos consultivo. Menos rastreável. Menos vendável para diretoria que precisa de auditoria. Por isso a v1 é 100% determinística. IA foi usada onde faz sentido: na construção. Não na operação."*

---

## Números do projeto (tenha na ponta da língua)

| Métrica | Valor |
|---|---|
| Tempo total (do "sim, começa" ao PDF funcionando) | ~1 hora |
| Arquivos de código Python | 12 |
| Arquivos de dados (JSON) | 3 |
| Testes automatizados | 28 (100% verdes) |
| Documentos técnicos | 4 (arquitetura, tutorial usuário, tutorial técnico, FAQ) |
| Catálogo de pilotos | 12 |
| Dimensões do diagnóstico | 5 |
| Níveis de maturidade | 5 |
| Categorias de dor mapeadas | 15 |
| Chamadas de IA em produção (por execução do app) | **0** |
| Custo por execução do app | **R$ 0** |
| Onde está | GitHub privado + OneDrive + local |

---

## Roteiro de fala — 3 minutos (você abre a apresentação com isso)

*"Professor, colegas — o que vocês vão ver aqui em 3 minutos não é um app sobre IA. É um app que virou o método da Aula 1 em ferramenta. E foi construído com IA — mas construído do jeito certo, com o método que o professor está ensinando.*

*Antes de escrever qualquer código, eu li o PDF da aula inteiro. Depois passei por um pipeline formal: backlog, arquitetura, construção, testes, deploy. Deleguei tarefas específicas para agentes especializados, cada um com escopo restrito. E tomei uma decisão contraintuitiva: **o app em si não usa IA para decidir**. É 100% determinístico.*

*Por quê? Porque a aula ensina que IA sem governança vira ferramenta. Se cada execução do app chamasse um LLM, ele seria caixa-preta — o oposto do consultor que este curso está formando. Então IA foi usada na construção — código, arquitetura, testes, documentação. Mas na operação, cada aluno recebe uma resposta rastreável, gratuita e auditável.*

*O app funciona assim: você responde 5 sliders do diagnóstico, escreve 5 blocos de dor, e recebe um PDF com 3 pilotos priorizados. É o mesmo método da Empresa Alfa que o professor mostrou, mas com seus dados e seu contexto. Bora ver rodando."*

---

## Créditos e transparência

- **Método pedagógico:** Prof. Dr. José Bezerra — BSBr
- **Base normativa:** PMI Standard for AI in PPPM (2026)
- **Construção do app:** Geovane Virmecati (Eixo Estratégico) com Claude Opus 4.7 via Claude Code
- **Pipeline de execução:** `/meu-pipeline --tipo app` — orquestração custom com agentes especializados
- **Repositório:** https://github.com/geovime1977/consultor-ia-pppm (privado)
- **Nenhum dado real de aluno foi usado no desenvolvimento.** O caso "João da Silva / ConstruBase Engenharia" é fictício, criado para demonstração.
