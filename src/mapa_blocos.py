import streamlit as st

from src.validators import validar_mapa

_BLOCOS = [
    (
        "contexto",
        "1. Contexto",
        "Qual projeto, processo, PMO ou área será analisado?",
        "Ex: Programa de Excelência Operacional do PMO — projetos de atendimento, faturamento, SLA e indicadores executivos.",
    ),
    (
        "dor",
        "2. Dor",
        "Qual dor real precisa ser resolvida?",
        "Ex: Baixa previsibilidade, atrasos recorrentes, retrabalho e decisões baseadas em planilhas conflitantes.",
    ),
    (
        "dados",
        "3. Dados",
        "Dados que já existem",
        "Ex: Cronogramas, status reports, atas, tickets, SLA, faturamento, BI financeiro e histórico de riscos.",
    ),
    (
        "riscos",
        "4. Riscos",
        "Que riscos, restrições e limites de governança precisam ser respeitados?",
        "Ex: Dados sensíveis, LGPD, vieses, alucinação, decisões sem validação humana, resistência das equipes.",
    ),
    (
        "valor",
        "5. Valor",
        "Que valor executivo pode ser gerado?",
        "Ex: Reduzir atrasos, recuperar receita, melhorar SLA, priorizar ações e fortalecer a governança executiva.",
    ),
]

_MIN_CHARS = 30


def render() -> None:
    st.subheader("3. Mapa 5 Blocos")
    st.caption(
        "Estruture a demanda em cinco blocos. Cada bloco precisa ter pelo menos "
        f"{_MIN_CHARS} caracteres para liberar a próxima etapa."
    )

    mapa = st.session_state["mapa"]

    for key, rotulo, pergunta, placeholder in _BLOCOS:
        st.markdown(f"**{rotulo} — {pergunta}**")
        mapa[key] = st.text_area(
            rotulo,
            value=mapa.get(key, ""),
            placeholder=placeholder,
            label_visibility="collapsed",
            height=110,
            key=f"mapa_{key}",
        )
        chars = len((mapa.get(key) or "").strip())
        cor = "green" if chars >= _MIN_CHARS else "gray"
        st.markdown(f"<small style='color:{cor}'>{chars} caracteres</small>", unsafe_allow_html=True)

    if st.button("Salvar mapa", type="primary"):
        ok, erros = validar_mapa(mapa)
        if ok:
            st.session_state["mapa_salvo"] = True
            st.success("Mapa salvo. Avance para os Pilotos Recomendados.")
        else:
            st.session_state["mapa_salvo"] = False
            for e in erros:
                st.error(e)
