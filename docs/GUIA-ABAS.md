# Guia do usuário — as 10 abas do consultor-ia-pppm

Este documento é a referência oficial das abas do app. Publicado junto com o repositório para que qualquer aluno consulte sem depender de sessão.

## Panorama

| # | Aba | Aula | O que faz |
|---|---|---|---|
| 1 | Mapa PMBOK × IA × IA+PO | Aula 1 | Referência mestre dos 40 processos do PMBOK 8ª ed. cruzados com "IA só" e "IA + Pesquisa Operacional" |
| 2 | Contexto | Aula 1 | Cadastra o consultor/aluno e a empresa-alvo (nome, cargo, porte, nº de projetos, PMO ativo) |
| 3 | Diagnóstico | Aula 1 | Score de maturidade em 5 dimensões (Estratégia · Dados · Casos de uso · Governança · Benefícios) |
| 4 | Mapa 5 Blocos | Aula 1 | Preenche Contexto · Dor · Dados · Riscos · Valor para gerar recomendação |
| 5 | Pilotos Recomendados | Aula 1 | 3 pilotos sugeridos pelo motor determinístico, com KPI benchmark auditável e plano 30d |
| 6 | Exportar PDF | Aula 1 | Gera PDF de entrega para o cliente com tudo acima |
| 7 | Projetos | Aula 1 | CRUD SQLite — cadastra vários projetos, alterna entre eles, guarda o estado |
| 8 | Comparar | Aula 1 | Radar + heatmap Plotly cruzando projetos cadastrados (portfólio) |
| **9** | **Priorização (Aula 2)** | **Aula 2** | Score executivo 30/20/20/15/15 + matriz Impacto×Viabilidade + 5 erros embutidos + top 3 |
| **10** | **Governança + HITL (Aula 2)** | **Aula 2** | Checklist segurança + rastro 5 passos + nível HITL puxado do impacto |

## Aula 2 tem duas abas, não uma

- **Aba 9 · Priorização** — é a central. Prioriza casos e roda os 5 erros em tempo real no mesmo lugar (os 5 erros ficaram embutidos aqui, não é aba separada — evita ping-pong).
- **Aba 10 · Governança + HITL** — só faz sentido depois que o aluno priorizou. Puxa cada caso da aba 9 e aplica o filtro de governança + o princípio de ouro.

## Projetos-benchmark que vêm carregados na aba 7

Cadastrados intencionalmente como referência didática — o aluno vê o diagnóstico já preenchido de projetos exemplares para calibrar o próprio.

**1. Empresa Alfa (case Bezerra)** — o caso hipotético que o próprio Prof. Bezerra usa no slide 37 do deck oficial da Aula 2. Aparece pré-carregado também na aba 9 como seed de priorização.

**Os 5 vencedores do PMI Project of the Year Award** — o prêmio mais prestigiado da profissão de gerência de projetos no mundo. Um por ano, escolhido pelo PMI Institute entre milhares de submissões globais:

| Ano | Projeto | Contexto |
|---|---|---|
| **2024** | Pertamina — One Price Fuel Program | Estatal indonésia de energia. Uniformizou o preço do combustível em todo o arquipélago da Indonésia (17 mil ilhas), incluindo regiões remotas — desafio logístico e de política pública em escala continental. |
| **2023** | Caterpillar — Battery Electric 793 Mining Truck | Primeiro caminhão de mineração pesada (793 modelo, ~250 t) totalmente elétrico a bateria. Descarboniza mineração — setor historicamente resistente a eletrificação. |
| **2022** | CDL — Rapid Screening Consortium | Creative Destruction Lab (Canadá). Consórcio que criou protocolo de triagem rápida COVID-19 para retomada segura de eventos e trabalho presencial. Coordenou dezenas de empresas privadas em pandemia. |
| **2021** | US State Dept — FASTC Training Center | Centro de treinamento em segurança para diplomatas dos EUA. Projeto federal complexo (múltiplas agências) entregue no orçamento e prazo. |
| **2020** | TANAP — Trans Anatolian Natural Gas Pipeline | Gasoduto de 1.850 km cruzando a Turquia, conectando o gás do Cáspio à Europa. Executado por SOCAR (Azerbaijão) + BOTAS (Turquia). Um dos maiores projetos de energia da última década. |

**Por que estes 5:** são casos oficialmente reconhecidos como *excelência em gerência de projetos*. Servem para o aluno comparar dimensões (porte, complexidade, tipo de dor, maturidade de PPPM) contra o próprio projeto — sem ter que inventar exemplo. Ao clicar em cada um na aba 7, ele vê o diagnóstico completo preenchido e pode cruzar com o dele na aba 8 (Comparar → radar + heatmap).

## Como o aluno cadastra o próprio projeto

1. Aba **7. Projetos** → botão **"+ Novo projeto"** → dá um nome.
2. Alterna para as abas **2. Contexto** e **3. Diagnóstico** e preenche.
3. Salva o diagnóstico (fica atrelado ao projeto ativo).
4. Volta à aba **8. Comparar** para cruzar com os benchmarks PMI.
5. Para casos de uso de IA no projeto, vai à aba **9. Priorização (Aula 2)** e adiciona quantos casos quiser.
6. Depois vai à aba **10. Governança + HITL** para definir o nível de validação humana.

## Concorrência — múltiplos alunos ao mesmo tempo

- URL é a mesma para todos: `https://consultor-ia-pppm.streamlit.app`.
- Cada aba/navegador = uma sessão isolada (Streamlit `session_state`). Ninguém sobrescreve o trabalho do outro.
- Streamlit Community Cloud (grátis, 1 GB RAM): 20-30 alunos simultâneos tranquilamente. Sem limite de tempo de uso — o app fica no ar 24/7 sem custo.
