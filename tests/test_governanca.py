"""Testes do módulo governanca — Aula 2 IA-PPPM (slides 31-36)."""

from src.governanca import (
    Rastro,
    carregar_politica,
    checklist_seguranca,
    nivel_hitl,
    prontidao_governanca,
)


def test_carregar_politica_estrutura_completa():
    p = carregar_politica()
    assert "seguranca" in p and "etica" in p and "rastreabilidade" in p and "hitl" in p


def test_seguranca_tem_4_blocos_oficiais():
    p = carregar_politica()
    ids = {b["id"] for b in p["seguranca"]["blocos"]}
    assert ids == {"dados_sensiveis", "acessos", "ambiente_seguro", "controle_uso"}


def test_rastreabilidade_tem_5_passos_na_ordem():
    p = carregar_politica()
    fluxo = p["rastreabilidade"]["fluxo"]
    assert [f["id"] for f in fluxo] == ["entrada", "processamento", "saida", "validacao", "registro"]


def test_hitl_tem_3_papeis_da_aula():
    p = carregar_politica()
    papeis = [x["papel"] for x in p["hitl"]["papeis"]]
    assert papeis == ["IA recomenda", "Humano valida", "Gestor decide"]


def test_nivel_hitl_leve_para_score_baixo():
    n = nivel_hitl(1.5)
    assert n["id"] == "leve"


def test_nivel_hitl_moderada_para_score_medio():
    n = nivel_hitl(3.0)
    assert n["id"] == "moderada"


def test_nivel_hitl_alta_para_score_alto():
    n = nivel_hitl(4.5)
    assert n["id"] == "alta"


def test_nivel_hitl_extremo_superior_recai_em_alta():
    assert nivel_hitl(5.0)["id"] == "alta"


def test_rastro_completo_true_quando_todos_campos_preenchidos():
    r = Rastro(
        caso_id="c1",
        entrada="Jira + planilhas",
        processamento="Prompt v3 + LLM",
        saida="Ranking",
        validacao="Consultor conferiu",
        registro="Aprovado em ata",
    )
    assert r.completo() is True
    assert r.campos_faltantes() == []


def test_rastro_incompleto_lista_campos_faltantes():
    r = Rastro(caso_id="c1", entrada="Jira", saida="Ranking")
    assert r.completo() is False
    faltando = r.campos_faltantes()
    assert "processamento" in faltando
    assert "validacao" in faltando
    assert "registro" in faltando


def test_checklist_seguranca_marca_atendido():
    resp = {"dados_sensiveis": True, "acessos": True, "ambiente_seguro": False, "controle_uso": True}
    result = checklist_seguranca(resp)
    por_id = {r["id"]: r for r in result}
    assert por_id["dados_sensiveis"]["atendido"] is True
    assert por_id["ambiente_seguro"]["atendido"] is False
    assert por_id["controle_uso"]["atendido"] is True


def test_prontidao_governanca_pronto_quando_tudo_ok():
    resp = {"dados_sensiveis": True, "acessos": True, "ambiente_seguro": True, "controle_uso": True}
    rastro = Rastro(
        caso_id="c1",
        entrada="x", processamento="x", saida="x", validacao="x", registro="x",
    )
    p = prontidao_governanca(resp, rastro)
    assert p["pronto"] is True
    assert p["seguranca_ok"] is True
    assert p["rastro_ok"] is True


def test_prontidao_governanca_nao_pronto_sem_seguranca():
    resp = {"dados_sensiveis": True}
    rastro = Rastro(
        caso_id="c1",
        entrada="x", processamento="x", saida="x", validacao="x", registro="x",
    )
    p = prontidao_governanca(resp, rastro)
    assert p["pronto"] is False
    assert p["seguranca_ok"] is False
    assert "Acessos" in p["seguranca_faltando"]


def test_prontidao_governanca_nao_pronto_sem_rastro():
    resp = {"dados_sensiveis": True, "acessos": True, "ambiente_seguro": True, "controle_uso": True}
    rastro = Rastro(caso_id="c1", entrada="ok")
    p = prontidao_governanca(resp, rastro)
    assert p["pronto"] is False
    assert p["rastro_ok"] is False
    assert "validacao" in p["rastro_faltando"]
