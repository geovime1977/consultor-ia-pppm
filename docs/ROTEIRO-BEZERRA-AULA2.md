# Roteiro — Apresentação ao Prof. Dr. José Bezerra

**Formato:** reunião 1:1 (Zoom/Meet), 7–8 min, com demo ao vivo do app.
**Objetivo:** validar que a extensão Aula 2 do `consultor-ia-pppm` respeita o método que o senhor ensinou, e obter sinal verde para levar aos alunos em palestra.
**Preparação:** app rodando em `https://consultor-ia-pppm-qyhmm8jymmjnsv6bauodz4.streamlit.app/` (ou `http://localhost:8512` local).

---

## Bloco 1 · Abertura (30 s)

> "Prof., queria mostrar rapidinho o que fiz esses dias em cima do material da Aula 2 — o app que o senhor viu na Aula 1 evoluiu e agora carrega o método completo da segunda aula. São 7 minutos. Depois queria pedir dois retornos: se o modelo respeita a sua doutrina, e se autoriza a gente rodar isso numa aula ao vivo para a turma."

---

## Bloco 2 · Contexto rápido (1 min)

- O app original é o `diag-ia-pppm` que apresentei na Aula 1 (aquele com o mapa 5 blocos, diagnóstico de maturidade e 3 pilotos recomendados).
- Fiz um fork chamado `consultor-ia-pppm` para não mexer no que o senhor viu. O fork é onde entra tudo que o senhor ensina depois da Aula 1.
- Depois da Aula 2, adicionei três módulos novos, cada um mapeado 1:1 com os slides do seu deck.

---

## Bloco 3 · O que a Aula 2 acrescentou (2 min)

Três módulos determinísticos, sem LLM, mantendo a filosofia do app:

1. **Priorização de Casos de Uso** — implementa o "Score executivo" do slide 30 com os pesos exatos que o senhor definiu: Impacto 30%, Viabilidade 20%, Dados 20%, Risco 15%, Valor 15%. Ranking em três faixas — Fazer agora / Preparar / Não priorizar. E o **corte obrigatório do slide 30**: sem dono humano identificado, o caso sai da fila mesmo com score alto.
2. **Validador dos 5 Erros** — cada um dos erros dos slides 8 a 12 virou uma regra que roda contra o caso enquanto o aluno digita. Se o aluno cita ferramenta antes de descrever a dor, aparece o alerta E1. Se esquece de definir dono, aparece o E4 (que também é o corte da priorização, fecha o ciclo).
3. **Governança + HITL** — traduz os slides 31 a 36: os 4 blocos de segurança viram checkboxes, o rastro de 5 passos (entrada → processamento → saída → validação → registro) vira formulário, e o **princípio de ouro** ("quanto maior o impacto, maior a validação humana") vira uma função que puxa o nível HITL — leve / moderada / alta — automaticamente da nota de impacto que o aluno deu na aba anterior.

Toda linguagem do app cita o slide de origem. Nada foi inventado — só operacionalizado.

---

## Bloco 4 · Demo ao vivo (3–4 min)

Abrir `https://consultor-ia-pppm-qyhmm8jymmjnsv6bauodz4.streamlit.app/`.

### Demo 1 — Aba 9 · Priorização (~90 s)

- Abrir a aba **"9. Priorização (Aula 2)"**. Já vem carregada com a Empresa Alfa do slide 37 do seu deck (os 4 casos: relatório executivo, análise preditiva, priorização de portfólio, chatbot de metodologia).
- Expandir o **Caso A** (relatório executivo) — mostrar os campos: dor, dados, decisão, dono, métrica, e os 5 sliders.
- Rolar até a **tabela colorida** — verde para Fazer agora, amarelo para Preparar, vermelho para Não priorizar.
- Mostrar a **matriz Impacto × Viabilidade** em Plotly — pontos coloridos por ranking, linhas de corte em 3.5.
- Rolar até **Top 3 selecionados** — o entregável literal da Aula 2: "o aluno sai com três casos priorizados".

### Demo 2 — Corte obrigatório em ação (~30 s)

- Expandir o **Caso D** (chatbot de metodologia). O senhor vai ver que ele veio **sem dono definido** de propósito.
- Mostrar o alerta E4 aparecendo em vermelho — *"Nenhum humano identificado como dono da decisão. IA recomenda. O humano valida e decide."*
- Voltar ao Top 3: ele ficou de fora mesmo se a gente atribuir nota máxima. Este é o corte que o senhor ensinou no slide 30.

### Demo 3 — Aba 10 · Governança + HITL (~90 s)

- Abrir a aba **"10. Governança + HITL (Aula 2)"**.
- Expandir o **Caso B** (análise preditiva de atrasos) — mostrar que o **nível HITL sugerido** foi puxado da nota de impacto que a gente deu na aba anterior. Impacto alto → HITL alta → aprovador é Especialista + Gestor.
- Marcar os 4 checkboxes de segurança + preencher rapidamente os 5 passos do rastro → o status muda para **"Governança pronta para escalar este piloto"**.

---

## Bloco 5 · Pergunta chave (30 s)

> "Prof., duas perguntas objetivas:
> 1. O modelo respeita a doutrina do seu deck ou tem algum ajuste que o senhor faria antes de eu levar isso para a turma?
> 2. Autoriza a gente rodar uma palestra de 30–45 min com os alunos, mostrando o app e convidando eles a jogar o próprio caso real deles dentro? Fico com o crédito de aluno da Aula 2, e o senhor com o crédito de método."

---

## Bloco 6 · Próximo passo se ele autorizar (30 s)

> "Perfeito. Combino três coisas:
> 1. Deixo a URL pública do app para os alunos usarem depois da palestra: `https://consultor-ia-pppm-qyhmm8jymmjnsv6bauodz4.streamlit.app/`.
> 2. Envio antes o roteiro dos slides da palestra para o senhor validar.
> 3. Publico o app no folder do Drive da turma junto com o PPTX da palestra e a instrução de uso."

---

## Anexos que já tenho para levar impressos ou compartilhar tela

- Este roteiro (também no repo em `docs/ROTEIRO-BEZERRA-AULA2.md`)
- Repo: `https://github.com/geovime1977/consultor-ia-pppm`
- Suíte de testes: 99/99 verdes (48 baseline Aula 1 + 51 novos Aula 2)
- Commits que consolidam: `9c6a21b` (código) + `a075059` (docs de deploy)

## Se ele perguntar algo técnico — respostas prontas

- **"Isso usa LLM por trás?"** → Não. 100% determinístico, mesma linha do que o senhor viu na Aula 1. Todo score é aritmético e todo alerta é regra explícita.
- **"E se eu quiser mudar os pesos?"** → Ficam num JSON isolado (`data/criterios_priorizacao.json`). Trocar o peso é editar 5 números — o app relê a cada refresh.
- **"E se eu quiser adicionar um sexto critério?"** → Adiciono no JSON e no dicionário `CRITERIO_IDS`. Levaria uns 20 min.
- **"Os dados dos alunos ficam salvos?"** → Só na sessão do navegador de cada aluno (session_state do Streamlit). Nada persiste no servidor.
- **"E o corte obrigatório do 'dono'?"** → Aplicado em dois lugares independentes: a Priorização força ranking "Não priorizar" e o Validador dispara alerta E4 crítico. Mesmo se um for burlado, o outro pega.
