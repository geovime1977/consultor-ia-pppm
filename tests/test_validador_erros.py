"""Testes do Validador dos 5 Erros — Aula 2 IA-PPPM."""

from src.priorizacao import CRITERIO_IDS, CasoDeUso
from src.validador_erros import (
    carregar_regras,
    resumo_lote,
    validar,
    validar_lote,
)


def _caso_saudavel(**over):
    base = dict(
        id="ok",
        nome="Priorização de portfólio para comitê",
        contexto="Portfólio corporativo",
        dor="Comitê prioriza por política; alta gestão pede critério auditável para as 40 iniciativas.",
        dados="Business cases 3 anos + matriz risco corporativa + histórico aprovações",
        decisao="Ranquear iniciativas trimestralmente com score comparável.",
        dono="CIO",
        metrica_valor="Realocação de 15% do CAPEX para top 10 iniciativas",
        notas={cid: 4 for cid in CRITERIO_IDS},
    )
    base.update(over)
    return CasoDeUso(**base)


def test_carregar_regras_tem_5_erros():
    r = carregar_regras()
    assert {e["id"] for e in r["erros"]} == {"E1", "E2", "E3", "E4", "E5"}


def test_caso_saudavel_zero_alertas():
    assert validar(_caso_saudavel()) == []


def test_e1_menciona_ferramenta_sem_dor_clara():
    caso = _caso_saudavel(nome="Vamos usar GPT", dor="usar IA")
    ids = [a.erro_id for a in validar(caso)]
    assert "E1" in ids


def test_e1_ferramenta_mas_dor_bem_descrita_nao_dispara():
    caso = _caso_saudavel(
        dor="Precisamos reduzir tempo de resposta do suporte via chatbot integrado ao CRM",
    )
    ids = [a.erro_id for a in validar(caso)]
    assert "E1" not in ids


def test_e2_fascinio_tecnico_sem_metrica():
    caso = _caso_saudavel(
        nome="Agente autônomo com RAG avançado",
        metrica_valor="",
    )
    ids = [a.erro_id for a in validar(caso)]
    assert "E2" in ids


def test_e2_fascinio_com_metrica_nao_dispara():
    caso = _caso_saudavel(
        nome="Agente autônomo com RAG avançado",
        metrica_valor="Redução de 40% no tempo médio de atendimento",
    )
    ids = [a.erro_id for a in validar(caso)]
    assert "E2" not in ids


def test_e3_dados_vazios():
    caso = _caso_saudavel(dados="")
    ids = [a.erro_id for a in validar(caso)]
    assert "E3" in ids


def test_e3_dados_curtos_disparam():
    caso = _caso_saudavel(dados="planilha")
    ids = [a.erro_id for a in validar(caso)]
    assert "E3" in ids


def test_e4_sem_dono_none():
    caso = _caso_saudavel(dono=None)
    assert "E4" in [a.erro_id for a in validar(caso)]


def test_e4_sem_dono_string_vazia():
    caso = _caso_saudavel(dono="")
    assert "E4" in [a.erro_id for a in validar(caso)]


def test_e4_sem_dono_espacos():
    caso = _caso_saudavel(dono="   ")
    assert "E4" in [a.erro_id for a in validar(caso)]


def test_e5_metrica_vazia():
    caso = _caso_saudavel(metrica_valor="")
    assert "E5" in [a.erro_id for a in validar(caso)]


def test_e5_metrica_curta():
    caso = _caso_saudavel(metrica_valor="ok")
    assert "E5" in [a.erro_id for a in validar(caso)]


def test_validar_lote_retorna_dict_por_caso():
    casos = [_caso_saudavel(id="a"), _caso_saudavel(id="b", dono=None)]
    resultado = validar_lote(casos)
    assert set(resultado.keys()) == {"a", "b"}
    assert resultado["a"] == []
    assert any(al.erro_id == "E4" for al in resultado["b"])


def test_resumo_lote_conta_alertas_por_erro():
    casos = [
        _caso_saudavel(id="1", dono=None),
        _caso_saudavel(id="2", dados=""),
        _caso_saudavel(id="3", metrica_valor=""),
        _caso_saudavel(id="4"),
    ]
    r = resumo_lote(casos)
    assert r["E4"] == 1
    assert r["E3"] == 1
    assert r["E5"] == 1
    assert r["E1"] == 0
    assert r["E2"] == 0


def test_alerta_tem_severidade_alta_para_e1_e3_e4():
    caso = _caso_saudavel(dono=None, dados="", nome="usar gpt agora", dor="ia")
    sev = {a.erro_id: a.severidade for a in validar(caso)}
    assert sev.get("E1") == "alta"
    assert sev.get("E3") == "alta"
    assert sev.get("E4") == "alta"


def test_alerta_contem_correcao_de_rota_do_slide():
    caso = _caso_saudavel(dono=None)
    alertas = validar(caso)
    e4 = [a for a in alertas if a.erro_id == "E4"][0]
    assert "IA recomenda" in e4.correcao
