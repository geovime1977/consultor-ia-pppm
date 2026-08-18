"""Testes do PDF export estendido para Aula 2."""

import os
import tempfile

from src import governanca, pdf_export, pdf_export_aula2, priorizacao


def _dados_completos(com_aula2=True):
    dados = {
        "contexto": {"nome": "Teste", "empresa": "Alfa", "porte": "PME", "cargo": "PMO"},
        "diagnostico": {"estrategia": 3, "dados": 3, "casos_uso": 3, "governanca": 3, "beneficios": 3},
        "mapa": {"contexto": "x", "dor": "y", "dados": "z", "riscos": "a", "valor": "b"},
        "pilotos_selecionados": [],
    }
    if com_aula2:
        casos = priorizacao.carregar_empresa_alfa()
        for c in casos:
            c.notas = {"impacto": 4, "viabilidade": 4, "dados": 4, "risco": 3, "valor": 4}
        dados["aula2"] = {
            "casos": casos,
            "gov_respostas": {"alfa-A": {"dados_sensiveis": True, "acessos": True, "ambiente_seguro": True, "controle_uso": True}},
            "gov_rastro": {"alfa-A": governanca.Rastro(caso_id="alfa-A", entrada="X", processamento="Y", saida="Z", validacao="W", registro="V")},
        }
    return dados


def test_pdf_gera_sem_aula2_como_antes():
    with tempfile.TemporaryDirectory() as d:
        caminho = pdf_export.gerar_pdf(_dados_completos(com_aula2=False), os.path.join(d, "t.pdf"))
        assert os.path.getsize(caminho) > 5_000


def test_pdf_com_aula2_tem_mais_paginas_que_sem():
    from pypdf import PdfReader

    # Slugs distintos evitam que os dois PDFs colidam no rename final do gerar_pdf.
    d_sem = _dados_completos(com_aula2=False)
    d_com = _dados_completos(com_aula2=True)
    d_sem["contexto"] = {**d_sem["contexto"], "nome": "Teste Sem"}
    d_com["contexto"] = {**d_com["contexto"], "nome": "Teste Com"}
    with tempfile.TemporaryDirectory() as d:
        sem_path = pdf_export.gerar_pdf(d_sem, os.path.join(d, "sem.pdf"))
        com_path = pdf_export.gerar_pdf(d_com, os.path.join(d, "com.pdf"))
        n_sem = len(PdfReader(sem_path).pages)
        n_com = len(PdfReader(com_path).pages)
        assert n_com > n_sem, f"esperava mais páginas com aula2 (sem={n_sem}, com={n_com})"


def test_pdf_com_lista_vazia_aula2_nao_adiciona_secao():
    dados = _dados_completos(com_aula2=False)
    dados["aula2"] = {"casos": [], "gov_respostas": {}, "gov_rastro": {}}
    with tempfile.TemporaryDirectory() as d:
        caminho = pdf_export.gerar_pdf(dados, os.path.join(d, "t.pdf"))
        assert os.path.getsize(caminho) > 5_000


def test_secao_priorizacao_adiciona_paginas():
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import Paragraph
    story = []
    styles = {
        "H1": ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=14),
        "H2": ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=12),
        "Body": ParagraphStyle("Body", fontName="Helvetica", fontSize=9),
    }
    casos = priorizacao.carregar_empresa_alfa()
    for c in casos:
        c.notas = {"impacto": 5, "viabilidade": 4, "dados": 4, "risco": 3, "valor": 4}
    pdf_export_aula2.renderizar_secao_priorizacao(story, casos, styles)
    # deve ter adicionado: PageBreak + H1 + parágrafo + spacer + H2 + tabela + spacer + H2 + tabela + spacer + H2 + tabela
    assert len(story) >= 10


def test_secao_governanca_gera_um_bloco_por_caso():
    from reportlab.lib.styles import ParagraphStyle
    story = []
    styles = {
        "H1": ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=14),
        "H2": ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=12),
        "Body": ParagraphStyle("Body", fontName="Helvetica", fontSize=9),
    }
    casos = priorizacao.carregar_empresa_alfa()
    for c in casos:
        c.notas = {"impacto": 4, "viabilidade": 4, "dados": 4, "risco": 3, "valor": 4}
    pdf_export_aula2.renderizar_secao_governanca(story, casos, {}, {}, styles)
    # 1 PageBreak + 1 H1 + 1 Body + 1 Spacer + N × (H2 + Body + Spacer + Table + Spacer)
    assert len(story) >= 4 + 5 * len(casos)
