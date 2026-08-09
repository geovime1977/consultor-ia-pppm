import pytest

from src.diagnostico import calcular_nivel, calcular_total, identificar_gargalo


def _diag(estrategia=0, dados=0, casos_uso=0, governanca=0, beneficios=0):
    return {
        "estrategia": estrategia,
        "dados": dados,
        "casos_uso": casos_uso,
        "governanca": governanca,
        "beneficios": beneficios,
    }


def test_total_soma_todas_dimensoes():
    diag = _diag(4, 3, 2, 1, 2)
    assert calcular_total(diag) == 12


def test_total_com_zeros():
    assert calcular_total(_diag()) == 0


def test_total_maximo():
    assert calcular_total(_diag(6, 6, 6, 6, 6)) == 30


@pytest.mark.parametrize(
    "total, esperado_numero, esperado_rotulo",
    [
        (0, 1, "Ausente"),
        (6, 1, "Ausente"),
        (7, 2, "Reativo"),
        (12, 2, "Reativo"),
        (13, 3, "Experimental"),
        (18, 3, "Experimental"),
        (19, 4, "Definido"),
        (24, 4, "Definido"),
        (25, 5, "Otimizado"),
        (30, 5, "Otimizado"),
    ],
)
def test_faixas_de_nivel(total, esperado_numero, esperado_rotulo):
    nivel = calcular_nivel(total)
    assert nivel["numero"] == esperado_numero
    assert nivel["rotulo"] == esperado_rotulo


def test_gargalo_menor_dimensao():
    diag = _diag(estrategia=4, dados=3, casos_uso=2, governanca=1, beneficios=2)
    assert identificar_gargalo(diag) == "governanca"


def test_gargalo_empate_prioriza_governanca():
    diag = _diag(estrategia=1, dados=1, casos_uso=1, governanca=1, beneficios=1)
    assert identificar_gargalo(diag) == "governanca"


def test_gargalo_empate_dados_vs_estrategia_prioriza_dados():
    diag = _diag(estrategia=2, dados=2, casos_uso=5, governanca=5, beneficios=5)
    assert identificar_gargalo(diag) == "dados"


def test_gargalo_empate_casos_uso_vs_beneficios_prioriza_casos_uso():
    diag = _diag(estrategia=5, dados=5, casos_uso=1, governanca=5, beneficios=1)
    assert identificar_gargalo(diag) == "casos_uso"
