from pathlib import Path

import streamlit as st

from src import (
    comparar,
    contexto,
    diagnostico,
    db,
    governanca_ui,
    mapa_blocos,
    mapa_pmbok,
    pdf_export,
    priorizacao_ui,
    projetos,
    recomendador,
    state,
    upload_ui,
)
from src.config import MOSTRAR_ABA_PILOTOS_PMBOK, MOSTRAR_PO_UI
from src.diagnostico import DIMENSOES, rotulo_dimensao

if MOSTRAR_ABA_PILOTOS_PMBOK:
    _TITULO_APP = "Consultor IA-PPPM — Mapa PMBOK 8ª Ed. × IA" + (" × IA+PO" if MOSTRAR_PO_UI else "")
else:
    _TITULO_APP = "Consultor IA-PPPM" + (" × PO" if MOSTRAR_PO_UI else "")

st.set_page_config(
    page_title=_TITULO_APP,
    layout="wide",
    initial_sidebar_state="expanded",
)

state.init_state()
db.init_db()
if "projeto_ativo_id" not in st.session_state:
    st.session_state["projeto_ativo_id"] = None

st.title(_TITULO_APP)
st.caption(
    "Quem usa IA acelera tarefas. Quem lidera IA gera valor. — Prof. Dr. José Bezerra | BSBr"
)

with st.sidebar:
    st.header("Progresso — Diagnóstico consultivo")
    etapas = [
        (1, "Contexto"),
        (2, "Diagnóstico"),
        (3, "Mapa 5 Blocos"),
        (4, "Pilotos"),
    ]
    for numero, rotulo in etapas:
        marcador = "✅" if state.is_step_complete(numero) else "⬜"
        st.write(f"{marcador} {numero}. {rotulo}")
    st.markdown("---")
    st.caption(
        "**Aula 1** conduz o diagnóstico consultivo: Contexto → Diagnóstico → Mapa 5 Blocos → "
        "Pilotos Recomendados → Exportar PDF. **Aula 2** traz Priorização e Governança + HITL. "
        "As abas de Projetos, Comparar e Auto-preencher são utilitárias — permitem salvar/reabrir "
        "seu trabalho e continuar depois."
    )
    st.markdown("---")
    if st.button("Reiniciar sessão"):
        state.reset_state()
        st.rerun()
    st.caption("Método Aulas 1 e 2 — Prof. Dr. José Bezerra | BSBr")

_LABELS_BASE = [
    "Contexto",
    "Diagnóstico",
    "Mapa 5 Blocos",
    "Pilotos Recomendados",
    "Exportar PDF",
    "Projetos",
    "Comparar",
    "Priorização (Aula 2)",
    "Governança + HITL (Aula 2)",
    "Auto-preencher (upload)",
]
_labels = (["Pilotos de IA em PPPM"] if MOSTRAR_ABA_PILOTOS_PMBOK else []) + _LABELS_BASE
tabs = st.tabs([f"{i}. {rot}" for i, rot in enumerate(_labels, start=1)])

_off = 0
if MOSTRAR_ABA_PILOTOS_PMBOK:
    with tabs[0]:
        mapa_pmbok.render()
    _off = 1

with tabs[_off + 0]:
    contexto.render()

with tabs[_off + 1]:
    if not state.is_step_complete(1):
        st.warning("Preencha e salve o contexto na aba anterior antes de avançar.")
    diagnostico.render()

with tabs[_off + 2]:
    if not state.is_step_complete(1):
        st.warning("Preencha o contexto antes de estruturar o Mapa 5 Blocos.")
    mapa_blocos.render()

with tabs[_off + 3]:
    st.subheader("Pilotos Recomendados")
    if not (state.is_step_complete(2) and state.is_step_complete(3)):
        st.warning("Complete o Diagnóstico e o Mapa 5 Blocos antes de gerar os pilotos.")
    else:
        catalogo = recomendador.carregar_catalogo()

        def _computar_top3() -> list[dict]:
            return recomendador.recomendar(
                st.session_state["diagnostico"],
                st.session_state["mapa"],
                top_n=3,
            )

        def _enriquecer(piloto: dict) -> dict:
            diag = st.session_state["diagnostico"]
            mapa_atual = st.session_state["mapa"]
            total = sum(int(diag.get(k, 0) or 0) for k, _, _ in DIMENSOES)
            from src import niveis as niveis_mod
            nivel_num = niveis_mod.get_nivel(total)["numero"]
            categorias = recomendador.extrair_categorias_dor(mapa_atual.get("dor", ""))
            entry = dict(piloto)
            entry["scoring"] = recomendador.scoring_piloto(piloto, nivel_num, categorias)
            entry["score_bruto"] = recomendador.computar_score_bruto(piloto, diag, mapa_atual)
            return entry

        if not st.session_state.get("pilotos_selecionados"):
            st.session_state["pilotos_selecionados"] = _computar_top3()

        col_rec, col_reset = st.columns([1, 1])
        if col_rec.button("🔄 Recalcular recomendação (top 3)"):
            st.session_state["pilotos_selecionados"] = _computar_top3()
            st.session_state.pop("pilotos_multiselect", None)
            st.rerun()
        if col_reset.button("🧹 Limpar seleção"):
            st.session_state["pilotos_selecionados"] = []
            st.session_state.pop("pilotos_multiselect", None)
            st.rerun()

        st.info(
            "🤝 **HITL — Human-in-the-Loop:** *A IA recomenda, o humano valida e decide.* "
            "(Prof. Dr. José Bezerra, Aula 1 IA-PPPM, BSBr, 2026-08-08 [16])"
        )

        nomes_catalogo = [p["nome"] for p in catalogo]
        nomes_selecionados = [p["nome"] for p in st.session_state["pilotos_selecionados"]]
        escolha = st.multiselect(
            "Pilotos incluídos no mapa e no PDF (adicione, tire ou troque à vontade):",
            options=nomes_catalogo,
            default=nomes_selecionados,
            key="pilotos_multiselect",
            help="Os 3 recomendados vêm marcados por padrão. Marque outros do catálogo para incluir; desmarque para remover.",
        )

        if escolha != nomes_selecionados:
            por_nome = {p["nome"]: p for p in catalogo}
            atual_por_nome = {p["nome"]: p for p in st.session_state["pilotos_selecionados"]}
            nova_lista = []
            for nome in escolha:
                if nome in atual_por_nome:
                    nova_lista.append(atual_por_nome[nome])
                elif nome in por_nome:
                    nova_lista.append(_enriquecer(por_nome[nome]))
            st.session_state["pilotos_selecionados"] = nova_lista
            st.rerun()

        pilotos = st.session_state["pilotos_selecionados"]
        if not pilotos:
            st.warning("Nenhum piloto selecionado. Clique em '🔄 Recalcular recomendação (top 3)' ou escolha manualmente acima.")

        for idx, piloto in enumerate(pilotos, start=1):
            with st.container(border=True):
                header = f"### {idx}. {piloto['nome']}"
                if piloto.get("citado_por_bezerra"):
                    header += " · 🎯 *citado por Bezerra em aula*"
                st.markdown(header)
                st.write(piloto["descricao"])
                c1, c2, c3 = st.columns(3)
                c1.metric("Impacto", piloto["scoring"]["impacto"].capitalize())
                c2.metric("Viabilidade", piloto["scoring"]["viabilidade"].capitalize())
                c3.metric("Risco", piloto["scoring"]["risco"].capitalize())
                st.markdown("**Pré-requisitos:**")
                for pr in piloto["pre_requisitos"]:
                    st.markdown(f"- {pr}")
                if piloto.get("ferramentas_recomendadas"):
                    st.markdown("**Ferramentas recomendadas:**")
                    for f in piloto["ferramentas_recomendadas"]:
                        st.markdown(f"- {f}")
                st.success(f"Ganho esperado: {piloto['ganho_esperado']}")
                st.caption(f"Tempo estimado: {piloto['tempo_estimado_semanas']} semanas")

with tabs[_off + 4]:
    st.subheader("Exportar PDF")
    if not state.is_step_complete(4):
        st.warning("Gere os pilotos recomendados na aba anterior antes de exportar.")
    else:
        ctx = st.session_state["contexto"]
        n_casos_a2 = len(st.session_state.get("aula2_casos") or [])
        st.markdown("**Preview do que vai no PDF:**")
        st.write(f"**Participante:** {ctx.get('nome')} — {ctx.get('cargo')}")
        st.write(f"**Empresa:** {ctx.get('empresa')} ({ctx.get('porte')})")
        st.write(f"**Nº de pilotos recomendados:** {len(st.session_state['pilotos_selecionados'])}")
        st.markdown(
            "**Aula 1 sempre inclui:** Capa · Contexto · Diagnóstico · Mapa 5 Blocos · "
            "Pilotos · Cases · Modelo Comercial."
        )
        if n_casos_a2:
            st.markdown(
                f"**Aula 2 disponível:** {n_casos_a2} caso(s) prontos para as seções "
                "*Priorização* e *Governança + HITL* no PDF completo."
            )
        else:
            st.caption(
                "Aula 2 vazia — cadastre casos na aba de Priorização para habilitar o PDF completo."
            )

        with st.expander("Ver leitura executiva do diagnóstico"):
            st.write(diagnostico.leitura_executiva(st.session_state["diagnostico"]))

        with st.expander("Ver gargalo prioritário"):
            gargalo = diagnostico.identificar_gargalo(st.session_state["diagnostico"])
            st.info(rotulo_dimensao(gargalo))

        col_a1, col_full = st.columns(2)

        if col_a1.button("📄 Gerar PDF — só Aula 1", type="secondary", use_container_width=True):
            output_dir = Path(__file__).resolve().parent / "output"
            output_dir.mkdir(exist_ok=True)
            tmp_path = output_dir / "mapa_aula1_temp.pdf"
            dados = state.get_all_data()
            dados["aula2"] = {"casos": [], "gov_respostas": {}, "gov_rastro": {}}
            caminho = pdf_export.gerar_pdf(dados, str(tmp_path))
            with open(caminho, "rb") as f:
                st.download_button(
                    "⬇️ Baixar PDF Aula 1",
                    data=f.read(),
                    file_name=Path(caminho).name,
                    mime="application/pdf",
                    use_container_width=True,
                )
            st.success(f"PDF Aula 1 gerado em: {caminho}")

        if col_full.button(
            "📚 Gerar PDF completo (Aula 1 + Aula 2)",
            type="primary",
            use_container_width=True,
            disabled=(n_casos_a2 == 0),
            help="Requer pelo menos 1 caso cadastrado na aba de Priorização (Aula 2)."
        ):
            output_dir = Path(__file__).resolve().parent / "output"
            output_dir.mkdir(exist_ok=True)
            tmp_path = output_dir / "mapa_completo_temp.pdf"
            caminho = pdf_export.gerar_pdf(state.get_all_data(), str(tmp_path))
            with open(caminho, "rb") as f:
                st.download_button(
                    "⬇️ Baixar PDF completo",
                    data=f.read(),
                    file_name=Path(caminho).name,
                    mime="application/pdf",
                    use_container_width=True,
                )
            st.success(f"PDF completo gerado em: {caminho}")

with tabs[_off + 5]:
    projetos.render()

with tabs[_off + 6]:
    comparar.render()

with tabs[_off + 7]:
    priorizacao_ui.render()

with tabs[_off + 8]:
    governanca_ui.render()

with tabs[_off + 9]:
    upload_ui.render()
