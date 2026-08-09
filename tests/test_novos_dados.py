"""Testes dos artefatos novos do consultor-ia-pppm: cases, modelo comercial, matriz."""
import json
from pathlib import Path


DATA = Path(__file__).resolve().parent.parent / "data"


def test_cases_bezerra_tem_5_casos_completos():
    d = json.load(open(DATA / "cases_bezerra.json"))
    cases = d.get("cases", [])
    assert len(cases) == 5
    for c in cases:
        for campo in ("id", "setor", "porte", "dor", "resultado_numerico", "citacao_bezerra"):
            assert c.get(campo), f"Case {c.get('id','?')} sem {campo}"


def test_modelo_comercial_5_modalidades():
    d = json.load(open(DATA / "modelo_comercial_bezerra.json"))
    modalidades = d.get("modalidades", [])
    assert len(modalidades) == 5
    for m in modalidades:
        assert m.get("nome")
        assert m.get("ticket_referencia")


def test_pilotos_json_16_pilotos():
    pilotos = json.load(open(DATA / "pilotos.json"))
    assert len(pilotos) == 16, "12 originais + 4 novos preenchendo gaps"

    novos_esperados = {
        "detector-mudanca-escopo",
        "previsor-fluxo-caixa",
        "matcher-skills-projeto",
        "monitor-utilizacao-equipe",
    }
    ids = {p["id"] for p in pilotos}
    assert novos_esperados <= ids


def test_todos_pilotos_tem_plano_projeto_30d():
    pilotos = json.load(open(DATA / "pilotos.json"))
    for p in pilotos:
        assert p.get("plano_projeto_30d"), f"Piloto {p['id']} sem plano_projeto_30d"
        plano = p["plano_projeto_30d"]
        assert plano.get("eap_macro")
        assert plano.get("cronograma_semanal")
        assert plano.get("papeis")


def test_matriz_pilotos_processos_cobre_16_pilotos():
    m = json.load(open(DATA / "matriz_pilotos_processos.json"))
    assert len(m["relacoes"]) == 16


def test_pmbok_processos_json_estrutura():
    d = json.load(open(DATA / "pmbok_processos.json"))
    processos = d["processos"]
    assert len(processos) == 40
    # 15 primeiros tem case Bezerra pelo menos
    com_case = sum(1 for p in processos if p.get("casos_bezerra"))
    assert com_case >= 15


def test_pdf_export_carrega_novos_artefatos():
    from src import pdf_export

    cases = pdf_export._carregar_cases()
    assert len(cases) == 5

    comercial = pdf_export._carregar_comercial()
    assert len(comercial.get("modalidades", [])) == 5


def test_cases_relevantes_filtra_por_pilotos():
    from src import pdf_export

    pilotos_ficticios = [{"id": "assistente-status-executivo"}]
    cases = pdf_export._carregar_cases()
    relevantes = pdf_export._cases_relevantes(pilotos_ficticios, cases, max_cases=5)
    assert len(relevantes) >= 1
    # deve incluir cases que listam assistente-status como aplicável
    ids_relevantes = {c["id"] for c in relevantes}
    esperados = {c["id"] for c in cases if "assistente-status-executivo" in c.get("aplicavel_aos_pilotos", [])}
    assert esperados <= ids_relevantes


def test_niveis_json_tem_taglines_bezerra():
    niveis = json.load(open(DATA / "niveis.json"))
    assert len(niveis) == 5
    # nível 1 deve mencionar Bezerra em algum ponto
    txt = json.dumps(niveis, ensure_ascii=False)
    assert "Bezerra" in txt or "IA sem método" in txt or "Dado é ouro" in txt
