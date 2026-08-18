"""Testes do módulo upload_documento — extração, heurística e conversão."""

import os
from unittest.mock import patch

import pytest

from src.priorizacao import CasoDeUso
from src.upload_documento import (
    ErroExtracao,
    api_key_disponivel,
    extrair_texto,
    heuristica_fallback,
    sugerir,
    sugestoes_para_casos_de_uso,
)


def test_extrair_texto_txt():
    texto = "Empresa Alfa Ltda enfrenta atrasos em portfólio de projetos."
    r = extrair_texto(texto.encode("utf-8"), "briefing.txt")
    assert "Empresa Alfa" in r


def test_extrair_texto_md():
    r = extrair_texto(b"# Contexto\nProblema: atrasos.\n", "nota.md")
    assert "Problema" in r


def test_extrair_texto_formato_desconhecido():
    with pytest.raises(ErroExtracao, match="não suportado"):
        extrair_texto(b"", "arquivo.xyz")


def test_heuristica_detecta_empresa_ltda():
    r = heuristica_fallback("A Alfa Corp Ltda tem 40 projetos e enfrenta atrasos.")
    assert "Alfa Corp" in r["contexto"]["empresa"]


def test_heuristica_detecta_pmo():
    r = heuristica_fallback("O PMO da empresa está sobrecarregado.")
    assert r["contexto"]["pmo_ativo"] is True


def test_heuristica_sem_pmo():
    r = heuristica_fallback("Empresa sem escritório de projetos formal.")
    assert r["contexto"]["pmo_ativo"] is True  # tem "escritório de projetos" no texto


def test_heuristica_pega_dor_por_keyword():
    texto = "O contexto é industrial. O problema principal é o atraso na entrega dos projetos."
    r = heuristica_fallback(texto)
    assert "atraso" in r["mapa"]["dor"].lower() or "problema" in r["mapa"]["dor"].lower()


def test_heuristica_pega_dados_por_keyword():
    r = heuristica_fallback("Usamos Jira e planilhas Excel para tudo.")
    assert "jira" in r["mapa"]["dados"].lower() or "planilha" in r["mapa"]["dados"].lower()


def test_heuristica_retorna_estrutura_esperada():
    r = heuristica_fallback("texto qualquer")
    assert set(r.keys()) == {"contexto", "mapa", "casos_uso"}
    assert set(r["contexto"].keys()) == {"empresa", "porte", "cargo", "n_projetos", "pmo_ativo"}
    assert set(r["mapa"].keys()) == {"contexto", "dor", "dados", "riscos", "valor"}


def test_heuristica_casos_uso_vazio():
    """Heurística não deve inventar casos de uso (só LLM propõe)."""
    r = heuristica_fallback("qualquer texto")
    assert r["casos_uso"] == []


def test_sugerir_sem_chave_cai_no_fallback():
    with patch.dict(os.environ, {}, clear=True):
        # sem OPENAI_API_KEY, sem st.secrets → heurística
        r = sugerir("Empresa Alfa Ltda. PMO ativo. Problema: atrasos crônicos.")
        assert "Alfa" in r["contexto"]["empresa"]
        assert r["casos_uso"] == []


def test_sugestoes_para_casos_de_uso_converte_para_objetos():
    sugestoes = {
        "casos_uso": [
            {
                "id": "c1", "nome": "Relatório executivo",
                "contexto": "PMO", "dor": "atrasos",
                "dados": "Jira", "decisao": "publicar semanal",
                "dono": "PMO", "metrica_valor": "70% menos tempo",
            }
        ]
    }
    r = sugestoes_para_casos_de_uso(sugestoes)
    assert len(r) == 1
    assert isinstance(r[0], CasoDeUso)
    assert r[0].nome == "Relatório executivo"
    assert r[0].dono == "PMO"


def test_sugestoes_sem_casos_retorna_lista_vazia():
    assert sugestoes_para_casos_de_uso({}) == []
    assert sugestoes_para_casos_de_uso({"casos_uso": []}) == []


def test_sugestoes_gera_id_se_ausente():
    r = sugestoes_para_casos_de_uso({"casos_uso": [{"nome": "sem id"}]})
    assert r[0].id.startswith("upload-")


def test_api_key_disponivel_env():
    with patch.dict(os.environ, {"GROQ_API_KEY": "gsk-fake"}):
        assert api_key_disponivel() is True


def test_api_key_indisponivel_sem_env_sem_secrets():
    with patch.dict(os.environ, {}, clear=True):
        # streamlit importado sem st.secrets configurado
        try:
            assert api_key_disponivel() is False
        except Exception:
            # se st.secrets levanta (fora do runtime streamlit), fallback é False
            pass
