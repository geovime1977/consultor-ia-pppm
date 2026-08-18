import json
from datetime import date

import streamlit as st

from src import db, import_export, mapa_pmbok
from src.config import MOSTRAR_ABA_PILOTOS_PMBOK

_PORTES = ["MEI", "Pequena", "Média", "Grande", "N/A"]


def _reset_form_state() -> None:
    for k in list(st.session_state.keys()):
        if k.startswith("proj_form_"):
            del st.session_state[k]


def _selecionar_projeto_ativo(projetos: list[dict]) -> None:
    """Seletor de projeto ativo (usado internamente para persistência SQLite)."""
    nomes = ["(nenhum)"] + [f"[{p['id']}] {p['nome']}" for p in projetos]
    escolha = st.selectbox(
        "Projeto ativo",
        nomes,
        key="proj_ativo_select",
        help="Ao escolher um projeto aqui, ele fica marcado como ativo na sessão.",
    )
    if escolha == "(nenhum)":
        st.session_state["projeto_ativo_id"] = None
    else:
        st.session_state["projeto_ativo_id"] = int(escolha.split("]")[0].strip("["))


def _bloco_import_export() -> None:  # noqa: D401 - documented via docstring
    with st.expander("📁 Salvar / Carregar meu projeto (JSON)", expanded=False):
        st.caption(
            "O Streamlit Cloud não guarda seu progresso entre sessões. "
            "**Exporte um JSON no fim da sessão** e **importe da próxima vez** para continuar de onde parou. "
            "Cobre Aula 1 (contexto, diagnóstico, mapa, pilotos) e Aula 2 (casos, governança, HITL)."
        )
        col_exp, col_imp = st.columns(2)
        with col_exp:
            st.markdown("**📤 Exportar sessão atual**")
            tem_chave_groq = bool((st.session_state.get("groq_api_key") or "").strip())
            incluir_chave = st.checkbox(
                "Incluir minha chave Groq no JSON (⚠ trate esse arquivo como senha)",
                value=False,
                key="proj_export_incluir_groq",
                disabled=not tem_chave_groq,
                help="Se marcar, na próxima vez que importar o JSON a IA já vem ativa "
                     "sem precisar colar a chave de novo. Não compartilhe o arquivo — "
                     "quem tiver ele consome o crédito grátis da sua conta Groq."
                     + ("" if tem_chave_groq else " (Cadastre a chave na aba Auto-preencher antes.)"),
            )
            estado = {
                "contexto": st.session_state.get("contexto", {}),
                "diagnostico": st.session_state.get("diagnostico", {}),
                "mapa": st.session_state.get("mapa", {}),
                "pilotos_selecionados": st.session_state.get("pilotos_selecionados", []),
                "aula2_casos": st.session_state.get("aula2_casos", []),
                "aula2_gov_respostas": st.session_state.get("aula2_gov_respostas", {}),
                "aula2_gov_rastro": st.session_state.get("aula2_gov_rastro", {}),
                "groq_api_key": st.session_state.get("groq_api_key", ""),
            }
            payload = import_export.exportar_json(estado, incluir_chave_groq=incluir_chave)
            empresa = (st.session_state.get("contexto", {}) or {}).get("empresa") or "meu-projeto"
            slug = "".join(c if c.isalnum() else "-" for c in empresa.lower()).strip("-") or "projeto"
            st.download_button(
                "📥 Baixar JSON do meu projeto",
                data=payload,
                file_name=f"consultor-ia-pppm-{slug}.json",
                mime="application/json",
                use_container_width=True,
            )
        with col_imp:
            st.markdown("**📥 Importar sessão anterior**")
            arquivo = st.file_uploader(
                "Escolha o JSON exportado",
                type=["json"],
                key="proj_import_json",
                label_visibility="collapsed",
            )
            if arquivo is not None:
                try:
                    texto = arquivo.read().decode("utf-8")
                    novo = import_export.importar_json(texto)
                    chave_importada = (novo.pop("groq_api_key", "") or "").strip()
                    for k, v in novo.items():
                        st.session_state[k] = v
                    if chave_importada:
                        st.session_state["groq_api_key"] = chave_importada
                    st.success(
                        "✅ Projeto importado com sucesso!\n\n"
                        + import_export.resumo_importacao(novo)
                        + ("\nChave Groq restaurada — IA ativa." if chave_importada else "")
                    )
                    st.info("Abra as abas do fluxo consultivo e da Aula 2 para ver os dados carregados.")
                except import_export.ErroImportacao as e:
                    st.error(f"❌ Falha na importação: {e}")


def render() -> None:
    st.subheader("Projetos cadastrados")
    st.caption(
        "Base persistente (SQLite `data/diag.db`) para acompanhar diagnósticos "
        "de múltiplos projetos e usar em benchmarks cross-portfólio."
    )

    _bloco_import_export()

    projetos = db.listar_projetos()
    if MOSTRAR_ABA_PILOTOS_PMBOK:
        c1, c2, c3, c4 = st.columns(4)
    else:
        c1, c2, c4 = st.columns(3)
    c1.metric("Projetos", len(projetos))
    if projetos:
        c2.metric("Empresas únicas", len({p["empresa"] for p in projetos if p["empresa"]}))
        if MOSTRAR_ABA_PILOTOS_PMBOK:
            total_procs = sum(len(db.listar_tratamentos_pmbok(p["id"])) for p in projetos)
            c3.metric("Processos PMBOK marcados", total_procs)
        c4.metric("Última atualização", projetos[0]["atualizado_em"][:10] if projetos else "—")

    _selecionar_projeto_ativo(projetos)

    st.markdown("---")

    if MOSTRAR_ABA_PILOTOS_PMBOK:
        aba_lista, aba_novo, aba_da_sessao, aba_processos = st.tabs(
            ["📋 Lista", "➕ Cadastrar novo", "💾 Salvar sessão atual", "🎯 Marcar processos PMBOK"]
        )
    else:
        aba_lista, aba_novo, aba_da_sessao = st.tabs(
            ["📋 Lista", "➕ Cadastrar novo", "💾 Salvar sessão atual"]
        )
        aba_processos = None

    with aba_lista:
        if not projetos:
            st.info("Nenhum projeto cadastrado ainda. Use as outras abas para popular.")
        else:
            for p in projetos:
                titulo = f"**[{p['id']}] {p['nome']}** — {p['empresa']} · {p['porte']}"
                with st.expander(titulo):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown(f"**Cargo do GP:** {p['cargo_gp']}")
                        st.markdown(f"**Nº de projetos:** {p['n_projetos']}")
                        st.markdown(f"**PMO ativo:** {'Sim' if p['pmo_ativo'] else 'Não'}")
                        st.markdown(f"**Criado em:** {p['criado_em'][:10]}")
                        st.markdown(f"**Atualizado em:** {p['atualizado_em'][:10]}")
                    with col_b:
                        total = sum(
                            int(p.get(d, 0) or 0)
                            for d in ("estrategia", "dados", "casos_uso", "governanca", "beneficios")
                        )
                        st.markdown(f"**Maturidade total:** {total}/30")
                        st.markdown(f"- Estratégia: {p['estrategia']}")
                        st.markdown(f"- Dados: {p['dados']}")
                        st.markdown(f"- Casos de uso: {p['casos_uso']}")
                        st.markdown(f"- Governança: {p['governanca']}")
                        st.markdown(f"- Benefícios: {p['beneficios']}")

                    st.markdown("**Mapa 5 Blocos:**")
                    st.markdown(f"- **Contexto:** {p['mapa_contexto']}")
                    st.markdown(f"- **Dor:** {p['mapa_dor']}")
                    st.markdown(f"- **Dados:** {p['mapa_dados']}")
                    st.markdown(f"- **Riscos:** {p['mapa_riscos']}")
                    st.markdown(f"- **Valor:** {p['mapa_valor']}")

                    if p["pilotos"]:
                        st.markdown("**Pilotos:**")
                        for piloto in p["pilotos"]:
                            st.markdown(
                                f"- {piloto.get('nome', '?')} · "
                                f"impacto: {piloto.get('impacto', '?')} · "
                                f"viabilidade: {piloto.get('viabilidade', '?')} · "
                                f"risco: {piloto.get('risco', '?')}"
                            )

                    if MOSTRAR_ABA_PILOTOS_PMBOK:
                        tratamentos = db.listar_tratamentos_pmbok(p["id"])
                        if tratamentos:
                            st.markdown(f"**Processos PMBOK marcados:** {len(tratamentos)}")
                            for pid_pr, t in sorted(tratamentos.items()):
                                emoji = {"ia": "🤖", "ia_po": "🧮", "gap": "⚠️", "nenhum": "⬜"}.get(t["tratamento"], "?")
                                st.markdown(
                                    f"- {emoji} `{pid_pr}` — **{t['tratamento']}** · "
                                    f"criticidade: {t['criticidade']} · _{t['observacao']}_"
                                )

                    col_del, col_json = st.columns(2)
                    if col_del.button("🗑 Excluir", key=f"del_{p['id']}"):
                        db.excluir_projeto(p["id"])
                        st.success(f"Projeto {p['nome']} excluído.")
                        st.rerun()
                    if col_json.download_button(
                        "📄 Exportar JSON",
                        data=json.dumps(
                            {**p, "tratamentos_pmbok": db.listar_tratamentos_pmbok(p["id"])},
                            ensure_ascii=False, indent=2, default=str,
                        ),
                        file_name=f"projeto_{p['id']}_{p['nome'].replace(' ', '_')}.json",
                        mime="application/json",
                        key=f"json_{p['id']}",
                    ):
                        pass

    with aba_novo:
        st.markdown("Cadastrar um projeto novo (preenchimento manual):")
        with st.form("novo_projeto_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome do projeto*")
                empresa = st.text_input("Empresa / cliente")
                porte = st.selectbox("Porte", _PORTES)
                cargo_gp = st.text_input("Cargo do GP")
                n_projetos = st.number_input("Nº de projetos no portfólio", min_value=0, value=0, step=1)
                pmo_ativo = st.checkbox("PMO ativo")
            with col2:
                st.markdown("**Diagnóstico (0-6 por dimensão):**")
                estrategia = st.slider("Estratégia", 0, 6, 0, key="new_estrategia")
                dados = st.slider("Dados", 0, 6, 0, key="new_dados")
                casos_uso = st.slider("Casos de uso", 0, 6, 0, key="new_casos")
                governanca = st.slider("Governança", 0, 6, 0, key="new_gov")
                beneficios = st.slider("Benefícios", 0, 6, 0, key="new_ben")

            st.markdown("**Mapa 5 Blocos:**")
            mapa_contexto = st.text_area("Contexto", height=80)
            mapa_dor = st.text_area("Dor", height=80)
            mapa_dados = st.text_area("Dados", height=80)
            mapa_riscos = st.text_area("Riscos", height=80)
            mapa_valor = st.text_area("Valor", height=80)

            submitted = st.form_submit_button("💾 Cadastrar", type="primary")
            if submitted:
                if not nome.strip():
                    st.error("Nome é obrigatório.")
                else:
                    try:
                        proj_id = db.salvar_projeto({
                            "nome": nome.strip(),
                            "empresa": empresa.strip(),
                            "porte": porte,
                            "cargo_gp": cargo_gp.strip(),
                            "n_projetos": n_projetos,
                            "pmo_ativo": pmo_ativo,
                            "estrategia": estrategia,
                            "dados": dados,
                            "casos_uso": casos_uso,
                            "governanca": governanca,
                            "beneficios": beneficios,
                            "mapa_contexto": mapa_contexto,
                            "mapa_dor": mapa_dor,
                            "mapa_dados": mapa_dados,
                            "mapa_riscos": mapa_riscos,
                            "mapa_valor": mapa_valor,
                            "pilotos": [],
                        })
                        st.success(f"Projeto cadastrado com id={proj_id}. Recarregue a aba Lista.")
                    except Exception as e:
                        st.error(f"Erro ao cadastrar: {e}")

    with aba_da_sessao:
        st.markdown(
            "Salva o **estado atual da sessão** (contexto + diagnóstico + Mapa 5 Blocos + pilotos "
            "das abas 1-4) como um projeto persistente."
        )
        ctx = st.session_state.get("contexto", {})
        diag = st.session_state.get("diagnostico", {})
        mapa = st.session_state.get("mapa", {})
        pilotos = st.session_state.get("pilotos_selecionados", [])

        if not ctx.get("nome"):
            st.warning("Preencha primeiro a aba 1 (Contexto) para poder salvar.")
        else:
            st.markdown(f"**Nome de origem:** {ctx.get('nome')}")
            st.markdown(f"**Empresa:** {ctx.get('empresa')}")
            nome_projeto = st.text_input(
                "Nome no cadastro persistente",
                value=f"{ctx.get('empresa', 'Projeto')} — {ctx.get('nome', 'sem nome')}",
            )
            if st.button("💾 Salvar sessão como projeto", type="primary"):
                dados = {
                    "nome": nome_projeto,
                    "empresa": ctx.get("empresa", ""),
                    "porte": ctx.get("porte", ""),
                    "cargo_gp": ctx.get("cargo", ""),
                    "n_projetos": ctx.get("n_projetos", 0),
                    "pmo_ativo": ctx.get("pmo_ativo", False),
                    "estrategia": diag.get("estrategia", 0),
                    "dados": diag.get("dados", 0),
                    "casos_uso": diag.get("casos_uso", 0),
                    "governanca": diag.get("governanca", 0),
                    "beneficios": diag.get("beneficios", 0),
                    "mapa_contexto": mapa.get("contexto", ""),
                    "mapa_dor": mapa.get("dor", ""),
                    "mapa_dados": mapa.get("dados", ""),
                    "mapa_riscos": mapa.get("riscos", ""),
                    "mapa_valor": mapa.get("valor", ""),
                    "pilotos": [
                        {
                            "nome": p.get("nome"),
                            "impacto": p.get("scoring", {}).get("impacto", ""),
                            "viabilidade": p.get("scoring", {}).get("viabilidade", ""),
                            "risco": p.get("scoring", {}).get("risco", ""),
                        }
                        for p in pilotos
                    ],
                }
                try:
                    existente = db.obter_projeto_por_nome(nome_projeto)
                    if existente:
                        db.salvar_projeto(dados, projeto_id=existente["id"])
                        st.success(f"Projeto atualizado (id={existente['id']}).")
                    else:
                        proj_id = db.salvar_projeto(dados)
                        st.success(f"Projeto salvo (id={proj_id}). Vá para a aba Lista.")
                except Exception as e:
                    st.error(f"Erro: {e}")

    if aba_processos is None:
        return
    with aba_processos:
        st.markdown(
            "Marcar quais dos 40 processos PMBOK são críticos para o projeto ativo, "
            "e o tratamento sugerido (aplicação de IA ou gap não atendido)."
        )
        pid_ativo = st.session_state.get("projeto_ativo_id")
        if not pid_ativo:
            st.warning("Selecione um projeto no topo da aba para marcar processos.")
        else:
            projeto = db.obter_projeto(pid_ativo)
            st.info(f"Editando processos de **{projeto['nome']}**")
            processos_catalogo = mapa_pmbok.carregar_processos()
            tratamentos = db.listar_tratamentos_pmbok(pid_ativo)

            areas = sorted({p["area"] for p in processos_catalogo})
            filtro_area = st.selectbox(
                "Filtrar por área", ["(todas)"] + areas, key=f"proc_filtro_area_{pid_ativo}"
            )

            for p in processos_catalogo:
                if filtro_area != "(todas)" and p["area"] != filtro_area:
                    continue
                atual = tratamentos.get(
                    p["id"], {"tratamento": "nenhum", "criticidade": "media", "observacao": ""}
                )
                if atual["tratamento"] == "nenhum" and not atual["observacao"]:
                    label_pref = "⬜"
                else:
                    label_pref = {"ia": "🤖", "ia_po": "🧮", "gap": "⚠️"}.get(atual["tratamento"], "⬜")

                with st.expander(f"{label_pref} `{p['id']}` — {p['nome']} ({p['area']})"):
                    col_a, col_b = st.columns(2)
                    trat_novo = col_a.selectbox(
                        "Tratamento",
                        db.TRATAMENTOS,
                        index=db.TRATAMENTOS.index(atual["tratamento"]),
                        key=f"trat_{pid_ativo}_{p['id']}",
                    )
                    crit_novo = col_b.selectbox(
                        "Criticidade",
                        db.CRITICIDADES,
                        index=db.CRITICIDADES.index(atual["criticidade"]),
                        key=f"crit_{pid_ativo}_{p['id']}",
                    )
                    obs_novo = st.text_input(
                        "Observação (opcional)",
                        value=atual["observacao"],
                        key=f"obs_{pid_ativo}_{p['id']}",
                    )
                    if st.button("Salvar", key=f"save_{pid_ativo}_{p['id']}"):
                        if trat_novo == "nenhum" and not obs_novo.strip():
                            db.excluir_tratamento_pmbok(pid_ativo, p["id"])
                            st.success(f"Marcação removida de {p['id']}.")
                        else:
                            db.salvar_tratamento_pmbok(
                                pid_ativo, p["id"], trat_novo, crit_novo, obs_novo
                            )
                            st.success(f"Salvo {p['id']}.")
                        st.rerun()
