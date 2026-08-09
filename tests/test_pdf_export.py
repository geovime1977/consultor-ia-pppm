import tempfile
from pathlib import Path

from pypdf import PdfReader

from src.pdf_export import gerar_pdf
from src.recomendador import recomendar


def _dados_completos():
    contexto = {
        "nome": "Ana Ribeiro",
        "empresa": "Empresa Alfa",
        "porte": "Média",
        "n_projetos": 28,
        "pmo_ativo": True,
        "cargo": "Gerente de PMO",
    }
    diagnostico = {
        "estrategia": 4,
        "dados": 3,
        "casos_uso": 2,
        "governanca": 1,
        "beneficios": 2,
    }
    mapa = {
        "contexto": "Programa de Excelência Operacional do PMO com 28 projetos ativos monitorados.",
        "dor": "Baixa previsibilidade, atrasos recorrentes e planilhas conflitantes na diretoria.",
        "dados": "Cronogramas, status reports, atas, tickets, SLA, faturamento e histórico de riscos.",
        "riscos": "Dados sensíveis, LGPD, alucinação, decisões sem validação humana.",
        "valor": "Reduzir atrasos, melhorar SLA, priorizar ações e fortalecer a governança executiva.",
    }
    pilotos = recomendar(diagnostico, mapa, top_n=3)
    return {
        "contexto": contexto,
        "diagnostico": diagnostico,
        "mapa": mapa,
        "pilotos_selecionados": pilotos,
    }


def test_gera_pdf_valido():
    dados = _dados_completos()
    with tempfile.TemporaryDirectory() as tmp:
        destino = Path(tmp) / "mapa_temp.pdf"
        caminho = gerar_pdf(dados, str(destino))
        p = Path(caminho)
        assert p.exists(), "PDF não foi gerado"
        assert p.stat().st_size > 5_000, "PDF gerado com tamanho suspeitamente pequeno"


def test_pdf_tem_mais_de_5_paginas():
    dados = _dados_completos()
    with tempfile.TemporaryDirectory() as tmp:
        destino = Path(tmp) / "mapa_temp.pdf"
        caminho = gerar_pdf(dados, str(destino))
        reader = PdfReader(caminho)
        assert len(reader.pages) >= 5, f"Esperado >= 5 páginas, obtido {len(reader.pages)}"


def test_pdf_usa_nome_slugificado():
    dados = _dados_completos()
    with tempfile.TemporaryDirectory() as tmp:
        destino = Path(tmp) / "mapa_temp.pdf"
        caminho = gerar_pdf(dados, str(destino))
        nome = Path(caminho).name
        assert nome.startswith("Mapa_Inicial_IA-PPPM_ana-ribeiro_")
        assert nome.endswith(".pdf")
