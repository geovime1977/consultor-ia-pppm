from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import cm, inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

NAVY = HexColor('#1F4E79')
ORANGE = HexColor('#ED7D31')
WHITE = HexColor('#FFFFFF')
DARK = HexColor('#1F1F1F')
GREY = HexColor('#666666')
LIGHT = HexColor('#F2F2F2')
LIGHT_TEXT = HexColor('#E8E8E8')

PAGE = (13.333 * inch, 7.5 * inch)
W, H = PAGE
FOOTER = "consultor-ia-pppm  ·  Geovane Virmecati  ·  Eixo Estratégico"

c = canvas.Canvas("/Users/virmecati/projetos/consultor-ia-pppm/docs/DECK-PALESTRA.pdf", pagesize=PAGE)


def fill_bg(color):
    c.setFillColor(color)
    c.rect(0, 0, W, H, stroke=0, fill=1)


def side_accent():
    c.setFillColor(ORANGE)
    c.rect(0, 0, 0.35 * inch, H, stroke=0, fill=1)


def top_accent():
    c.setFillColor(ORANGE)
    c.rect(0.6 * inch, H - 0.65 * inch, 1.2 * inch, 0.08 * inch, stroke=0, fill=1)


def footer(page_num, total=10):
    c.setFillColor(GREY)
    c.setFont("Helvetica", 9)
    c.drawString(0.6 * inch, 0.4 * inch, FOOTER)
    c.drawRightString(W - 0.6 * inch, 0.4 * inch, f"{page_num} / {total}")


def title(text, y=None, size=32, color=NAVY, x=0.6 * inch, bold=True):
    if y is None:
        y = H - 1.1 * inch
    c.setFillColor(color)
    c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
    c.drawString(x, y, text)


def subtitle(text, y=None, size=16, color=GREY, x=0.6 * inch):
    if y is None:
        y = H - 1.8 * inch
    c.setFillColor(color)
    c.setFont("Helvetica", size)
    c.drawString(x, y, text)


def round_rect(x, y, w, h, fill, stroke=None, stroke_w=1, radius=8):
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(stroke_w)
        c.roundRect(x, y, w, h, radius, stroke=1, fill=1)
    else:
        c.roundRect(x, y, w, h, radius, stroke=0, fill=1)


def text_center(x_center, y, text, font="Helvetica", size=12, color=DARK, bold=False):
    fname = "Helvetica-Bold" if bold else font
    c.setFont(fname, size)
    c.setFillColor(color)
    c.drawCentredString(x_center, y, text)


def text_wrap(x, y, text, w, size=12, color=DARK, font="Helvetica", leading=None):
    if leading is None:
        leading = size * 1.3
    c.setFont(font, size)
    c.setFillColor(color)
    words = text.split()
    line = ""
    yy = y
    for word in words:
        test = (line + " " + word).strip()
        if c.stringWidth(test, font, size) <= w:
            line = test
        else:
            c.drawString(x, yy, line)
            yy -= leading
            line = word
    if line:
        c.drawString(x, yy, line)
    return yy


# ============================================================
# SLIDE 1 — Capa
# ============================================================
fill_bg(NAVY)
side_accent()

c.setFillColor(WHITE)
c.setFont("Helvetica-Bold", 52)
c.drawString(1.0 * inch, H - 2.8 * inch, "Do método à ferramenta")

c.setFillColor(ORANGE)
c.setFont("Helvetica-Bold", 38)
c.drawString(1.0 * inch, H - 3.6 * inch, "consultor-ia-pppm")

c.setFillColor(LIGHT_TEXT)
c.setFont("Helvetica", 18)
c.drawString(1.0 * inch, H - 4.4 * inch, "Um app que materializa o método da Aula 1 do Prof. Dr. José Bezerra")

c.setFillColor(LIGHT_TEXT)
c.setFont("Helvetica", 12)
c.drawString(1.0 * inch, 0.6 * inch, "Geovane Virmecati  ·  Eixo Estratégico  ·  Formação de Consultores em IA aplicada ao PPPM — BSBr")
c.showPage()


# ============================================================
# SLIDE 2 — Provocação
# ============================================================
fill_bg(WHITE)
top_accent()
title("A provocação")
subtitle("Vocês acabaram de ver um método. Agora vão ver ele virado ferramenta em 5 minutos.")

# quote box
qbx = 1.5 * inch; qby = 2.5 * inch; qbw = W - 3.0 * inch; qbh = 2.0 * inch
round_rect(qbx, qby, qbw, qbh, NAVY, radius=12)
text_center(W / 2, qby + qbh - 0.8 * inch,
            '"IA sem método vira ferramenta. IA com método vira valor."',
            size=20, color=WHITE, bold=True)
text_center(W / 2, qby + 0.5 * inch,
            "Prof. Dr. José Bezerra · Aula 1 · slide 22",
            size=11, color=HexColor("#C0C0C0"))

footer(2)
c.showPage()


# ============================================================
# SLIDE 3 — O que o app faz
# ============================================================
fill_bg(WHITE)
top_accent()
title("O que o app faz")
subtitle("Fluxo em 5 etapas — o mesmo método da Empresa Alfa, com os dados do participante.")

steps = [
    ("1", "Contexto", "empresa, porte,", "projetos, PMO"),
    ("2", "Diagnóstico", "5 dimensões", "× 0-6 pontos"),
    ("3", "Mapa 5 Blocos", "Contexto, Dor,", "Dados, Riscos, Valor"),
    ("4", "3 Pilotos", "recomendação", "determinística"),
    ("5", "PDF", "entregável", "executivo"),
]
box_w = 2.3 * inch; box_h = 2.6 * inch; gap = 0.15 * inch
total_w = 5 * box_w + 4 * gap
start_x = (W - total_w) / 2
top_y = 2.0 * inch

for i, (num, ttl, d1, d2) in enumerate(steps):
    x = start_x + i * (box_w + gap)
    round_rect(x, top_y, box_w, box_h, LIGHT, stroke=NAVY, stroke_w=1.5)
    text_center(x + box_w / 2, top_y + box_h - 0.6 * inch, num, size=28, color=ORANGE, bold=True)
    text_center(x + box_w / 2, top_y + box_h - 1.1 * inch, ttl, size=15, color=NAVY, bold=True)
    text_center(x + box_w / 2, top_y + box_h - 1.7 * inch, d1, size=11, color=DARK)
    text_center(x + box_w / 2, top_y + box_h - 2.0 * inch, d2, size=11, color=DARK)

text_center(W / 2, 1.2 * inch, "Tempo total do participante: ~10 minutos", size=14, color=ORANGE)
footer(3)
c.showPage()


# ============================================================
# SLIDE 4 — Demo ao vivo
# ============================================================
fill_bg(NAVY)
c.setFillColor(WHITE)
c.setFont("Helvetica-Bold", 60)
tw = c.stringWidth("Demo ao vivo", "Helvetica-Bold", 60)
c.drawString((W - tw) / 2, H - 3.5 * inch, "Demo ao vivo")

c.setFillColor(LIGHT_TEXT)
c.setFont("Helvetica-Oblique", 20)
tw = c.stringWidth("Vou rodar aqui — na minha máquina, offline, sem chamar API.", "Helvetica-Oblique", 20)
c.drawString((W - tw) / 2, H - 4.5 * inch, "Vou rodar aqui — na minha máquina, offline, sem chamar API.")

c.setFillColor(ORANGE)
c.setFont("Courier-Bold", 24)
tw = c.stringWidth("http://localhost:8512", "Courier-Bold", 24)
c.drawString((W - tw) / 2, H - 5.8 * inch, "http://localhost:8512")

c.showPage()


# ============================================================
# SLIDE 5 — Pipeline formal
# ============================================================
fill_bg(WHITE)
top_accent()
title("Como foi construído — pipeline formal")
subtitle('Não foi "prompt aleatório para IA". Foi processo com etapas, gates e validação humana.')

etapas = [("1","Backlog"),("2","Triagem"),("3","Especificação"),("4","Arquitetura"),
          ("5","Construção"),("6","Validação"),("7","Deploy"),("8","Documentação")]
box_w = 2.75 * inch; box_h = 1.5 * inch; gap_h = 0.15 * inch; gap_v = 0.35 * inch
row_total = 4 * box_w + 3 * gap_h
row_start = (W - row_total) / 2
row_top = 4.5 * inch

for i, (num, nome) in enumerate(etapas):
    row = i // 4; col = i % 4
    x = row_start + col * (box_w + gap_h)
    y = row_top - row * (box_h + gap_v)
    round_rect(x, y, box_w, box_h, LIGHT, stroke=NAVY, stroke_w=1)
    text_center(x + box_w / 2, y + box_h / 2 - 6, f"{num}. {nome}", size=18, color=NAVY, bold=True)

text_center(W / 2, 0.85 * inch,
            "Cada etapa produziu artefato — arquitetura em 17 KB de markdown ANTES da primeira linha de código.",
            size=13, color=GREY)
footer(5)
c.showPage()


# ============================================================
# SLIDE 6 — Agentes especializados
# ============================================================
fill_bg(WHITE)
top_accent()
title("Agentes especializados, não IA generalista")
subtitle("Cada agente com uma responsabilidade única + validação humana (HITL) entre etapas.")

agentes = [
    ("architect", "Desenhou a arquitetura", "estrutura, módulos, schemas, regras"),
    ("builder", "Implementou o código", "24 arquivos Python + 3 JSON"),
    ("vault-writer", "Documentou no Obsidian", "nota estruturada com frontmatter"),
    ("librarian", "Validou a documentação", "checou índice, tags, links"),
]

row_start_y = H - 2.9 * inch
row_h = 0.85 * inch; row_gap = 0.15 * inch
for i, (nome, papel, detalhe) in enumerate(agentes):
    y = row_start_y - i * (row_h + row_gap)
    # nome do agente (esquerda)
    round_rect(0.9 * inch, y, 2.8 * inch, row_h, NAVY, radius=6)
    text_center(0.9 * inch + 1.4 * inch, y + row_h / 2 - 6, nome,
                size=16, color=WHITE, font="Courier-Bold", bold=True)
    # papel
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(4.0 * inch, y + row_h / 2 - 6, papel)
    # detalhe
    c.setFillColor(GREY)
    c.setFont("Helvetica-Oblique", 13)
    c.drawString(8.6 * inch, y + row_h / 2 - 5, detalhe)

text_center(W / 2, 0.85 * inch,
            "Nenhum agente sabia o que o outro estava fazendo. Escopo restrito = auditabilidade.",
            size=13, color=ORANGE)
footer(6)
c.showPage()


# ============================================================
# SLIDE 7 — Zero LLM em produção
# ============================================================
fill_bg(WHITE)
top_accent()
title("A decisão contraintuitiva")

# ZERO gigante
c.setFillColor(ORANGE)
c.setFont("Helvetica-Bold", 120)
tw = c.stringWidth("ZERO", "Helvetica-Bold", 120)
c.drawString((W - tw) / 2, H - 3.8 * inch, "ZERO")

c.setFillColor(NAVY)
c.setFont("Helvetica-Bold", 24)
tw = c.stringWidth("chamadas de LLM em produção", "Helvetica-Bold", 24)
c.drawString((W - tw) / 2, H - 4.4 * inch, "chamadas de LLM em produção")

# 3 badges
badges = ["AUDITÁVEL", "GRATUITO", "RASTREÁVEL"]
bw = 3.2 * inch; bh = 0.8 * inch; bg = 0.4 * inch
btot = 3 * bw + 2 * bg
bstart = (W - btot) / 2
by = 1.4 * inch
for i, txt in enumerate(badges):
    x = bstart + i * (bw + bg)
    round_rect(x, by, bw, bh, NAVY, radius=10)
    text_center(x + bw / 2, by + bh / 2 - 6, txt, size=18, color=WHITE, bold=True)

text_center(W / 2, 0.85 * inch,
            "Recomendador de pilotos é regra matemática, não modelo estatístico. Diretoria consegue auditar.",
            size=13, color=GREY)
footer(7)
c.showPage()


# ============================================================
# SLIDE 8 — Camada meta
# ============================================================
fill_bg(WHITE)
top_accent()
title("3 frases da aula → 3 decisões do projeto")
subtitle("A camada meta: o próprio app é caso vivo do que a aula ensina.")

pares = [
    ('"IA com método vira valor."', "Pipeline formal + 28 testes automatizados"),
    ('"Governança e HITL são o gargalo."', "Agentes com escopo restrito + validação humana entre etapas"),
    ('"Diagnóstico revela oportunidade."', "App respeita o espaço que o professor deixou para próximas aulas"),
]
row_top_y = H - 3.0 * inch
row_h = 1.0 * inch; row_gap = 0.3 * inch
for i, (frase, decisao) in enumerate(pares):
    y = row_top_y - i * (row_h + row_gap)
    # esquerda — aula
    round_rect(0.9 * inch, y, 5.4 * inch, row_h, NAVY, radius=8)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Oblique", 14)
    text_wrap(1.15 * inch, y + row_h - 0.4 * inch, frase, 5.0 * inch, size=14, color=WHITE, font="Helvetica-Oblique")
    # seta
    text_center(6.6 * inch, y + row_h / 2 - 8, "→", size=26, color=ORANGE, bold=True)
    # direita — decisão
    round_rect(6.9 * inch, y, 5.6 * inch, row_h, LIGHT, stroke=ORANGE, stroke_w=1.5, radius=8)
    text_wrap(7.15 * inch, y + row_h - 0.4 * inch, decisao, 5.2 * inch, size=13, color=DARK, font="Helvetica-Bold")

footer(8)
c.showPage()


# ============================================================
# SLIDE 9 — Números
# ============================================================
fill_bg(WHITE)
top_accent()
title("Números do projeto")
subtitle("Reproduzível. Barato. Rastreável.")

numeros = [
    ("~1h", "do 'começa' ao", "PDF funcionando"),
    ("12", "arquivos Python", "+ 3 JSON"),
    ("28/28", "testes", "automatizados"),
    ("0", "chamadas de IA", "por execução"),
    ("R$ 0", "custo", "por uso"),
    ("100%", "código aberto", "determinístico"),
]
box_w = 3.9 * inch; box_h = 1.8 * inch; gap_h = 0.15 * inch; gap_v = 0.2 * inch
row_total = 3 * box_w + 2 * gap_h
row_start_x = (W - row_total) / 2
row_top_y = 4.4 * inch

for i, (n, l1, l2) in enumerate(numeros):
    row = i // 3; col = i % 3
    x = row_start_x + col * (box_w + gap_h)
    y = row_top_y - row * (box_h + gap_v)
    round_rect(x, y, box_w, box_h, LIGHT, stroke=NAVY, stroke_w=1)
    text_center(x + box_w / 2, y + box_h - 0.7 * inch, n, size=36, color=ORANGE, bold=True)
    text_center(x + box_w / 2, y + box_h - 1.25 * inch, l1, size=12, color=DARK)
    text_center(x + box_w / 2, y + box_h - 1.55 * inch, l2, size=12, color=DARK)

text_center(W / 2, 0.85 * inch,
            "Repositório: github.com/geovime1977/consultor-ia-pppm  ·  Backup: OneDrive Eixo Estratégico",
            size=11, color=GREY)
footer(9)
c.showPage()


# ============================================================
# SLIDE 10 — Fechamento
# ============================================================
fill_bg(NAVY)
side_accent()

c.setFillColor(WHITE)
c.setFont("Helvetica-Bold", 38)
tw = c.stringWidth("IA foi usada NA construção.", "Helvetica-Bold", 38)
c.drawString((W - tw) / 2, H - 3.2 * inch, "IA foi usada NA construção.")

c.setFillColor(ORANGE)
c.setFont("Helvetica-Bold", 38)
tw = c.stringWidth("Não na operação.", "Helvetica-Bold", 38)
c.drawString((W - tw) / 2, H - 3.9 * inch, "Não na operação.")

c.setFillColor(LIGHT_TEXT)
c.setFont("Helvetica-Oblique", 18)
tw = c.stringWidth("É essa a diferença que este curso está formando.", "Helvetica-Oblique", 18)
c.drawString((W - tw) / 2, H - 4.7 * inch, "É essa a diferença que este curso está formando.")

c.setFillColor(LIGHT_TEXT)
c.setFont("Helvetica", 11)
tw = c.stringWidth("Método: Prof. Dr. José Bezerra · BSBr  |  Base: PMI Standard for AI in PPPM (2026)", "Helvetica", 11)
c.drawString((W - tw) / 2, 0.9 * inch, "Método: Prof. Dr. José Bezerra · BSBr  |  Base: PMI Standard for AI in PPPM (2026)")
tw = c.stringWidth("github.com/geovime1977/consultor-ia-pppm  ·  Geovane Virmecati · Eixo Estratégico", "Helvetica", 11)
c.drawString((W - tw) / 2, 0.6 * inch, "github.com/geovime1977/consultor-ia-pppm  ·  Geovane Virmecati · Eixo Estratégico")

c.showPage()

c.save()

import os
path = "/Users/virmecati/projetos/consultor-ia-pppm/docs/DECK-PALESTRA.pdf"
print(f"PDF gerado: {path} ({os.path.getsize(path)/1024:.1f} KB)")
