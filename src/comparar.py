import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src import db, mapa_pmbok

_DIMENSOES = [
    ("estrategia", "Estratégia"),
    ("dados", "Dados"),
    ("casos_uso", "Casos de uso"),
    ("governanca", "Governança"),
    ("beneficios", "Benefícios"),
]

_CORES_TRATAMENTO = {
    "ia": "#1E88E5",       # azul — só IA
    "ia_po": "#43A047",    # verde — IA+PO
    "gap": "#E53935",      # vermelho — gap não atendido
    "nenhum": "#ECEFF1",   # cinza claro — não marcado
}


def _radar_multi_projeto(projetos: list[dict]) -> go.Figure:
    categorias = [rot for _, rot in _DIMENSOES]
    fig = go.Figure()
    for p in projetos:
        valores = [int(p.get(k, 0) or 0) for k, _ in _DIMENSOES]
        valores += valores[:1]
        fig.add_trace(
            go.Scatterpolar(
                r=valores,
                theta=categorias + categorias[:1],
                fill="toself",
                name=f"[{p['id']}] {p['nome'][:35]}",
                hovertemplate="<b>%{theta}</b>: %{r}/6<extra></extra>",
            )
        )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 6])),
        showlegend=True,
        height=500,
        margin=dict(t=10, b=10, l=10, r=10),
    )
    return fig


def _heatmap_pmbok(projetos: list[dict], processos: list[dict]) -> go.Figure:
    proc_ids = [p["id"] for p in processos]
    proc_labels = [f"{p['id']} {p['nome'][:24]}" for p in processos]

    matriz_num: list[list[int]] = []
    matriz_txt: list[list[str]] = []
    projeto_labels: list[str] = []
    map_trat_num = {"nenhum": 0, "ia": 1, "ia_po": 2, "gap": -1}

    for pj in projetos:
        projeto_labels.append(f"[{pj['id']}] {pj['nome'][:30]}")
        tratamentos = db.listar_tratamentos_pmbok(pj["id"])
        linha_n, linha_t = [], []
        for pid in proc_ids:
            t = tratamentos.get(pid)
            if t:
                linha_n.append(map_trat_num[t["tratamento"]])
                linha_t.append(f"{t['tratamento']} · {t['criticidade']}<br>{t['observacao']}")
            else:
                linha_n.append(0)
                linha_t.append("não marcado")
        matriz_num.append(linha_n)
        matriz_txt.append(linha_t)

    fig = go.Figure(
        data=go.Heatmap(
            z=matriz_num,
            x=proc_labels,
            y=projeto_labels,
            text=matriz_txt,
            hovertemplate="<b>%{y}</b><br>%{x}<br>%{text}<extra></extra>",
            colorscale=[
                [0.0, "#E53935"],   # gap (-1)
                [0.25, "#ECEFF1"],  # nenhum (0)
                [0.5, "#ECEFF1"],
                [0.75, "#1E88E5"],  # ia (1)
                [1.0, "#43A047"],   # ia_po (2)
            ],
            zmin=-1, zmax=2,
            showscale=True,
            colorbar=dict(
                title="Tratamento",
                tickvals=[-1, 0, 1, 2],
                ticktext=["gap", "—", "IA", "IA+PO"],
            ),
        )
    )
    fig.update_layout(
        height=max(340, 40 * len(projetos)),
        xaxis=dict(tickangle=-70, tickfont=dict(size=9)),
        yaxis=dict(tickfont=dict(size=10)),
        margin=dict(t=10, b=140, l=10, r=10),
    )
    return fig


def _dataframe_ranking(projetos: list[dict]) -> pd.DataFrame:
    linhas = []
    for p in projetos:
        tratamentos = db.listar_tratamentos_pmbok(p["id"])
        total_matur = sum(int(p.get(k, 0) or 0) for k, _ in _DIMENSOES)
        cont = {"ia": 0, "ia_po": 0, "gap": 0, "nenhum": 0}
        for t in tratamentos.values():
            cont[t["tratamento"]] = cont.get(t["tratamento"], 0) + 1
        criticos = sum(
            1 for t in tratamentos.values() if t["criticidade"] == "alta"
        )
        linhas.append(
            {
                "ID": p["id"],
                "Projeto": p["nome"],
                "Empresa": p["empresa"],
                "Porte": p["porte"],
                "Maturidade /30": total_matur,
                "Processos marcados": len(tratamentos),
                "Só IA": cont["ia"],
                "IA + PO": cont["ia_po"],
                "Gaps": cont["gap"],
                "Críticos (alta)": criticos,
            }
        )
    return pd.DataFrame(linhas).sort_values("Maturidade /30", ascending=False)


def render() -> None:
    st.subheader("8. Comparar projetos")
    st.caption(
        "Visão cross-portfólio: maturidade em IA-PPPM (5 dimensões) e cobertura "
        "PMBOK × IA × PO por projeto. Serve para benchmark interno e demo comercial."
    )

    projetos = db.listar_projetos()
    if not projetos:
        st.warning("Nenhum projeto cadastrado. Popule a base pela aba 7 ou rode `scripts/seed_projetos_locais.py`.")
        return

    processos = mapa_pmbok.carregar_processos()

    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        c1.metric("Total de projetos", len(projetos))
        c2.metric("Empresas únicas", len({p["empresa"] for p in projetos if p["empresa"]}))
        total_marc = sum(len(db.listar_tratamentos_pmbok(p["id"])) for p in projetos)
        c3.metric("Total de marcações PMBOK", total_marc)

    nomes = {f"[{p['id']}] {p['nome']}": p["id"] for p in projetos}
    escolhidos = st.multiselect(
        "Projetos para comparar (padrão: todos)",
        options=list(nomes.keys()),
        default=list(nomes.keys()),
        key="comparar_multiselect",
    )
    ids_escolhidos = [nomes[n] for n in escolhidos]
    projetos_sel = [p for p in projetos if p["id"] in ids_escolhidos]
    if not projetos_sel:
        st.info("Selecione ao menos 1 projeto.")
        return

    aba_radar, aba_heat, aba_rank = st.tabs(
        ["🕸 Radar de maturidade", "🔥 Heatmap PMBOK", "🏁 Ranking / tabela"]
    )

    with aba_radar:
        st.markdown(
            "Radar sobreposto das 5 dimensões de maturidade IA-PPPM (0-6). "
            "Áreas pequenas indicam projetos ainda iniciantes; áreas grandes, projetos maduros."
        )
        st.plotly_chart(_radar_multi_projeto(projetos_sel), use_container_width=True)

    with aba_heat:
        st.markdown(
            "Cobertura PMBOK × IA × PO por projeto. **Verde:** IA+PO. **Azul:** só IA. "
            "**Vermelho:** gap declarado (processo importante ainda não atendido). "
            "Serve para achar padrões de subutilização e priorizar próximos pilotos."
        )
        st.plotly_chart(_heatmap_pmbok(projetos_sel, processos), use_container_width=True)

    with aba_rank:
        df = _dataframe_ranking(projetos_sel)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("**Distribuição de tratamentos (todos os projetos selecionados):**")
        col_a, col_b = st.columns(2)
        totais_trat = {"Só IA": 0, "IA + PO": 0, "Gaps": 0}
        for p in projetos_sel:
            for t in db.listar_tratamentos_pmbok(p["id"]).values():
                if t["tratamento"] == "ia":
                    totais_trat["Só IA"] += 1
                elif t["tratamento"] == "ia_po":
                    totais_trat["IA + PO"] += 1
                elif t["tratamento"] == "gap":
                    totais_trat["Gaps"] += 1
        col_a.metric("Só IA", totais_trat["Só IA"])
        col_b.metric("IA + PO", totais_trat["IA + PO"])
        st.metric("Gaps declarados", totais_trat["Gaps"])

        st.markdown("**Áreas PMBOK mais atendidas:**")
        contagem_area: dict[str, int] = {}
        for p in projetos_sel:
            trats = db.listar_tratamentos_pmbok(p["id"])
            for pid_pr, t in trats.items():
                if t["tratamento"] in ("ia", "ia_po"):
                    proc = next((x for x in processos if x["id"] == pid_pr), None)
                    if proc:
                        contagem_area[proc["area"]] = contagem_area.get(proc["area"], 0) + 1
        if contagem_area:
            df_area = pd.DataFrame(
                sorted(contagem_area.items(), key=lambda x: -x[1]),
                columns=["Área PMBOK", "Marcações IA/IA+PO"],
            )
            fig_bar = px.bar(
                df_area,
                x="Marcações IA/IA+PO",
                y="Área PMBOK",
                orientation="h",
                color="Marcações IA/IA+PO",
                color_continuous_scale="Blues",
            )
            fig_bar.update_layout(height=280, margin=dict(t=10, b=10, l=10, r=10))
            st.plotly_chart(fig_bar, use_container_width=True)
