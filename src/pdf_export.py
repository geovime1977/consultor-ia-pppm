import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from src import diagnostico as diag_mod
from src.niveis import get_nivel

_COR_H1 = colors.HexColor("#1f4e79")
_COR_H2 = colors.HexColor("#2e75b6")
_COR_BODY = colors.HexColor("#333333")
_COR_HEADER_BG = colors.HexColor("#d9e1f2")
_COR_BORDA = colors.HexColor("#a6a6a6")

_MARGEM = 2.5 * cm

_ROTULO_DIMENSAO = {
    "estrategia": "Estratégia e valor",
    "dados": "Dados e processos",
    "casos_uso": "Casos de uso",
    "governanca": "Governança e HITL",
    "beneficios": "Benefícios e ROI",
}

_ROTULO_BLOCO = {
    "contexto": "Contexto",
    "dor": "Dor",
    "dados": "Dados",
    "riscos": "Riscos",
    "valor": "Valor",
}

_RODAPE = "Método Aula 1 — Prof. Dr. José Bezerra"


def _slugify(nome: str) -> str:
    nfkd = unicodedata.normalize("NFKD", nome or "participante")
    ascii_ = "".join(c for c in nfkd if not unicodedata.combining(c))
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_).strip("-").lower()
    return slug or "participante"


def _build_styles() -> dict:
    base = getSampleStyleSheet()
    styles = {
        "H1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=_COR_H1,
            spaceAfter=12,
        ),
        "H2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=_COR_H2,
            spaceBefore=10,
            spaceAfter=6,
        ),
        "Body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            textColor=_COR_BODY,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        ),
        "BodyLeft": ParagraphStyle(
            "BodyLeft",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            textColor=_COR_BODY,
            alignment=TA_LEFT,
            spaceAfter=6,
        ),
        "Capa": ParagraphStyle(
            "Capa",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=30,
            textColor=_COR_H1,
            alignment=1,
            spaceAfter=18,
        ),
        "Subcapa": ParagraphStyle(
            "Subcapa",
            parent=base["Title"],
            fontName="Helvetica",
            fontSize=14,
            leading=18,
            textColor=_COR_BODY,
            alignment=1,
            spaceAfter=8,
        ),
        "Destaque": ParagraphStyle(
            "Destaque",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=16,
            textColor=_COR_H1,
            spaceBefore=6,
            spaceAfter=6,
        ),
    }
    return styles


def _draw_footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(_COR_BODY)
    page_num = canvas.getPageNumber()
    canvas.drawString(_MARGEM, 1.2 * cm, _RODAPE)
    canvas.drawRightString(A4[0] - _MARGEM, 1.2 * cm, f"Página {page_num}")
    canvas.restoreState()


def _tabela_contexto(ctx: dict) -> Table:
    linhas = [
        ["Campo", "Valor"],
        ["Nome", ctx.get("nome", "")],
        ["Cargo", ctx.get("cargo", "")],
        ["Empresa", ctx.get("empresa", "")],
        ["Porte", ctx.get("porte", "")],
        ["Nº de projetos ativos", str(ctx.get("n_projetos", 0))],
        ["PMO ativo", "Sim" if ctx.get("pmo_ativo") else "Não"],
    ]
    t = Table(linhas, colWidths=[6 * cm, 10 * cm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), _COR_HEADER_BG),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 11),
                ("TEXTCOLOR", (0, 0), (-1, -1), _COR_BODY),
                ("GRID", (0, 0), (-1, -1), 0.4, _COR_BORDA),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return t


def _tabela_diagnostico(diag: dict) -> Table:
    linhas = [["Dimensão", "Pontuação (0-6)"]]
    total = 0
    for chave, rotulo in _ROTULO_DIMENSAO.items():
        v = int(diag.get(chave, 0) or 0)
        total += v
        linhas.append([rotulo, str(v)])
    linhas.append(["Total", f"{total} / 30"])
    t = Table(linhas, colWidths=[10 * cm, 6 * cm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), _COR_HEADER_BG),
                ("BACKGROUND", (0, -1), (-1, -1), _COR_HEADER_BG),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 11),
                ("TEXTCOLOR", (0, 0), (-1, -1), _COR_BODY),
                ("GRID", (0, 0), (-1, -1), 0.4, _COR_BORDA),
                ("ALIGN", (1, 0), (1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return t


def _tabela_scoring(scoring: dict) -> Table:
    linhas = [
        ["Impacto", "Viabilidade", "Risco"],
        [scoring.get("impacto", "-").capitalize(), scoring.get("viabilidade", "-").capitalize(), scoring.get("risco", "-").capitalize()],
    ]
    t = Table(linhas, colWidths=[5 * cm, 5 * cm, 5 * cm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), _COR_HEADER_BG),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 11),
                ("TEXTCOLOR", (0, 0), (-1, -1), _COR_BODY),
                ("GRID", (0, 0), (-1, -1), 0.4, _COR_BORDA),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return t


_CASES_PATH = Path(__file__).resolve().parent.parent / "data" / "cases_bezerra.json"
_COMERCIAL_PATH = Path(__file__).resolve().parent.parent / "data" / "modelo_comercial_bezerra.json"


def _carregar_cases() -> list[dict]:
    if not _CASES_PATH.exists():
        return []
    with open(_CASES_PATH, encoding="utf-8") as f:
        return json.load(f).get("cases", [])


def _cases_relevantes(pilotos: list[dict], cases: list[dict], max_cases: int = 3) -> list[dict]:
    ids_pilotos = {p.get("id") for p in pilotos if p.get("id")}
    relevantes = []
    for c in cases:
        aplicaveis = set(c.get("aplicavel_aos_pilotos", []))
        if aplicaveis & ids_pilotos:
            relevantes.append(c)
        if len(relevantes) >= max_cases:
            break
    if not relevantes:
        relevantes = cases[:max_cases]
    return relevantes


def _renderizar_cases(story: list, pilotos: list[dict], styles: dict) -> None:
    cases = _carregar_cases()
    if not cases:
        return
    escolhidos = _cases_relevantes(pilotos, cases)
    if not escolhidos:
        return
    story.append(Paragraph("5. Casos que inspiram", styles["H1"]))
    story.append(
        Paragraph(
            "Casos reais compartilhados pelo Prof. Dr. José Bezerra na Aula 1 IA-PPPM (BSBr) "
            "que aderem aos pilotos recomendados neste diagnóstico.",
            styles["Body"],
        )
    )
    story.append(Spacer(1, 6))
    for c in escolhidos:
        titulo = f"{c.get('setor', 'Case')} — {c.get('porte', '')}"
        story.append(Paragraph(titulo, styles["H2"]))
        if c.get("dor"):
            story.append(Paragraph(f"<b>Dor:</b> {c['dor']}", styles["BodyLeft"]))
        if c.get("intervencao"):
            story.append(Paragraph(f"<b>Intervenção:</b> {c['intervencao']}", styles["BodyLeft"]))
        if c.get("resultado_numerico"):
            story.append(
                Paragraph(
                    f"<b>Resultado:</b> {c['resultado_numerico']}",
                    styles["Destaque"],
                )
            )
        if c.get("moral"):
            story.append(Paragraph(f"<b>Moral:</b> {c['moral']}", styles["BodyLeft"]))
        if c.get("citacao_bezerra"):
            story.append(
                Paragraph(f"<i>Fonte: {c['citacao_bezerra']}</i>", styles["BodyLeft"])
            )
        story.append(Spacer(1, 8))


def _carregar_comercial() -> dict:
    if not _COMERCIAL_PATH.exists():
        return {}
    with open(_COMERCIAL_PATH, encoding="utf-8") as f:
        return json.load(f)


def _renderizar_modelo_comercial(story: list, styles: dict) -> None:
    dados = _carregar_comercial()
    if not dados:
        return
    story.append(Paragraph("6. Como cobrar por este trabalho", styles["H1"]))
    story.append(
        Paragraph(
            "Referência de modelo comercial do Prof. Dr. José Bezerra (Aula 1 IA-PPPM, BSBr).",
            styles["Body"],
        )
    )
    story.append(Spacer(1, 6))
    for princ in dados.get("principios", []):
        story.append(Paragraph(f"• {princ}", styles["BodyLeft"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Modalidades de cobrança:", styles["H2"]))
    for m in dados.get("modalidades", []):
        story.append(Paragraph(f"<b>{m['nome']}</b>", styles["Destaque"]))
        story.append(Paragraph(m.get("descricao", ""), styles["BodyLeft"]))
        if m.get("ticket_referencia"):
            story.append(Paragraph(f"<b>Ticket de referência:</b> {m['ticket_referencia']}", styles["BodyLeft"]))
        if m.get("quando_usar"):
            story.append(Paragraph(f"<b>Quando usar:</b> {m['quando_usar']}", styles["BodyLeft"]))
        if m.get("citacao"):
            story.append(Paragraph(f"<i>{m['citacao']}</i>", styles["BodyLeft"]))
        story.append(Spacer(1, 6))
    if dados.get("regras_de_pricing"):
        story.append(Paragraph("Regras de pricing (checklist):", styles["H2"]))
        for r in dados["regras_de_pricing"]:
            story.append(Paragraph(f"✓ {r}", styles["BodyLeft"]))


def _renderizar_pilotos(story: list, pilotos: list[dict], styles: dict) -> None:
    story.append(Paragraph("4. Pilotos Recomendados", styles["H1"]))
    for idx, piloto in enumerate(pilotos, start=1):
        story.append(Paragraph(f"{idx}. {piloto['nome']}", styles["H2"]))
        story.append(Paragraph(piloto.get("descricao", ""), styles["Body"]))
        story.append(Spacer(1, 4))
        story.append(_tabela_scoring(piloto.get("scoring", {})))
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b>Pré-requisitos:</b>", styles["BodyLeft"]))
        for pr in piloto.get("pre_requisitos", []):
            story.append(Paragraph(f"• {pr}", styles["BodyLeft"]))
        story.append(Spacer(1, 4))
        story.append(
            Paragraph(f"<b>Ganho esperado:</b> {piloto.get('ganho_esperado', '')}", styles["Destaque"])
        )
        story.append(
            Paragraph(
                f"<b>Tempo estimado:</b> {piloto.get('tempo_estimado_semanas', '?')} semanas",
                styles["BodyLeft"],
            )
        )
        story.append(Spacer(1, 10))


def gerar_pdf(dados: dict, output_path: str) -> str:
    styles = _build_styles()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(output),
        pagesize=A4,
        leftMargin=_MARGEM,
        rightMargin=_MARGEM,
        topMargin=_MARGEM,
        bottomMargin=_MARGEM,
        title="Mapa Inicial de Oportunidades de IA-PPPM",
        author="BSBr — Prof. Dr. José Bezerra",
    )

    ctx = dados.get("contexto", {})
    diag = dados.get("diagnostico", {})
    mapa = dados.get("mapa", {})
    pilotos = dados.get("pilotos_selecionados", [])

    story: list = []

    story.append(Spacer(1, 4 * cm))
    story.append(Paragraph("Mapa Inicial de Oportunidades de IA-PPPM", styles["Capa"]))
    story.append(
        Paragraph(f"{ctx.get('nome', '-')} — {ctx.get('empresa', '-')}", styles["Subcapa"])
    )
    story.append(Paragraph(datetime.now().strftime("%d/%m/%Y"), styles["Subcapa"]))
    story.append(Spacer(1, 2 * cm))
    story.append(Paragraph("Do diagnóstico inicial à recomendação consultiva.", styles["Subcapa"]))
    story.append(Spacer(1, 1.2 * cm))
    story.append(
        Paragraph(
            "<i>“Quem usa IA acelera tarefas. Quem lidera IA gera valor.”</i>",
            styles["Subcapa"],
        )
    )
    story.append(
        Paragraph(
            "<i>“IA sem método vira ferramenta. IA com método vira valor.”</i>",
            styles["Subcapa"],
        )
    )
    story.append(Paragraph("— Prof. Dr. José Bezerra | BSBr", styles["Subcapa"]))
    story.append(PageBreak())

    story.append(Paragraph("1. Contexto", styles["H1"]))
    story.append(_tabela_contexto(ctx))
    story.append(PageBreak())

    story.append(Paragraph("2. Diagnóstico de Maturidade", styles["H1"]))
    story.append(_tabela_diagnostico(diag))
    total = sum(int(diag.get(k, 0) or 0) for k in _ROTULO_DIMENSAO)
    nivel = get_nivel(total)
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            f"<b>Nível {nivel['numero']} — {nivel['rotulo']}</b>",
            styles["Destaque"],
        )
    )
    story.append(Paragraph(diag_mod.leitura_executiva(diag), styles["Body"]))
    story.append(PageBreak())

    story.append(Paragraph("3. Mapa 5 Blocos", styles["H1"]))
    for chave, rotulo in _ROTULO_BLOCO.items():
        story.append(Paragraph(rotulo, styles["H2"]))
        texto = (mapa.get(chave) or "").strip() or "—"
        story.append(Paragraph(texto.replace("\n", "<br/>"), styles["Body"]))
    story.append(PageBreak())

    _renderizar_pilotos(story, pilotos, styles)
    story.append(PageBreak())

    _renderizar_cases(story, pilotos, styles)
    story.append(PageBreak())

    _renderizar_modelo_comercial(story, styles)
    story.append(PageBreak())

    aula2 = dados.get("aula2") or {}
    casos_aula2 = aula2.get("casos") or []
    if casos_aula2:
        from src import pdf_export_aula2
        pdf_export_aula2.renderizar_secao_priorizacao(story, casos_aula2, styles)
        pdf_export_aula2.renderizar_secao_governanca(
            story,
            casos_aula2,
            aula2.get("gov_respostas") or {},
            aula2.get("gov_rastro") or {},
            styles,
        )
        story.append(PageBreak())

    story.append(Paragraph("7. Próximos Passos", styles["H1"]))
    passos = [
        "Validar viabilidade técnica com TI e revisar os pré-requisitos de dados.",
        "Priorizar 1 dos 3 pilotos para MVP em 30 dias, com dono executivo formal.",
        "Definir métrica de sucesso quantitativa antes de iniciar o piloto.",
        "Agendar checkpoint em 60 dias para revisar benefícios entregues e governança.",
    ]
    for i, p in enumerate(passos, start=1):
        story.append(Paragraph(f"{i}. {p}", styles["BodyLeft"]))

    doc.build(story, onFirstPage=_draw_footer, onLaterPages=_draw_footer)

    slug = _slugify(ctx.get("nome", ""))
    data_str = datetime.now().strftime("%Y%m%d")
    nome_esperado = f"Mapa_Inicial_IA-PPPM_{slug}_{data_str}.pdf"
    destino_final = output.parent / nome_esperado
    if output.name != nome_esperado:
        output.rename(destino_final)
        return str(destino_final)
    return str(output)
