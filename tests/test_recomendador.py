from src.recomendador import (
    carregar_catalogo,
    extrair_categorias_dor,
    recomendar,
    scoring_piloto,
)


def _diag(estrategia=3, dados=3, casos_uso=3, governanca=3, beneficios=3):
    return {
        "estrategia": estrategia,
        "dados": dados,
        "casos_uso": casos_uso,
        "governanca": governanca,
        "beneficios": beneficios,
    }


def _mapa(dor=""):
    return {"contexto": "x" * 40, "dor": dor, "dados": "x" * 40, "riscos": "x" * 40, "valor": "x" * 40}


def test_match_direto_com_gargalo_governanca():
    diag = _diag(estrategia=5, dados=5, casos_uso=5, governanca=1, beneficios=5)
    mapa = _mapa(dor="Precisamos de governança e validação humana antes de escalar.")
    resultado = recomendar(diag, mapa, top_n=3)
    dimensoes_topo = resultado[0]["dimensoes_alvo"]
    assert "governanca" in dimensoes_topo


def test_match_por_dor_reporting_traz_status_executivo():
    diag = _diag(estrategia=5, dados=5, casos_uso=5, governanca=5, beneficios=5)
    mapa = _mapa(
        dor="Diretoria cobra status executivo consolidado. Relatórios espalhados e planilhas conflitantes."
    )
    resultado = recomendar(diag, mapa, top_n=3)
    ids = [p["id"] for p in resultado]
    assert "assistente-status-executivo" in ids


def test_fallback_complementa_quando_top_n_maior_que_matches():
    diag = _diag(estrategia=4, dados=4, casos_uso=4, governanca=4, beneficios=4)
    mapa = _mapa(dor="")
    resultado = recomendar(diag, mapa, top_n=8)
    assert len(resultado) == 8, "Fallback deve preencher até atingir top_n"
    catalogo = carregar_catalogo()
    ids_seguros = {
        p["id"]
        for p in catalogo
        if p["viabilidade_base"] == "alto" and p["risco_base"] == "baixo"
    }
    ids_resultado = {p["id"] for p in resultado}
    assert ids_resultado & ids_seguros, "Fallback deveria trazer ao menos um piloto viab=alto/risco=baixo"


def test_fallback_recomendacao_sempre_devolve_no_minimo_top_n():
    diag = _diag(estrategia=6, dados=6, casos_uso=6, governanca=6, beneficios=6)
    mapa = _mapa(dor="")
    resultado = recomendar(diag, mapa, top_n=3)
    assert len(resultado) == 3


def test_scoring_ajusta_viabilidade_para_baixo_em_nivel_baixo():
    catalogo = carregar_catalogo()
    piloto_alta_viab = next(p for p in catalogo if p["viabilidade_base"] == "alto")
    scoring_maduro = scoring_piloto(piloto_alta_viab, nivel=5, categorias_dor=[])
    scoring_imaturo = scoring_piloto(piloto_alta_viab, nivel=1, categorias_dor=[])
    assert scoring_maduro["viabilidade"] == "alto"
    assert scoring_imaturo["viabilidade"] == "medio"


def test_scoring_sobe_impacto_quando_dor_bate_forte():
    catalogo = carregar_catalogo()
    piloto_impacto_medio = next(
        p
        for p in catalogo
        if p["impacto_base"] == "medio" and len(p["categorias_dor"]) >= 2
    )
    scoring_sem_dor = scoring_piloto(piloto_impacto_medio, nivel=3, categorias_dor=[])
    scoring_com_dor = scoring_piloto(
        piloto_impacto_medio, nivel=3, categorias_dor=piloto_impacto_medio["categorias_dor"]
    )
    assert scoring_sem_dor["impacto"] == "medio"
    assert scoring_com_dor["impacto"] == "alto"


def test_extrair_categorias_dor_normaliza_acentos():
    categorias = extrair_categorias_dor(
        "Precisamos consolidar STATUS e melhorar priorização do portfolio."
    )
    assert "comunicacao_stakeholder" in categorias
    assert "priorizacao" in categorias


def test_recomendar_devolve_no_maximo_top_n():
    diag = _diag()
    mapa = _mapa(dor="atrasos, risco, priorizar, roi, sla, ata, dependência, satisfação, estimativa")
    resultado = recomendar(diag, mapa, top_n=3)
    assert len(resultado) == 3
    for p in resultado:
        assert "scoring" in p
        assert set(p["scoring"].keys()) == {"impacto", "viabilidade", "risco"}
