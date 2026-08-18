"""UI Streamlit da aba de Priorização de Casos de Uso — Aula 2 IA-PPPM."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src import priorizacao, validador_erros


STATE_KEY = "aula2_casos"


def _seed_empresa_alfa() -> list[priorizacao.CasoDeUso]:
    casos = priorizacao.carregar_empresa_alfa()
    for c in casos:
        c.notas = {
            "impacto": {"alfa-A": 4, "alfa-B": 5, "alfa-C": 5, "alfa-D": 2}[c.id],
            "viabilidade": {"alfa-A": 5, "alfa-B": 3, "alfa-C": 4, "alfa-D": 5}[c.id],
            "dados": {"alfa-A": 4, "alfa-B": 4, "alfa-C": 3, "alfa-D": 4}[c.id],
            "risco": {"alfa-A": 4, "alfa-B": 3, "alfa-C": 4, "alfa-D": 3}[c.id],
            "valor": {"alfa-A": 4, "alfa-B": 5, "alfa-C": 5, "alfa-D": 2}[c.id],
        }
    return casos


def _ensure_state() -> None:
    if STATE_KEY not in st.session_state:
        st.session_state[STATE_KEY] = _seed_empresa_alfa()


def _renderiza_alertas(caso: priorizacao.CasoDeUso) -> None:
    alertas = validador_erros.validar(caso)
    if not alertas:
        st.success("✅ Nenhum dos 5 erros de IA detectado neste caso.")
        return
    st.markdown("**⚠️ Alertas — 5 erros de IA em projetos (Aula 2, slides 7-12)**")
    for a in alertas:
        box = st.error if a.severidade == "alta" else st.warning
        box(
            f"**{a.erro_id} · {a.nome}** — {a.motivo}  \n"
            f"↳ *Correção de rota:* {a.correcao}"
        )


def _caso_editor(caso: priorizacao.CasoDeUso, criterios: list[dict]) -> None:
    alertas_qtd = len(validador_erros.validar(caso))
    marcador = "⚠️ " * min(alertas_qtd, 3) if alertas_qtd else "✅ "
    header = f"{marcador}**{caso.nome}** · `{caso.id}`" + (f" — {alertas_qtd} alerta(s)" if alertas_qtd else "")
    with st.expander(header, expanded=False):
        caso.contexto = st.text_input("Contexto (projeto/PMO/programa/portfólio)", caso.contexto, key=f"ctx_{caso.id}")
        caso.dor = st.text_area("Dor — qual problema real será resolvido?", caso.dor, key=f"dor_{caso.id}", height=70)
        caso.dados = st.text_area("Dados — quais informações sustentam?", caso.dados, key=f"dad_{caso.id}", height=70)
        caso.decisao = st.text_area("Decisão — qual escolha será melhorada?", caso.decisao, key=f"dec_{caso.id}", height=70)
        caso.dono = st.text_input(
            "Dono humano da decisão (⚠️ obrigatório — sem dono, corte automático)",
            caso.dono or "",
            key=f"dono_{caso.id}",
        )
        caso.metrica_valor = st.text_area(
            "Métrica de valor — como mediremos?", caso.metrica_valor, key=f"met_{caso.id}", height=70
        )
        st.markdown("**Notas (1 = muito baixo · 5 = muito alto)**")
        cols = st.columns(len(criterios))
        for col, crit in zip(cols, criterios):
            with col:
                caso.notas[crit["id"]] = st.slider(
                    crit["nome"],
                    min_value=1,
                    max_value=5,
                    value=int(caso.notas.get(crit["id"], 3) or 3),
                    key=f"nota_{caso.id}_{crit['id']}",
                    help=crit["pergunta_executiva"],
                )
        st.markdown("---")
        _renderiza_alertas(caso)


def _tabela_resultado(resultado: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(
        [
            {
                "Caso": r["nome"],
                "Score": r["score"],
                "Ranking": r["ranking"],
                "Quadrante": r["quadrante"],
                "Dono": r["dono"] or "—",
                "Prontidão": r["status_prontidao"],
            }
            for r in resultado
        ]
    )
    return df


def _matriz_visual(resultado: list[dict]) -> None:
    pontos = pd.DataFrame(
        [
            {
                "Caso": r["nome"],
                "Impacto": r["notas"].get("impacto", 0),
                "Viabilidade": r["notas"].get("viabilidade", 0),
                "Score": r["score"],
                "Ranking": r["ranking"],
            }
            for r in resultado
        ]
    )
    fig = px.scatter(
        pontos,
        x="Viabilidade",
        y="Impacto",
        size="Score",
        color="Ranking",
        text="Caso",
        range_x=[0.5, 5.5],
        range_y=[0.5, 5.5],
        color_discrete_map={
            "Fazer agora": "#2ecc71",
            "Preparar": "#f1c40f",
            "Não priorizar": "#e74c3c",
        },
    )
    fig.add_shape(type="line", x0=3.5, x1=3.5, y0=0.5, y1=5.5, line=dict(dash="dash", color="#888"))
    fig.add_shape(type="line", x0=0.5, x1=5.5, y0=3.5, y1=3.5, line=dict(dash="dash", color="#888"))
    fig.update_traces(textposition="top center")
    fig.update_layout(height=500, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)


def render() -> None:
    _ensure_state()
    criterios_data = priorizacao.carregar_criterios()
    criterios = criterios_data["criterios"]

    st.subheader("9. Priorização de Casos de Uso — Aula 2")
    st.caption(
        "*Ideia boa só vira valor quando passa por método, governança e decisão humana.* "
        "— Prof. Dr. José Bezerra, Aula 2 IA-PPPM (BSBr, 2026-08-17)"
    )

    with st.expander("📖 Metodologia — Score Executivo e Corte Obrigatório", expanded=False):
        st.markdown(
            f"""
**Score ponderado** ({criterios_data['fonte']}):

| Critério | Peso | Pergunta executiva |
|---|---:|---|
| Impacto no resultado | {int(criterios[0]['peso']*100)}% | {criterios[0]['pergunta_executiva']} |
| Viabilidade técnica | {int(criterios[1]['peso']*100)}% | {criterios[1]['pergunta_executiva']} |
| Dados disponíveis | {int(criterios[2]['peso']*100)}% | {criterios[2]['pergunta_executiva']} |
| Risco / segurança | {int(criterios[3]['peso']*100)}% | {criterios[3]['pergunta_executiva']} |
| Valor potencial | {int(criterios[4]['peso']*100)}% | {criterios[4]['pergunta_executiva']} |

- **Ranking**: {criterios_data['thresholds']['descricao']}
- **Corte obrigatório**: {criterios_data['corte_obrigatorio']['regra']}
"""
        )

    st.markdown("### Casos de uso")
    st.caption(
        "Preset carregado: **Empresa Alfa** (slide 37). Edite, adicione, remova. "
        "Um dos casos vem sem dono — é o exemplo do corte obrigatório."
    )

    c1, c2, c3 = st.columns([1, 1, 3])
    if c1.button("+ Novo caso", use_container_width=True):
        novos = st.session_state[STATE_KEY]
        novos.append(
            priorizacao.CasoDeUso(
                id=f"c{len(novos)+1}",
                nome=f"Novo caso {len(novos)+1}",
                notas={cid: 3 for cid in priorizacao.CRITERIO_IDS},
            )
        )
        st.rerun()
    if c2.button("↺ Recarregar Empresa Alfa", use_container_width=True):
        st.session_state[STATE_KEY] = _seed_empresa_alfa()
        st.rerun()

    for caso in st.session_state[STATE_KEY]:
        _caso_editor(caso, criterios)

    st.markdown("---")
    st.markdown("### 🛡️ Resumo dos 5 Erros no lote")
    contagem = validador_erros.resumo_lote(st.session_state[STATE_KEY])
    regras = {r["id"]: r for r in validador_erros.carregar_regras()["erros"]}
    cols = st.columns(5)
    for col, eid in zip(cols, ["E1", "E2", "E3", "E4", "E5"]):
        with col:
            n = contagem[eid]
            delta_color = "inverse" if n > 0 else "off"
            col.metric(
                label=f"{eid} · {regras[eid]['nome']}",
                value=f"{n} caso(s)",
                delta="atenção" if n > 0 else "ok",
                delta_color=delta_color,
            )

    st.markdown("### 🎯 Resultado — Ranking e Matriz")
    resultado = priorizacao.priorizar_lote(st.session_state[STATE_KEY])

    def _cor_ranking(v):
        if v == "Fazer agora":
            return "background-color: #d4edda; color: #155724"
        if v == "Preparar":
            return "background-color: #fff3cd; color: #856404"
        return "background-color: #f8d7da; color: #721c24"

    df = _tabela_resultado(resultado)
    st.dataframe(
        df.style.map(_cor_ranking, subset=["Ranking"]),
        use_container_width=True,
        hide_index=True,
    )

    _matriz_visual(resultado)

    st.markdown("### ✅ Top 3 selecionados (entregável da Aula 2)")
    top3 = priorizacao.top_n(resultado, n=3)
    if not top3:
        st.warning("Nenhum caso com score suficiente e dono definido. Ajuste os casos acima.")
    else:
        for i, r in enumerate(top3, start=1):
            with st.container(border=True):
                st.markdown(
                    f"**{i}. {r['nome']}** · Score **{r['score']}** · "
                    f"Ranking **{r['ranking']}** · Quadrante *{r['quadrante']}* · "
                    f"Dono: {r['dono']}"
                )
        st.info(
            "🤝 **Próximo passo** — para cada caso: definir onde haverá validação humana "
            "(HITL) e o registro de rastreabilidade. Ver aba de Governança."
        )
