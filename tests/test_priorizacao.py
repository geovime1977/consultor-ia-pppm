"""Testes do módulo priorizacao — Aula 2 IA-PPPM."""

from src.priorizacao import (
    CRITERIO_IDS,
    CasoDeUso,
    carregar_criterios,
    carregar_empresa_alfa,
    priorizar_lote,
    quadrante,
    ranking,
    score_ponderado,
    status_prontidao,
    top_n,
)


def _caso(**over):
    base = dict(
        id="c1",
        nome="Teste",
        contexto="PMO",
        dor="atrasos",
        dados="Jira",
        decisao="priorizar sprint",
        dono="Ana Coordenadora",
        metrica_valor="redução 20% atraso",
        notas={"impacto": 5, "viabilidade": 4, "dados": 4, "risco": 3, "valor": 4},
    )
    base.update(over)
    return CasoDeUso(**base)


def test_carregar_criterios_tem_5_criterios_com_pesos_somando_1():
    c = carregar_criterios()
    assert len(c["criterios"]) == 5
    assert {x["id"] for x in c["criterios"]} == set(CRITERIO_IDS)
    assert abs(sum(x["peso"] for x in c["criterios"]) - 1.0) < 1e-9


def test_pesos_oficiais_da_aula_30_20_20_15_15():
    c = carregar_criterios()
    pesos = {x["id"]: x["peso"] for x in c["criterios"]}
    assert pesos["impacto"] == 0.30
    assert pesos["viabilidade"] == 0.20
    assert pesos["dados"] == 0.20
    assert pesos["risco"] == 0.15
    assert pesos["valor"] == 0.15


def test_score_ponderado_calculo_esperado():
    notas = {"impacto": 5, "viabilidade": 4, "dados": 4, "risco": 3, "valor": 4}
    # 5*0.30 + 4*0.20 + 4*0.20 + 3*0.15 + 4*0.15 = 1.5 + 0.8 + 0.8 + 0.45 + 0.6 = 4.15
    assert score_ponderado(notas) == 4.15


def test_score_notas_faltando_contam_zero():
    assert score_ponderado({"impacto": 5}) == round(5 * 0.30, 2)


def test_score_todas_nota_maxima_score_5():
    notas = {cid: 5 for cid in CRITERIO_IDS}
    assert score_ponderado(notas) == 5.0


def test_status_prontidao_sem_dono():
    assert status_prontidao(_caso(dono=None)).startswith("Não pronto")
    assert status_prontidao(_caso(dono="")).startswith("Não pronto")
    assert status_prontidao(_caso(dono="   ")).startswith("Não pronto")


def test_status_prontidao_com_dono():
    assert status_prontidao(_caso(dono="Ana")) == "Pronto"


def test_ranking_fazer_agora_acima_threshold():
    assert ranking(_caso(), 3.5) == "Fazer agora"
    assert ranking(_caso(), 4.15) == "Fazer agora"


def test_ranking_preparar_faixa_media():
    assert ranking(_caso(), 3.0) == "Preparar"
    assert ranking(_caso(), 2.5) == "Preparar"


def test_ranking_nao_priorizar_abaixo_threshold():
    assert ranking(_caso(), 1.5) == "Não priorizar"
    assert ranking(_caso(), 2.49) == "Não priorizar"


def test_ranking_sem_dono_forca_nao_priorizar_mesmo_score_alto():
    c = _caso(dono=None)
    assert ranking(c, 5.0) == "Não priorizar"


def test_quadrante_comece_aqui():
    assert quadrante({"impacto": 5, "viabilidade": 4}) == "Comece aqui"
    assert quadrante({"impacto": 4, "viabilidade": 5}) == "Comece aqui"


def test_quadrante_investigue():
    assert quadrante({"impacto": 5, "viabilidade": 2}) == "Investigue"


def test_quadrante_baixa_prioridade():
    assert quadrante({"impacto": 2, "viabilidade": 5}) == "Baixa prioridade"


def test_quadrante_evite_agora():
    assert quadrante({"impacto": 2, "viabilidade": 2}) == "Evite agora"


def test_priorizar_lote_ordena_por_score_desc():
    casos = [
        _caso(id="baixo", notas={cid: 2 for cid in CRITERIO_IDS}),
        _caso(id="alto", notas={cid: 5 for cid in CRITERIO_IDS}),
        _caso(id="medio", notas={cid: 3 for cid in CRITERIO_IDS}),
    ]
    r = priorizar_lote(casos)
    assert [x["id"] for x in r] == ["alto", "medio", "baixo"]


def test_priorizar_lote_marca_sem_dono_como_nao_priorizar():
    casos = [
        _caso(id="orfao", dono=None, notas={cid: 5 for cid in CRITERIO_IDS}),
    ]
    r = priorizar_lote(casos)
    assert r[0]["ranking"] == "Não priorizar"
    assert r[0]["status_prontidao"].startswith("Não pronto")


def test_top_n_retorna_3_e_exclui_nao_priorizar():
    casos = [
        _caso(id="a", notas={cid: 5 for cid in CRITERIO_IDS}),
        _caso(id="b", notas={cid: 4 for cid in CRITERIO_IDS}),
        _caso(id="c", notas={cid: 3 for cid in CRITERIO_IDS}),
        _caso(id="d", dono=None, notas={cid: 5 for cid in CRITERIO_IDS}),
    ]
    top = top_n(priorizar_lote(casos), n=3)
    ids = [x["id"] for x in top]
    assert "d" not in ids
    assert len(top) == 3


def test_empresa_alfa_seed_tem_4_casos_e_um_sem_dono():
    casos = carregar_empresa_alfa()
    assert len(casos) == 4
    ids = {c.id for c in casos}
    assert ids == {"alfa-A", "alfa-B", "alfa-C", "alfa-D"}
    sem_dono = [c for c in casos if not c.dono]
    assert len(sem_dono) == 1
    assert sem_dono[0].id == "alfa-D"


def test_ciclo_completo_empresa_alfa_produz_ranking_valido():
    casos = carregar_empresa_alfa()
    for caso in casos:
        for cid in CRITERIO_IDS:
            caso.notas[cid] = 4
    resultado = priorizar_lote(casos)
    alfa_d = next(r for r in resultado if r["id"] == "alfa-D")
    assert alfa_d["ranking"] == "Não priorizar"
    demais = [r for r in resultado if r["id"] != "alfa-D"]
    for r in demais:
        assert r["ranking"] == "Fazer agora"
