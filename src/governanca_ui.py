"""UI Streamlit da aba de Governança + HITL — Aula 2 IA-PPPM."""

from __future__ import annotations

import streamlit as st

from src import governanca, priorizacao, priorizacao_ui


STATE_RESP = "aula2_gov_respostas"
STATE_RASTRO = "aula2_gov_rastro"


def _ensure_state(casos: list[priorizacao.CasoDeUso]) -> None:
    if STATE_RESP not in st.session_state:
        st.session_state[STATE_RESP] = {
            c.id: {"dados_sensiveis": False, "acessos": False, "ambiente_seguro": False, "controle_uso": False}
            for c in casos
        }
    if STATE_RASTRO not in st.session_state:
        st.session_state[STATE_RASTRO] = {
            c.id: governanca.Rastro(caso_id=c.id) for c in casos
        }
    for c in casos:
        st.session_state[STATE_RESP].setdefault(
            c.id, {"dados_sensiveis": False, "acessos": False, "ambiente_seguro": False, "controle_uso": False}
        )
        st.session_state[STATE_RASTRO].setdefault(c.id, governanca.Rastro(caso_id=c.id))


def _bloco_principios(politica: dict) -> None:
    with st.expander("📖 Metodologia — Governança + HITL da Aula 2", expanded=False):
        st.markdown(
            f"""
**Princípio de ouro:** *{politica['principio_de_ouro']}* (slide 33).

**Segurança (slide 32) — 4 blocos:**
"""
        )
        for b in politica["seguranca"]["blocos"]:
            st.markdown(f"- **{b['titulo']}:** {b['regra']}")
        st.markdown("\n**Ética (slide 33) — riscos a evitar:**")
        for r in politica["etica"]["riscos"]:
            st.markdown(f"- {r}")
        st.markdown("\n**Rastreabilidade (slide 34) — 5 passos:** " + " → ".join(
            f["titulo"] for f in politica["rastreabilidade"]["fluxo"]
        ))
        st.markdown("\n**HITL (slide 35):**")
        for p in politica["hitl"]["papeis"]:
            st.markdown(f"- **{p['papel']}** — {p['responsabilidade']}")
        st.markdown("\n**Workflow de validação (slide 36):** " + " → ".join(
            politica["hitl"]["workflow_validacao"]
        ))


def _tabela_nivel_hitl(politica: dict) -> None:
    st.markdown("### 🎚️ Nível de HITL por impacto (princípio de ouro)")
    linhas = "\n".join(
        f"| {n['id'].capitalize()} | {n['impacto_min']}–{n['impacto_max']} | {n['aprovador']} | {n['descricao']} |"
        for n in politica["hitl"]["niveis"]
    )
    st.markdown(
        "| Nível | Score de impacto | Aprovador | Descrição |\n"
        "|---|---|---|---|\n" + linhas
    )


def _editor_governanca_por_caso(caso: priorizacao.CasoDeUso) -> None:
    resp = st.session_state[STATE_RESP][caso.id]
    rastro = st.session_state[STATE_RASTRO][caso.id]
    politica = governanca.carregar_politica()
    score_impacto = float(caso.notas.get("impacto", 0) or 0)
    nivel = governanca.nivel_hitl(score_impacto)

    with st.expander(f"**{caso.nome}** · `{caso.id}`", expanded=False):
        st.info(
            f"🎚️ **Nível HITL sugerido:** **{nivel['id'].capitalize()}** — {nivel['descricao']}  \n"
            f"Aprovador: {nivel['aprovador']}"
        )

        st.markdown("**Segurança — confirme cada bloco antes de escalar o piloto (slide 32):**")
        cols = st.columns(2)
        blocos = politica["seguranca"]["blocos"]
        for idx, b in enumerate(blocos):
            with cols[idx % 2]:
                resp[b["id"]] = st.checkbox(
                    f"**{b['titulo']}** — {b['regra']}",
                    value=resp.get(b["id"], False),
                    key=f"gov_{caso.id}_{b['id']}",
                )

        st.markdown("**Rastreabilidade — preencha o rastro do piloto (slide 34):**")
        rastro.entrada = st.text_input("1. Entrada — dados usados", rastro.entrada, key=f"ent_{caso.id}")
        rastro.processamento = st.text_input(
            "2. Processamento — prompt, modelo e regra", rastro.processamento, key=f"pro_{caso.id}"
        )
        rastro.saida = st.text_input("3. Saída — recomendação gerada", rastro.saida, key=f"sai_{caso.id}")
        rastro.validacao = st.text_input(
            "4. Validação — humano aprova ou ajusta", rastro.validacao, key=f"val_{caso.id}"
        )
        rastro.registro = st.text_input(
            "5. Registro — decisão e evidência", rastro.registro, key=f"reg_{caso.id}"
        )

        diag = governanca.prontidao_governanca(resp, rastro)
        if diag["pronto"]:
            st.success("✅ Governança pronta para escalar este piloto.")
        else:
            msgs = []
            if not diag["seguranca_ok"]:
                msgs.append(f"Segurança faltando: {', '.join(diag['seguranca_faltando'])}")
            if not diag["rastro_ok"]:
                msgs.append(f"Rastro faltando: {', '.join(diag['rastro_faltando'])}")
            st.warning("⚠️ Ainda não pronto. " + " · ".join(msgs))


def render() -> None:
    politica = governanca.carregar_politica()
    st.subheader("10. Governança + HITL — Aula 2")
    st.caption(
        "*Sem governança, a IA escala problemas. Com governança, a IA escala valor.* "
        "— Prof. Dr. José Bezerra, Aula 2 IA-PPPM (BSBr, 2026-08-17)"
    )

    _bloco_principios(politica)
    _tabela_nivel_hitl(politica)

    casos = st.session_state.get(priorizacao_ui.STATE_KEY, [])
    if not casos:
        st.info("Vá primeiro à aba **9. Priorização (Aula 2)** para cadastrar/ajustar seus casos de uso.")
        return

    _ensure_state(casos)

    st.markdown("### Governança por caso")
    st.caption("Cada caso puxa o próprio nível de HITL a partir da nota de Impacto definida na aba anterior.")
    for caso in casos:
        _editor_governanca_por_caso(caso)

    st.markdown("---")
    st.markdown("### 📊 Prontidão agregada")
    pronto = 0
    for caso in casos:
        resp = st.session_state[STATE_RESP][caso.id]
        rastro = st.session_state[STATE_RASTRO][caso.id]
        if governanca.prontidao_governanca(resp, rastro)["pronto"]:
            pronto += 1
    total = len(casos)
    c1, c2 = st.columns(2)
    c1.metric("Casos com governança pronta", f"{pronto}/{total}")
    c2.metric("Casos pendentes", f"{total - pronto}/{total}", delta_color="inverse")
