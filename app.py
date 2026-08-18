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
from src.config import MOSTRAR_PO_UI
from src.diagnostico import DIMENSOES, rotulo_dimensao

_TITULO_APP = "Consultor IA-PPPM — Mapa PMBOK 8ª Ed. × IA" + (" × IA+PO" if MOSTRAR_PO_UI else "")

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
        "**Aba 1 — Pilotos de IA em PPPM** mostra 16 aplicações concretas onde IA muda o jogo "
        "em Portfólio, Programa e Projeto (dor real, exemplo, esforço, KPI benchmark). "
        "O mapa completo dos 40 processos PMBOK fica como referência opcional no fim da aba. "
        "As demais abas rodam o diagnóstico consultivo (Contexto → Diagnóstico → Mapa 5 Blocos → Pilotos → PDF), "
        "as próximas gerenciam múltiplos projetos e comparações, e as duas últimas (9 e 10) trazem o método da Aula 2."
    )
    st.markdown("---")
    if st.button("Reiniciar sessão"):
        state.reset_state()
        st.rerun()
    st.caption("Método Aula 1 — Prof. Dr. José Bezerra | BSBr")

tabs = st.tabs(
    [
        "1. Pilotos de IA em PPPM",
        "2. Contexto",
        "3. Diagnóstico",
        "4. Mapa 5 Blocos",
        "5. Pilotos Recomendados",
        "6. Exportar PDF",
        "7. Projetos",
        "8. Comparar",
        "9. Priorização (Aula 2)",
        "10. Governança + HITL (Aula 2)",
        "11. Auto-preencher (upload)",
    ]
)

with tabs[0]:
    mapa_pmbok.render()

with tabs[1]:
    contexto.render()

with tabs[2]:
    if not state.is_step_complete(1):
        st.warning("Preencha e salve o contexto na aba 2 antes de avançar.")
    diagnostico.render()

with tabs[3]:
    if not state.is_step_complete(1):
        st.warning("Preencha o contexto antes de estruturar o Mapa 5 Blocos.")
    mapa_blocos.render()

with tabs[4]:
    st.subheader("5. Pilotos Recomendados")
    if not (state.is_step_complete(2) and state.is_step_complete(3)):
        st.warning("Complete o Diagnóstico e o Mapa 5 Blocos antes de gerar os pilotos.")
    else:
        catalogo = recomendador.carregar_catalogo()
        pilotos = recomendador.recomendar(
            st.session_state["diagnostico"],
            st.session_state["mapa"],
            top_n=3,
        )
        st.session_state["pilotos_selecionados"] = pilotos

        st.info(
            "🤝 **HITL — Human-in-the-Loop:** *A IA recomenda, o humano valida e decide.* "
            "(Prof. Dr. José Bezerra, Aula 1 IA-PPPM, BSBr, 2026-08-08 [16])"
        )

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

                nomes = [p["nome"] for p in catalogo]
                atual_idx = nomes.index(piloto["nome"]) if piloto["nome"] in nomes else 0
                escolha = st.selectbox(
                    "Substituir por outro piloto do catálogo:",
                    nomes,
                    index=atual_idx,
                    key=f"substituir_{idx}",
                )
                if escolha != piloto["nome"]:
                    novo = next(p for p in catalogo if p["nome"] == escolha)
                    total = sum(int(st.session_state["diagnostico"].get(k, 0) or 0) for k, _, _ in DIMENSOES)
                    from src import niveis as niveis_mod
                    nivel_num = niveis_mod.get_nivel(total)["numero"]
                    categorias = recomendador.extrair_categorias_dor(st.session_state["mapa"].get("dor", ""))
                    novo_entry = dict(novo)
                    novo_entry["scoring"] = recomendador.scoring_piloto(novo, nivel_num, categorias)
                    novo_entry["score_bruto"] = 0
                    st.session_state["pilotos_selecionados"][idx - 1] = novo_entry
                    st.rerun()

with tabs[5]:
    st.subheader("6. Exportar PDF")
    if not state.is_step_complete(4):
        st.warning("Gere os pilotos recomendados na aba 5 antes de exportar.")
    else:
        st.markdown("**Preview do que vai no PDF:**")
        ctx = st.session_state["contexto"]
        st.write(f"**Participante:** {ctx.get('nome')} — {ctx.get('cargo')}")
        st.write(f"**Empresa:** {ctx.get('empresa')} ({ctx.get('porte')})")
        st.write(f"**Nº de pilotos recomendados:** {len(st.session_state['pilotos_selecionados'])}")

        with st.expander("Ver leitura executiva do diagnóstico"):
            st.write(diagnostico.leitura_executiva(st.session_state["diagnostico"]))

        with st.expander("Ver gargalo prioritário"):
            gargalo = diagnostico.identificar_gargalo(st.session_state["diagnostico"])
            st.info(rotulo_dimensao(gargalo))

        if st.button("Gerar PDF", type="primary"):
            output_dir = Path(__file__).resolve().parent / "output"
            output_dir.mkdir(exist_ok=True)
            tmp_path = output_dir / "mapa_temp.pdf"
            caminho = pdf_export.gerar_pdf(state.get_all_data(), str(tmp_path))
            with open(caminho, "rb") as f:
                st.download_button(
                    "Baixar PDF",
                    data=f.read(),
                    file_name=Path(caminho).name,
                    mime="application/pdf",
                )
            st.success(f"PDF gerado em: {caminho}")

with tabs[6]:
    projetos.render()

with tabs[7]:
    comparar.render()

with tabs[8]:
    priorizacao_ui.render()

with tabs[9]:
    governanca_ui.render()

with tabs[10]:
    upload_ui.render()
