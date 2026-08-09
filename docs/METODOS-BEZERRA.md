# 5 Frameworks proprietários do Prof. Dr. José Bezerra

Extraídos da transcrição RAW da Aula 1 IA-PPPM (BSBr, 2026-08-08).
Ver `docs/FONTES-BEZERRA-AULA1-TRANSCRICAO-RAW.md` para timestamps exatos.

Estes 5 métodos são a **metodologia consultiva** que envelopa a **framework técnica** do PMI Standard for AI in PPPM (2026). Bezerra define claramente a distinção em [01:14:26]:

> "Framework é direção/orientação; Metodologia é receita de bolo passo-a-passo."

---

## 1. Regra dos 5 Porquês

**O que é:** técnica clássica de análise de causa-raiz. Diante de uma dor declarada pelo cliente, o consultor pergunta "por quê?" cinco vezes seguidas, cada resposta gerando a próxima pergunta. Ao fim, a causa raiz emerge.

**Quando usar:** primeira reunião de discovery, quando o cliente traz uma dor superficial (ex: "meus projetos atrasam"). Os 5 Porquês desmontam a superfície e chegam ao gargalo real (ex: "não temos governança de portfólio").

**Como aplicar no `consultor-ia-pppm`:** cada bloco de Dor do Mapa 5 Blocos deveria idealmente vir da aplicação dos 5 Porquês — o campo `mapa_dor` no formulário deve capturar a causa-raiz, não o sintoma.

**Citação:** Bezerra, Aula 1 IA-PPPM, BSBr, 2026-08-08 [02:34:23] e [03:56:10] — "não tem aquele negócio dos cinco porquês, ninguém escapa".

---

## 2. Lei de Pareto 80/20 aplicada à consultoria de IA

**O que é:** o princípio de Pareto (80% dos efeitos vêm de 20% das causas) aplicado ao portfólio de dores de um cliente. Bezerra formula assim:

> "20% dos casos recebem 80% dos problemas."

**Quando usar:** priorização de piloto. Depois de mapear 50 dores possíveis do cliente, identificar as 10 que concentram 80% do valor perdido. Dessas 10, escolher 1-3 como piloto de IA.

**Como aplicar no `consultor-ia-pppm`:** o algoritmo do `recomendador.py` já opera nesse espírito ao ranquear pilotos por scoring (impacto × viabilidade × risco). O que falta explicitar no UI: mostrar por que os 3 pilotos escolhidos representam ~80% do valor recuperável.

**Citação:** Bezerra, Aula 1 IA-PPPM, BSBr, 2026-08-08 [03:07:06].

---

## 3. Regra das 50 Dores → 5 → 1

**O que é:** metodologia estruturada de discovery. Fluxo em 3 passos:

1. **50 dores:** cliente lista tudo que dói, sem filtro.
2. **5 dores:** consultor filtra as 5 mais críticas por impacto e viabilidade.
3. **1 dor:** cliente escolhe entre as 5, o consultor ataca essa.

Blindagem: a decisão final é do cliente, não do consultor.

**Quando usar:** segunda reunião de discovery, depois dos 5 Porquês terem mapeado causas-raízes. Substitui listas soltas de "prioridades" por método reprodutível.

**Como aplicar no `consultor-ia-pppm`:** próxima versão do Mapa 5 Blocos deveria ter um campo `dores_candidatas` (lista de 5-10) e um `dor_escolhida` (a que vira piloto). Auditável e defensável.

**Citação:** Bezerra, Aula 1 IA-PPPM, BSBr, 2026-08-08 [03:56:10].

---

## 4. Método das 3 Opções (A/B/C)

**O que é:** o consultor nunca decide sozinho. Diante de qualquer decisão relevante, apresenta **três caminhos** (A, B, C) com trade-offs claros. O cliente escolhe. A decisão fica registrada por e-mail — protege o consultor de responsabilidade unilateral.

**Fluxo:**
1. Consultor apresenta A/B/C com prós, contras e recomendação própria (opcional).
2. Cliente escolhe uma opção.
3. Consultor envia e-mail: "Confirmo que você escolheu B. Vou executar assim."
4. Cliente responde confirmando.
5. Executa.

**Quando usar:** toda decisão que envolva risco reputacional, legal ou financeiro relevante. Também em decisões técnicas (qual LLM, qual métrica, qual threshold).

**Como aplicar no `consultor-ia-pppm`:** o passo `4. Pilotos Recomendados` já entrega 3 pilotos — reforça esse método. O usuário substitui pilotos via dropdown, materializando a escolha A/B/C.

**Citação:** Bezerra, Aula 1 IA-PPPM, BSBr, 2026-08-08 [03:50:18] a [03:52:23].

---

## 5. Framework vs. Metodologia

**O que é:** distinção operacional que o Bezerra usa para separar o padrão do PMI (framework) do método consultivo (metodologia).

- **Framework** = direção, orientação, princípios. Ex.: PMI Standard for AI in PPPM (2026).
- **Metodologia** = receita de bolo, passo-a-passo, executável. Ex.: as 4 metodologias acima (5 Porquês, Pareto, 50 Dores, 3 Opções).

**Consequência prática:** o consultor **usa** o framework do PMI mas **vende** a metodologia própria. O framework é público (qualquer um lê o Standard por US$ 85). A metodologia é o diferencial competitivo do consultor.

**Como aplicar no `consultor-ia-pppm`:** o app expõe o framework (5 dimensões, 5 blocos, princípios IA responsável) mas a metodologia consultiva do Geovane é o algoritmo de recomendação + o roteiro do PDF + a curadoria dos 12 pilotos. Nunca confundir os dois em pitch comercial.

**Citação:** Bezerra, Aula 1 IA-PPPM, BSBr, 2026-08-08 [01:14:26].

---

## Como combinar os 5 métodos numa consultoria de IA-PPPM

Sequência recomendada em cliente novo:

| Sessão | Método | Entrega |
|---|---|---|
| 1. Discovery inicial (60 min) | 5 Porquês | Causa-raiz da dor executiva |
| 2. Amplificação (90 min) | 50 Dores → 5 | Lista curta de dores prioritárias |
| 3. Priorização (60 min) | Pareto 80/20 | 1-3 pilotos candidatos |
| 4. Decisão executiva (30 min) | 3 Opções (A/B/C) | Escolha do sponsor + e-mail confirmando |
| 5. Execução (30 dias) | Plano projeto 30d + HITL | Piloto rodando, baseline + delta medidos |
| 6. Handover | Framework (PMI Standard) + Metodologia (Bezerra) | Runbook + governança + próximo ciclo |

Este é o **método Bezerra completo** — o app `consultor-ia-pppm` é o instrumento que operacionaliza esse método em ferramenta reproduzível.
