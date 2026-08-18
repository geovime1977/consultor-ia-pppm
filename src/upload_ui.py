"""Aba 11 · Upload de documento com auto-preenchimento."""

from __future__ import annotations

import streamlit as st

from src import priorizacao_ui, upload_documento


def _painel_status_chave() -> None:
    if upload_documento.api_key_disponivel():
        st.success(
            "🔑 Chave OpenAI detectada — as sugestões vão ser feitas por IA "
            "(modelo `gpt-4o-mini`, baixo custo)."
        )
    else:
        st.warning(
            "⚠️ **Sem chave OpenAI configurada.** O upload ainda funciona, "
            "mas as sugestões usam apenas heurísticas simples (regex + keywords). "
            "Para ativar a IA:\n\n"
            "1. Peça ao dono do app (ou você) configurar `OPENAI_API_KEY` "
            "em **Settings → Secrets** do Streamlit Cloud.\n"
            "2. Ou defina a variável de ambiente `OPENAI_API_KEY` se rodando local."
        )


def _preview_sugestoes(sugestoes: dict) -> None:
    ctx = sugestoes.get("contexto", {}) or {}
    mapa = sugestoes.get("mapa", {}) or {}
    casos = sugestoes.get("casos_uso", []) or []
    with st.container(border=True):
        st.markdown("**Contexto identificado**")
        c1, c2, c3 = st.columns(3)
        c1.metric("Empresa", ctx.get("empresa") or "—")
        c2.metric("Porte", ctx.get("porte") or "—")
        c3.metric("PMO ativo", "Sim" if ctx.get("pmo_ativo") else "Não")
    with st.container(border=True):
        st.markdown("**Mapa 5 Blocos sugerido**")
        for k, rot in [("contexto", "Contexto"), ("dor", "Dor"), ("dados", "Dados"), ("riscos", "Riscos"), ("valor", "Valor")]:
            v = (mapa.get(k) or "").strip()
            st.markdown(f"**{rot}:** {v if v else '_(não identificado)_'}")
    with st.container(border=True):
        st.markdown(f"**Casos de uso propostos ({len(casos)})**")
        if not casos:
            st.caption("Nenhum caso proposto — provável falta de contexto ou chave OpenAI.")
        for i, c in enumerate(casos, start=1):
            with st.expander(f"{i}. {c.get('nome', '(sem nome)')}"):
                st.markdown(f"**Dor:** {c.get('dor') or '_(vazio)_'}")
                st.markdown(f"**Dados:** {c.get('dados') or '_(vazio)_'}")
                st.markdown(f"**Decisão:** {c.get('decisao') or '_(vazio)_'}")
                st.markdown(f"**Dono sugerido:** {c.get('dono') or '_(vazio — atenção Erro E4)_'}")
                st.markdown(f"**Métrica de valor:** {c.get('metrica_valor') or '_(vazio)_'}")


def render() -> None:
    st.subheader("11. Auto-preencher a partir de documento (upload)")
    st.caption(
        "Envie um PDF, DOCX ou TXT (briefing, termo de abertura, ata, "
        "descrição de projeto) e o app sugere preenchimento das abas "
        "2 (Contexto), 4 (Mapa 5 Blocos) e 9 (Casos da Aula 2). "
        "**Você sempre revisa antes de aplicar.**"
    )
    _painel_status_chave()

    arquivo = st.file_uploader(
        "Escolha o arquivo (PDF, DOCX, TXT ou MD)",
        type=["pdf", "docx", "txt", "md"],
        key="upload_doc_file",
    )
    if arquivo is None:
        st.info("Aguardando upload…")
        return

    try:
        texto = upload_documento.extrair_texto(arquivo.read(), arquivo.name)
    except upload_documento.ErroExtracao as e:
        st.error(f"❌ Falha ao ler o arquivo: {e}")
        return
    if not texto or len(texto.strip()) < 40:
        st.warning("Texto extraído está muito curto (<40 caracteres). Confira o arquivo.")
        return
    st.success(f"✅ Texto extraído com sucesso · {len(texto):,} caracteres.")
    with st.expander("Ver texto extraído (primeiros 2000 caracteres)"):
        st.text(texto[:2000] + ("…" if len(texto) > 2000 else ""))

    if st.button("🧠 Analisar e sugerir preenchimento", type="primary", use_container_width=True):
        with st.spinner("Analisando…"):
            sugestoes = upload_documento.sugerir(texto)
        st.session_state["upload_sugestoes"] = sugestoes

    sugestoes = st.session_state.get("upload_sugestoes")
    if not sugestoes:
        return

    st.markdown("---")
    st.markdown("### 👀 Revise as sugestões antes de aplicar")
    _preview_sugestoes(sugestoes)

    st.markdown("---")
    st.markdown("### ✅ Aplicar sugestões ao app")
    st.caption(
        "Aplique somente o que fizer sentido. Cada botão joga a sugestão no "
        "session_state da aba correspondente."
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Aplicar Contexto (aba 2)", use_container_width=True):
            ctx_novo = sugestoes.get("contexto", {}) or {}
            ctx_atual = dict(st.session_state.get("contexto") or {})
            for k, v in ctx_novo.items():
                if v not in (None, "", 0, False):
                    ctx_atual[k] = v
            st.session_state["contexto"] = ctx_atual
            st.success("Contexto atualizado. Confira na aba 2.")
    with col2:
        if st.button("Aplicar Mapa 5 Blocos (aba 4)", use_container_width=True):
            mapa_novo = sugestoes.get("mapa", {}) or {}
            mapa_atual = dict(st.session_state.get("mapa") or {})
            for k, v in mapa_novo.items():
                if v and str(v).strip():
                    mapa_atual[k] = v
            st.session_state["mapa"] = mapa_atual
            st.success("Mapa 5 Blocos atualizado. Confira na aba 4.")
    with col3:
        if st.button("Aplicar Casos de Uso (aba 9)", use_container_width=True):
            novos = upload_documento.sugestoes_para_casos_de_uso(sugestoes)
            existentes = list(st.session_state.get(priorizacao_ui.STATE_KEY) or [])
            st.session_state[priorizacao_ui.STATE_KEY] = existentes + novos
            st.success(f"{len(novos)} caso(s) adicionado(s). Confira na aba 9.")

    st.markdown("---")
    st.caption(
        "⚠️ **Lembre-se do método:** nada substitui sua leitura crítica. "
        "As sugestões da IA são ponto de partida, não decisão final. "
        "Revise, ajuste, e aplique só o que faz sentido no seu contexto."
    )
