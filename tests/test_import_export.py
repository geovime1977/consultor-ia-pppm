"""Testes do módulo import_export — round-trip e validação de schema."""

import json

import pytest

from src.governanca import Rastro
from src.import_export import (
    SCHEMA,
    VERSAO_SCHEMA,
    ErroImportacao,
    exportar,
    exportar_json,
    importar,
    importar_json,
    resumo_importacao,
)
from src.priorizacao import CasoDeUso


def _estado_completo():
    return {
        "contexto": {"nome": "Geovane", "empresa": "Eixo", "porte": "PME"},
        "diagnostico": {"estrategia": 3, "dados": 4, "casos_uso": 2, "governanca": 3, "beneficios": 3},
        "mapa": {"contexto": "PMO corporativo", "dor": "atrasos", "dados": "Jira", "riscos": "compliance", "valor": "20% redução"},
        "pilotos_selecionados": [{"nome": "Piloto X", "descricao": "..."}],
        "aula2_casos": [
            CasoDeUso(
                id="c1", nome="Priorização portfólio",
                contexto="PMO", dor="critério auditável", dados="business cases",
                decisao="ranquear iniciativas", dono="CIO",
                metrica_valor="15% CAPEX top10",
                notas={"impacto": 5, "viabilidade": 4, "dados": 4, "risco": 3, "valor": 5},
            ),
        ],
        "aula2_gov_respostas": {"c1": {"dados_sensiveis": True, "acessos": True, "ambiente_seguro": False, "controle_uso": True}},
        "aula2_gov_rastro": {"c1": Rastro(caso_id="c1", entrada="Jira", processamento="Prompt v1", saida="ranking", validacao="Ana", registro="Ata")},
    }


def test_exportar_produz_schema_versionado():
    d = exportar(_estado_completo())
    assert d["schema"] == SCHEMA
    assert d["versao"] == VERSAO_SCHEMA
    assert "exportado_em" in d


def test_exportar_estrutura_aula1_aula2():
    d = exportar(_estado_completo())
    assert set(d["aula1"].keys()) == {"contexto", "diagnostico", "mapa", "pilotos_selecionados"}
    assert set(d["aula2"].keys()) == {"casos", "governanca"}


def test_exportar_json_string_parseavel():
    txt = exportar_json(_estado_completo())
    d = json.loads(txt)
    assert d["schema"] == SCHEMA


def test_round_trip_preserva_dados():
    original = _estado_completo()
    exportado = exportar_json(original)
    importado = importar_json(exportado)
    assert importado["contexto"]["empresa"] == "Eixo"
    assert importado["diagnostico"]["dados"] == 4
    assert len(importado["aula2_casos"]) == 1
    caso = importado["aula2_casos"][0]
    assert isinstance(caso, CasoDeUso)
    assert caso.dono == "CIO"
    assert caso.notas["impacto"] == 5
    assert importado["aula2_gov_respostas"]["c1"]["dados_sensiveis"] is True
    rastro = importado["aula2_gov_rastro"]["c1"]
    assert isinstance(rastro, Rastro)
    assert rastro.entrada == "Jira"


def test_importar_estado_vazio_produz_defaults():
    minimo = {"schema": SCHEMA, "versao": VERSAO_SCHEMA, "aula1": {}, "aula2": {}}
    r = importar(minimo)
    assert r["contexto"] == {}
    assert r["diagnostico"] == {}
    assert r["aula2_casos"] == []
    assert r["aula2_gov_rastro"] == {}


def test_importar_rejeita_schema_desconhecido():
    with pytest.raises(ErroImportacao, match="Schema desconhecido"):
        importar({"schema": "outra-coisa", "versao": "1.0"})


def test_importar_rejeita_versao_incompativel():
    with pytest.raises(ErroImportacao, match="Versão"):
        importar({"schema": SCHEMA, "versao": "2.0"})


def test_importar_rejeita_json_sem_aula1_nem_aula2():
    with pytest.raises(ErroImportacao, match="não contém"):
        importar({"schema": SCHEMA, "versao": VERSAO_SCHEMA})


def test_importar_rejeita_nao_dict_no_topo():
    with pytest.raises(ErroImportacao, match="objeto no topo"):
        importar(["lista", "no", "topo"])


def test_importar_json_rejeita_json_invalido():
    with pytest.raises(ErroImportacao, match="JSON inválido"):
        importar_json("{ nao é json valido")


def test_resumo_importacao_humano_legivel():
    estado = importar(exportar(_estado_completo()))
    txt = resumo_importacao(estado)
    assert "Eixo" in txt
    assert "1 caso" in txt or "casos: 1" in txt
    assert "Aula 2" in txt


def test_exportar_com_estado_vazio_nao_quebra():
    d = exportar({})
    assert d["aula1"]["contexto"] == {}
    assert d["aula2"]["casos"] == []


def test_round_trip_com_dono_none_preserva_none():
    estado = {
        "aula2_casos": [
            CasoDeUso(id="orfao", nome="sem dono", dono=None,
                      notas={"impacto": 5, "viabilidade": 5, "dados": 5, "risco": 5, "valor": 5}),
        ],
    }
    r = importar_json(exportar_json(estado))
    assert r["aula2_casos"][0].dono is None
