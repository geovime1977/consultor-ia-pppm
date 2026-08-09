import streamlit as st

from src import niveis

DIMENSOES = [
    ("estrategia", "Estratégia e valor", "Clareza sobre onde a IA deve gerar valor no PPPM."),
    ("dados", "Dados e processos", "Qualidade, disponibilidade e integração dos dados."),
    ("casos_uso", "Casos de uso", "Existência de casos de uso estruturados e reprodutíveis."),
    ("governanca", "Governança e HITL", "Regras de validação humana, ética, LGPD e auditoria."),
    ("beneficios", "Benefícios e ROI", "Mensuração de ganho, custo e retorno das iniciativas."),
]

_ORDEM_DESEMPATE = ["governanca", "dados", "estrategia", "casos_uso", "beneficios"]

_ACAO_GARGALO = {
    "estrategia": "conectar cada iniciativa de IA a um objetivo estratégico mensurável e a um dono executivo",
    "dados": "mapear as fontes de dados, corrigir os gaps críticos e definir um padrão mínimo de qualidade",
    "casos_uso": "priorizar de 1 a 3 casos de uso com dor real, dado mínimo, risco controlável e benefício mensurável",
    "governanca": "definir regras de validação humana (HITL), papéis, ética e conformidade antes de escalar qualquer piloto",
    "beneficios": "estruturar business case, métricas de sucesso e rotina de medição de benefícios em ciclos curtos",
}


def calcular_total(diag: dict) -> int:
    return sum(int(diag.get(k, 0) or 0) for k, _, _ in DIMENSOES)


def calcular_nivel(total: int) -> dict:
    return niveis.get_nivel(total)


def identificar_gargalo(diag: dict) -> str:
    valores = {k: int(diag.get(k, 0) or 0) for k, _, _ in DIMENSOES}
    minimo = min(valores.values())
    for dim in _ORDEM_DESEMPATE:
        if valores.get(dim, 0) == minimo:
            return dim
    return next(iter(valores))


def rotulo_dimensao(dim_key: str) -> str:
    for k, rotulo, _ in DIMENSOES:
        if k == dim_key:
            return rotulo
    return dim_key


def acao_gargalo(dim_key: str) -> str:
    return _ACAO_GARGALO.get(dim_key, "atacar o gargalo com uma ação consultiva específica")


def leitura_executiva(diag: dict) -> str:
    total = calcular_total(diag)
    nivel = calcular_nivel(total)
    gargalo = identificar_gargalo(diag)
    template = nivel["leitura_executiva_template"]
    return template.format(
        gargalo=rotulo_dimensao(gargalo),
        acao_gargalo=acao_gargalo(gargalo),
    )


def render() -> None:
    st.subheader("2. Diagnóstico de Maturidade IA-PPPM")
    st.caption(
        "Pontue cada dimensão de 0 (ausente) a 6 (otimizado). "
        "Pontuação total revela o nível e a leitura por dimensão revela onde agir primeiro."
    )

    col_form, col_painel = st.columns([2, 1])

    with col_form:
        for key, rotulo, helper in DIMENSOES:
            atual = int(st.session_state["diagnostico"].get(key, 0) or 0)
            st.session_state["diagnostico"][key] = st.slider(
                rotulo, min_value=0, max_value=6, value=atual, help=helper, key=f"slider_{key}"
            )

    diag = st.session_state["diagnostico"]
    total = calcular_total(diag)
    nivel = calcular_nivel(total)
    gargalo = identificar_gargalo(diag)

    with col_painel:
        st.metric("Pontuação total", f"{total} / 30")
        st.metric("Nível", f"{nivel['numero']} — {nivel['rotulo']}")
        st.markdown("**Gargalo prioritário**")
        st.info(rotulo_dimensao(gargalo))

    st.markdown("---")
    st.markdown("**Leitura executiva**")
    st.write(leitura_executiva(diag))
