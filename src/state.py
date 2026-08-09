import streamlit as st

_SCHEMA_DEFAULT = {
    "contexto": {
        "nome": "",
        "empresa": "",
        "porte": "",
        "n_projetos": 0,
        "pmo_ativo": False,
        "cargo": "",
    },
    "diagnostico": {
        "estrategia": 0,
        "dados": 0,
        "casos_uso": 0,
        "governanca": 0,
        "beneficios": 0,
    },
    "mapa": {
        "contexto": "",
        "dor": "",
        "dados": "",
        "riscos": "",
        "valor": "",
    },
    "pilotos_selecionados": [],
    "contexto_salvo": False,
    "mapa_salvo": False,
}


def init_state() -> None:
    for key, default in _SCHEMA_DEFAULT.items():
        if key not in st.session_state:
            st.session_state[key] = default.copy() if hasattr(default, "copy") else default


def reset_state() -> None:
    for key, default in _SCHEMA_DEFAULT.items():
        st.session_state[key] = default.copy() if hasattr(default, "copy") else default


def is_step_complete(step: int) -> bool:
    from src.validators import validar_contexto, validar_diagnostico, validar_mapa

    if step == 1:
        ok, _ = validar_contexto(st.session_state.get("contexto", {}))
        return ok and st.session_state.get("contexto_salvo", False)
    if step == 2:
        ok, _ = validar_diagnostico(st.session_state.get("diagnostico", {}))
        return ok
    if step == 3:
        ok, _ = validar_mapa(st.session_state.get("mapa", {}))
        return ok and st.session_state.get("mapa_salvo", False)
    if step == 4:
        return len(st.session_state.get("pilotos_selecionados", [])) > 0
    return False


def get_all_data() -> dict:
    return {
        "contexto": dict(st.session_state.get("contexto", {})),
        "diagnostico": dict(st.session_state.get("diagnostico", {})),
        "mapa": dict(st.session_state.get("mapa", {})),
        "pilotos_selecionados": list(st.session_state.get("pilotos_selecionados", [])),
    }
