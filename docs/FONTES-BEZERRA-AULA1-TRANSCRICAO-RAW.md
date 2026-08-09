# Fontes primárias — transcrição RAW da Aula 1 IA-PPPM (BSBr, 2026-08-08)

Extração cirúrgica da transcrição RAW (99 páginas, 258 min).
Fonte: `~/Downloads/Aula 1_ Formação de Consultores em IA Aplicada ao PPPM.pdf`

## 1. Números novos (não estavam no resumo curto)

| Item | Valor | Timestamp |
|---|---|---|
| Recuperação de faturamento SUS (case contabilidade) | R$ 5 milhões | [01:33] |
| Aumento de velocidade de atendimento com IA | 80% | [03:18:25] |
| Antecipação de aditivo pelo Radar de Riscos | 30 dias | [02:38:51] |
| Redução de atraso (Geovane reafirma) | 25% | [02:38:51] |
| Aula 1 futura — ticket próxima turma | R$ 10.000/aluno | [01:23:04] |
| Guia PMI Standard PDF | R$ 85 | [01:13:17] |
| MBA em PPPM BSBr | R$ 22.000 | [58:46] |
| Grupo empresarial recomendado ao filho | R$ 18.000 | [01:05:29] |
| Startup Mac Funny (Felipe) — valuation | R$ 10M implícito (10% por R$ 1M) | [01:06:41] |
| Escala micro-consultoria de sites com IA | R$ 200-1.000/site × 10/dia = R$ 30k/mês | [03:18:25] |
| Caso Marielle Franco — volume de documentos analisados | 8.000 | [03:41:29] |
| Caso viés de IA em contratação | 80% homens / 20% mulheres | [01:30:27] |
| Produtividade EUA vs Brasil | 5x mais | [01:18:27] |
| Corte de "achado" (padrão de dado ouro) | 90% de eficiência | [03:13:14] |
| SLA típico de e-mail | 3 horas | [02:55:14] |

## 2. Casos concretos além da Empresa Alfa (fictícia)

| Caso | Setor / Porte | Dor / Intervenção |
|---|---|---|
| Consultoria SUS (contabilidade) | Contábil PME | Cliente recuperou R$ 5M não cobrados; demitiu contador |
| Autarquia Trânsito Fortaleza (Detran) | Público estadual | Bezerra foi diretor 1 ano; cada depto com sua planilha; forçou CRM via presidência |
| Fujita (construtora Estrela) | Construção | Consultoria antiga logística/materiais |
| Secretaria Saúde Estado (Irismar) | Público saúde | Reestruturação estoque/almoxarifado, 1 ano |
| Aluno Boston | Serviço migrante | Faz sites para brasileiros em Boston |
| Oficina mecânica (Felipe) | PME serviço | IA localiza oficinas sem site → gera + WhatsApp/e-mail |
| Empreendimento imobiliário Aquiraz-CE | MCMV | 20 aptos com 2 sócios; planejam 46 via Caixa |
| Lions Club | Voluntariado | IA gerou template de projeto aprovado antes; virou coordenador |
| Empresa 11 mil funcionários | Corporativa | Viés de gênero em contratação — governança IA obrigatória |
| Governo Alagoas | Público | Engenheiros/médicos viram auditores por salário |

## 3. Citações-copy (frases fortes para reuso comercial)

- "**Dado é ouro**" [01:01:56]
- "**Resultado é rei**" [01:01:56, 01:34:01]
- "**Quem não mede não gerencia**" [03:10:36]
- "**Uma boa ideia implementada vale muito; uma boa ideia não implementada vale zero**" [03:00:24]
- "**O que separa as mulheres das meninas são os métodos; o que separa os homens dos meninos são as métricas**" [02:46:02]
- "**Sucesso é preparação mais oportunidade**" [37:00, 58:01]
- "**Ninguém faz nada sozinho**" [07:00, repetida]
- "**Neto vale mais do que dinheiro**" [08:30]
- "**Quanto mais você compartilha, mais você recebe — a Bíblia diz que volta no mínimo 100 vezes**" [01:25:54]

## 4. Modelo comercial (números do Bezerra)

- **Ticket próxima turma do curso:** R$ 10.000/aluno [01:23:04]
- **Cobrança por resultado:** "Percentual da recuperação" (% do que o cliente ganhar — sem % fechado)
- **Diagnóstico inicial:** gratuito, porta de entrada [48:47]
- **Consultoria presencial vs remota:** presencial ~5x mais cara [14:58]
- **Micro-produto IA (site com IA):** R$ 200-1.000/site, escala R$ 30k/mês [03:18:25]
- **MBA BSBr:** R$ 22k [58:46]

## 5. Ferramentas específicas por caso de uso

| Uso | Ferramenta |
|---|---|
| Documentação de projeto | Claude Code + Python |
| Site PME | Automação IA (sem fornecedor citado) |
| PowerPoint → HTML | ChatGPT direto |
| Cronograma / caminho crítico | Substitui MS Project |
| Análise de riscos | App em desenvolvimento (Felipe) |
| Automação genérica | RPA |
| Visualização PMO | Power BI |
| Stacks de referência | Azure MS, Google, AWS |
| MVP demonstrado (Geovane) | Streamlit + Python |

## 6. Correções ao resumo Quick Prompts (âncoras validadas)

| Item | Resumo diz | RAW diz | Ação |
|---|---|---|---|
| Status executivo | "~70%" | "70%" exato [02:39:47] | Manter |
| SLA | "15-25%" | "15 a 25%" [02:38:51] | Manter |
| Aditivo | "antecipação" | "antecipar em 30 dias" [02:38:51] | **CORRIGIR** — adicionar prazo |
| Escala maturidade R4 slide 26 | "0-3" | Bezerra usa **0-6** [52:10, 02:30:30]; R4 truncou | **PROJETO ESTÁ CORRETO (0-6)** |
| Aumento velocidade | não citado no resumo | 80% [03:18:25] | **ADICIONAR ao piloto SLA** |

## 7. Frameworks/matrizes NOVOS (não estavam no R4 nem no resumo)

1. **5 Porquês** [02:34:23, 03:56:10] — método explícito de root cause. "Ninguém escapa dos 5 porquês."
2. **Pareto 80/20 aplicado** [03:07:06] — "20% dos casos recebem 80% dos problemas". Justifica priorização de piloto.
3. **Regra das "50 dores"** [03:56:10] — cliente lista 50, consultor filtra 5 mais importantes, cliente escolhe 1, ataca essa.
4. **Método das 3 opções (A/B/C)** [03:50:18-03:52:23] — consultor sempre apresenta 3 caminhos, cliente escolhe, decisão registrada por e-mail. Protege consultor de responsabilidade unilateral.
5. **Framework vs Metodologia** [01:14:26] — Framework é direção/orientação (PMI Standard); Metodologia é receita de bolo passo-a-passo (do consultor).

## 8. Perguntas de alunos com respostas úteis

- **Cristiane** [02:51:43]: "O que é SLA?" → definição: Service Level Agreement (prazo, disponibilidade, responsabilidades, penalidades)
- **Márcio** [01:54:36]: "Ferramentas IA + Python que Geovane usou?" → "agentes de IA + Python + Streamlit + acesso local"
- **Giancarlo** [02:48:54]: crítica ao MVP — sugere adicionar EAP/WBS macro + plano de projeto + cronograma de 30 dias por piloto. **Bezerra pediu incorporar essa sugestão.**
- **Cristiane** [01:29:28]: "Consultor tira o emprego?" → Bezerra: "insegurança e burrice; média gerência barra crescimento porque não quer se capacitar"
- **Aline** [01:55:37]: "Uso IA só em básico" → Bezerra: "melhor começar pelo básico"

## Recomendações de uso desta fonte

- Todo número citado como âncora comercial deve trazer timestamp entre colchetes.
- Frases-copy do bloco 3 podem ir para header do app, PDF e proposta comercial — sem parafrasear.
- Casos reais do bloco 2 servem de storytelling em pitch (trocar nome se cliente pediu sigilo).
- Frameworks do bloco 7 são a metodologia proprietária do Bezerra — usar com atribuição.
- Sugestão do Giancarlo (bloco 8) é **backlog explícito** para o `diag-ia-pppm`.
