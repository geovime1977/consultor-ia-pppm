# Tutorial do Usuário — consultor-ia-pppm

App simples que ajuda você a sair de "quero usar IA em projetos" e chegar em um **plano concreto com 3 pilotos priorizados** em cerca de 10 minutos.

Baseado no método da Aula 1 do Prof. Dr. José Bezerra (BSBr) — "Formação de Consultores em IA aplicada ao PPPM".

---

## O que o app entrega

Ao final você recebe um PDF chamado **"Mapa Inicial de Oportunidades de IA-PPPM"** com:

1. Seus dados de contexto (nome, empresa, cargo)
2. Sua pontuação de maturidade em IA-PPPM (0–30) e o nível resultante
3. O Mapa 5 Blocos (Contexto · Dor · Dados · Riscos · Valor)
4. 3 pilotos recomendados com scoring de Impacto, Viabilidade e Risco
5. Próximos passos sugeridos

Você leva o PDF para a diretoria, para o cliente ou para a próxima reunião do PMO.

---

## Como instalar

Precisa ter Python 3.10 ou mais recente instalado.

```bash
cd ~/projetos/consultor-ia-pppm
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Pronto. Instalação demora ~30 segundos.

---

## Como usar

### Passo 1 — Abrir o app

```bash
cd ~/projetos/consultor-ia-pppm
.venv/bin/streamlit run app.py --server.port 8512
```

O navegador abre em `http://localhost:8512`.

### Passo 2 — Preencher as 5 abas em ordem

**Aba 1 — Contexto**
Preencha nome, empresa, porte, número de projetos ativos, se tem PMO e seu cargo. Clique em "Salvar contexto".

**Aba 2 — Diagnóstico**
5 sliders de 0 a 6 pontos cada:
- Estratégia e valor
- Dados e processos
- Casos de uso
- Governança e HITL (Human-in-the-Loop)
- Benefícios e ROI

O app mostra em tempo real o total (0–30) e o nível resultante (1 Ausente a 5 Otimizado).

**Aba 3 — Mapa 5 Blocos**
Escreva livremente sobre:
- **Contexto** — situação do projeto ou área
- **Dor** — problema real a resolver
- **Dados** — o que já existe (planilhas, sistemas, atas)
- **Riscos** — LGPD, viés, resistência, alucinação
- **Valor** — o que espera ganhar

Mínimo de 30 caracteres por campo. Clique em "Salvar mapa".

**Aba 4 — Pilotos Recomendados**
O app processa suas respostas e mostra 3 pilotos ranqueados. Cada card traz:
- Nome + descrição
- Impacto / Viabilidade / Risco (alto/médio/baixo)
- Pré-requisitos
- Ganho esperado
- Tempo estimado em semanas

Você pode trocar manualmente um dos pilotos por outro do catálogo se preferir.

**Aba 5 — Exportar PDF**
Confira o preview. Clique em "Gerar PDF" e depois em "Download" para baixar.
Nome do arquivo: `Mapa_Inicial_IA-PPPM_<seu-nome>_<data>.pdf`.

### Passo 3 — Usar o resultado

Leve o PDF para:
- Reunião com o cliente (proposta consultiva)
- Reunião com o PMO (priorização de pilotos)
- Reunião com a diretoria (business case inicial)

---

## Se der erro

**"streamlit: command not found"** — você não ativou o venv. Rode com `.venv/bin/streamlit` no caminho completo, não só `streamlit`.

**"Address already in use" na porta 8512** — outro app já está usando. Troque a porta: `--server.port 8512`.

**Botão "Salvar mapa" não habilita** — algum bloco tem menos de 30 caracteres. Preencha melhor.

**PDF sai em branco ou sem 3 pilotos** — você pulou a aba 4. Volte, entre nela, e só depois vá para a aba 5.

**Quer mudar os pilotos ofertados** — abra `data/pilotos.json` em qualquer editor de texto e edite o catálogo. Formato JSON (documentado em `docs/ARQUITETURA.md`).

---

## Suporte

- Autor: Geovane Virmecati — Eixo Estratégico
- Método pedagógico: Prof. Dr. José Bezerra — BSBr
- Base normativa: PMI Standard for AI in PPPM (2026)
