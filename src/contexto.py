import streamlit as st

from src.validators import validar_contexto

_PORTES = ["PME", "Média", "Grande", "Governo"]


def render() -> None:
    st.subheader("1. Contexto do participante")
    st.caption("Antes da solução, o diagnóstico. Comece pelo contexto do participante e da empresa.")

    ctx = st.session_state["contexto"]

    col1, col2 = st.columns(2)
    with col1:
        ctx["nome"] = st.text_input("Nome do participante", value=ctx.get("nome", ""))
        ctx["cargo"] = st.text_input(
            "Cargo do participante",
            value=ctx.get("cargo", ""),
            placeholder="ex: Gerente de PMO, Diretor de Projetos, Consultor",
        )
        ctx["empresa"] = st.text_input("Empresa", value=ctx.get("empresa", ""))
    with col2:
        porte_atual = ctx.get("porte") if ctx.get("porte") in _PORTES else _PORTES[0]
        ctx["porte"] = st.selectbox("Porte da empresa", _PORTES, index=_PORTES.index(porte_atual))
        ctx["n_projetos"] = st.number_input(
            "Nº de projetos ativos",
            min_value=0,
            step=1,
            value=int(ctx.get("n_projetos", 0) or 0),
        )
        ctx["pmo_ativo"] = st.radio(
            "PMO ativo?",
            options=[True, False],
            format_func=lambda v: "Sim" if v else "Não",
            index=0 if ctx.get("pmo_ativo") else 1,
            horizontal=True,
        )

    if st.button("Salvar contexto", type="primary"):
        ok, erros = validar_contexto(ctx)
        if ok:
            st.session_state["contexto_salvo"] = True
            st.success("Contexto salvo. Avance para o Diagnóstico.")
        else:
            st.session_state["contexto_salvo"] = False
            for e in erros:
                st.error(e)
