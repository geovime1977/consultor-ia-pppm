"""Seções do PDF de export que cobrem a Aula 2 (Priorização + Governança/HITL).

Chamado por src/pdf_export.py quando `dados` contém a chave "aula2".
Zero LLM, 100% determinístico.
"""

from __future__ import annotations

from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from src import governanca, priorizacao, validador_erros


_COR_H1 = colors.HexColor("#1f4e79")
_COR_H2 = colors.HexColor("#2e75b6")
_COR_HEADER_BG = colors.HexColor("#d9e1f2")
_COR_BORDA = colors.HexColor("#a6a6a6")
_COR_FAZER = colors.HexColor("#c6efce")
_COR_PREPARAR = colors.HexColor("#ffeb9c")
_COR_NAO = colors.HexColor("#f4cccc")
_COR_ALERTA_ALTA = colors.HexColor("#f4cccc")
_COR_ALERTA_MEDIA = colors.HexColor("#fff2cc")


def _tabela_casos(resultado: list[dict]) -> Table:
    header = ["Caso", "Score", "Ranking", "Quadrante", "Dono", "Prontidão"]
    dados = [header]
    for r in resultado:
        dados.append(
            [
                Paragraph(f"<b>{r['nome']}</b>", _get_body_style()),
                str(r["score"]),
                r["ranking"],
                r["quadrante"],
                r["dono"] or "—",
                r["status_prontidao"],
            ]
        )
    t = Table(dados, colWidths=[4.5 * cm, 1.5 * cm, 2.4 * cm, 2.4 * cm, 3 * cm, 3 * cm])
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), _COR_HEADER_BG),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.4, _COR_BORDA),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for i, r in enumerate(resultado, start=1):
        cor = {"Fazer agora": _COR_FAZER, "Preparar": _COR_PREPARAR, "Não priorizar": _COR_NAO}.get(r["ranking"])
        if cor:
            style.append(("BACKGROUND", (2, i), (2, i), cor))
    t.setStyle(TableStyle(style))
    return t


def _tabela_top3(top: list[dict]) -> Table:
    header = ["#", "Caso selecionado", "Score", "Ranking", "Dono"]
    dados = [header]
    for i, r in enumerate(top, start=1):
        dados.append([str(i), Paragraph(f"<b>{r['nome']}</b>", _get_body_style()), str(r["score"]), r["ranking"], r["dono"] or "—"])
    t = Table(dados, colWidths=[0.9 * cm, 7.5 * cm, 1.6 * cm, 2.6 * cm, 3.4 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), _COR_HEADER_BG),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.4, _COR_BORDA),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def _tabela_governanca(caso: priorizacao.CasoDeUso, respostas: dict, rastro: governanca.Rastro, nivel: dict) -> Table:
    dados = [
        ["Item", "Estado"],
        ["Nível HITL sugerido", f"{nivel['id'].capitalize()} — {nivel['aprovador']}"],
        ["Dados sensíveis classificados", "✅ sim" if respostas.get("dados_sensiveis") else "❌ pendente"],
        ["Acessos definidos", "✅ sim" if respostas.get("acessos") else "❌ pendente"],
        ["Ambiente seguro confirmado", "✅ sim" if respostas.get("ambiente_seguro") else "❌ pendente"],
        ["Controle de uso registrado", "✅ sim" if respostas.get("controle_uso") else "❌ pendente"],
        ["Rastro · Entrada", rastro.entrada or "—"],
        ["Rastro · Processamento", rastro.processamento or "—"],
        ["Rastro · Saída", rastro.saida or "—"],
        ["Rastro · Validação", rastro.validacao or "—"],
        ["Rastro · Registro", rastro.registro or "—"],
    ]
    t = Table(dados, colWidths=[5 * cm, 12 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), _COR_HEADER_BG),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.4, _COR_BORDA),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 1), (0, 1), _COR_HEADER_BG),
    ]))
    return t


def _get_body_style():
    from reportlab.lib.styles import ParagraphStyle
    return ParagraphStyle(
        "AulaBody",
        fontName="Helvetica",
        fontSize=9,
        leading=11,
        textColor=colors.HexColor("#333333"),
    )


def renderizar_secao_priorizacao(story: list, casos: list, styles: dict) -> None:
    """Adiciona a seção de Priorização (Aula 2) ao story do PDF."""
    if not casos:
        return
    story.append(PageBreak())
    story.append(Paragraph("Priorização de Casos de Uso · Aula 2", styles["H1"]))
    story.append(Paragraph(
        "<i>Score executivo ponderado — Impacto 30% · Viabilidade 20% · "
        "Dados 20% · Risco 15% · Valor 15%. Corte obrigatório: sem dono humano, "
        "caso não está pronto (Prof. Dr. José Bezerra, Aula 2 IA-PPPM, slide 30).</i>",
        styles["Body"],
    ))
    story.append(Spacer(1, 8))

    resultado = priorizacao.priorizar_lote(casos)

    story.append(Paragraph("Todos os casos avaliados", styles["H2"]))
    story.append(_tabela_casos(resultado))
    story.append(Spacer(1, 12))

    top = priorizacao.top_n(resultado, n=3)
    if top:
        story.append(Paragraph("Top 3 selecionados (entregável da aula)", styles["H2"]))
        story.append(_tabela_top3(top))
        story.append(Spacer(1, 12))

    # Alertas dos 5 erros
    story.append(Paragraph("Alertas dos 5 erros de IA em projetos", styles["H2"]))
    contagem = validador_erros.resumo_lote(casos)
    regras = {r["id"]: r for r in validador_erros.carregar_regras()["erros"]}
    linhas = [["Erro", "Nome", "Casos afetados"]]
    for eid in ["E1", "E2", "E3", "E4", "E5"]:
        linhas.append([eid, regras[eid]["nome"], str(contagem[eid])])
    tab = Table(linhas, colWidths=[1.4 * cm, 10 * cm, 3 * cm])
    tab.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), _COR_HEADER_BG),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.4, _COR_BORDA),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    for i, eid in enumerate(["E1", "E2", "E3", "E4", "E5"], start=1):
        if contagem[eid] > 0:
            tab.setStyle(TableStyle([
                ("BACKGROUND", (2, i), (2, i), _COR_ALERTA_ALTA if eid in ("E1", "E3", "E4") else _COR_ALERTA_MEDIA),
            ]))
    story.append(tab)


def renderizar_secao_governanca(story: list, casos: list, respostas_por_caso: dict, rastros_por_caso: dict, styles: dict) -> None:
    """Adiciona a seção de Governança + HITL (Aula 2) ao story do PDF."""
    if not casos:
        return
    story.append(PageBreak())
    story.append(Paragraph("Governança + HITL · Aula 2", styles["H1"]))
    story.append(Paragraph(
        "<i>Princípio de ouro (slide 33): quanto maior o impacto da decisão, "
        "maior a validação humana. Nível HITL puxado automaticamente da nota de "
        "impacto de cada caso.</i>",
        styles["Body"],
    ))
    story.append(Spacer(1, 8))

    for caso in casos:
        respostas = respostas_por_caso.get(caso.id, {})
        rastro = rastros_por_caso.get(caso.id, governanca.Rastro(caso_id=caso.id))
        score_imp = float((caso.notas or {}).get("impacto", 0) or 0)
        nivel = governanca.nivel_hitl(score_imp)
        diag = governanca.prontidao_governanca(respostas, rastro)

        story.append(Paragraph(f"{caso.nome}", styles["H2"]))
        status = "✅ Governança pronta para escalar" if diag["pronto"] else "⚠️ Ainda não pronto"
        story.append(Paragraph(f"<b>Status:</b> {status}", styles["Body"]))
        story.append(Spacer(1, 4))
        story.append(_tabela_governanca(caso, respostas, rastro, nivel))
        story.append(Spacer(1, 12))
