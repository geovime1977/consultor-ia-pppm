"""Auto-diagnóstico PMBOK — classifica cada um dos 40 processos de um projeto
por eficiência esperada e criticidade, e identifica gargalos.

Heurística determinística (sem LLM) baseada em:
1. As 5 dimensões de maturidade IA-PPPM (0-6) do projeto (aba 2).
2. O texto do Mapa 5 Blocos (dor / dados / valor) para detectar keywords.
3. O grupo de processo PMBOK (Início/Planejamento/Execução/M&C/Encerramento).

Não substitui a marcação manual — sugere pontos de partida.
"""
from __future__ import annotations

from typing import Iterable

# Mapeamento área PMBOK → dimensões de maturidade que mais afetam sua eficiência.
# Cada área usa média ponderada de 2 dimensões relevantes.
_AREA_DIMENSOES = {
    "Governança":          [("governanca", 0.6), ("estrategia", 0.4)],
    "Escopo":              [("casos_uso", 0.6), ("dados", 0.4)],
    "Cronograma":          [("governanca", 0.5), ("dados", 0.5)],
    "Finanças":            [("beneficios", 0.6), ("estrategia", 0.4)],
    "Partes Interessadas": [("governanca", 0.5), ("beneficios", 0.5)],
    "Recursos":            [("dados", 0.5), ("casos_uso", 0.5)],
    "Riscos":              [("governanca", 0.5), ("estrategia", 0.5)],
}

# Keywords no Mapa 5 Blocos que indicam relevância adicional de uma área.
_AREA_KEYWORDS = {
    "Governança":          ["governanca", "governança", "compliance", "regulator", "auditor", "hitl", "político"],
    "Escopo":              ["escopo", "requisito", "mvp", "backlog", "produto", "feature"],
    "Cronograma":          ["prazo", "cronograma", "atraso", "sprint", "marco", "deadline"],
    "Finanças":            ["custo", "orçamento", "financeiro", "receita", "roi", "payback", "capex", "opex"],
    "Partes Interessadas": ["stakeholder", "sponsor", "cliente", "comitê", "usuário", "engajamento"],
    "Recursos":            ["equipe", "alocação", "recurso", "headcount", "contratação", "squad", "consultor"],
    "Riscos":              ["risco", "incerteza", "lgpd", "regulatório", "compliance", "adversarial"],
}

# Boost por grupo de processo — alguns projetos naturalmente estão em fases diferentes.
_GRUPO_BOOST = {
    "Início": 0.9,
    "Planejamento": 1.0,
    "Execução": 1.05,
    "Monitoramento e Controle": 1.05,
    "Encerramento": 0.85,
}


def _texto_mapa(projeto: dict) -> str:
    partes = [
        projeto.get("mapa_contexto", ""),
        projeto.get("mapa_dor", ""),
        projeto.get("mapa_dados", ""),
        projeto.get("mapa_riscos", ""),
        projeto.get("mapa_valor", ""),
    ]
    return " ".join(partes).lower()


def _score_area(projeto: dict, area: str, texto: str) -> float:
    """Score 0-6 de maturidade projetada para uma área PMBOK."""
    if area not in _AREA_DIMENSOES:
        return 0.0
    base = sum(
        float(projeto.get(dim, 0) or 0) * peso
        for dim, peso in _AREA_DIMENSOES[area]
    )
    boost_keyword = 0.0
    for kw in _AREA_KEYWORDS.get(area, []):
        if kw in texto:
            boost_keyword += 0.3
    boost_keyword = min(boost_keyword, 1.2)
    return min(6.0, base + boost_keyword)


def sugerir_tratamento(score_area: float, grupo: str) -> tuple[str, str]:
    """Retorna (tratamento, criticidade) sugeridos.

    tratamento: nenhum | ia | ia_po | gap
    criticidade: baixa | media | alta
    """
    score_ajustado = score_area * _GRUPO_BOOST.get(grupo, 1.0)

    if score_ajustado < 2.0:
        return "gap", "alta"
    if score_ajustado < 3.5:
        return "ia", "media"
    if score_ajustado < 5.0:
        return "ia", "alta"
    return "ia_po", "alta"


def _eficiencia(score_area: float, tratamento: str, criticidade: str) -> float:
    """Score 0-100 de eficiência esperada do processo naquele projeto."""
    base = (score_area / 6.0) * 100.0
    mult_tratamento = {"ia_po": 1.15, "ia": 1.0, "gap": 0.4, "nenhum": 0.7}
    mult_crit = {"alta": 1.0, "media": 0.9, "baixa": 0.75}
    ef = base * mult_tratamento.get(tratamento, 1.0) * mult_crit.get(criticidade, 0.9)
    return round(min(100.0, ef), 1)


def analisar_projeto(projeto: dict, processos: list[dict]) -> list[dict]:
    """Para cada processo PMBOK, calcula score, tratamento sugerido, eficiência.

    Retorna lista de dicts com:
      processo_id, nome, area, grupo, score_area, tratamento_sugerido,
      criticidade_sugerida, eficiencia_pct, is_gargalo
    """
    texto = _texto_mapa(projeto)
    resultados = []

    for p in processos:
        score = _score_area(projeto, p["area"], texto)
        trat, crit = sugerir_tratamento(score, p["grupo"])
        ef = _eficiencia(score, trat, crit)
        resultados.append({
            "processo_id": p["id"],
            "nome": p["nome"],
            "area": p["area"],
            "grupo": p["grupo"],
            "score_area": round(score, 2),
            "tratamento_sugerido": trat,
            "criticidade_sugerida": crit,
            "eficiencia_pct": ef,
            "is_gargalo": trat == "gap" or (crit == "alta" and ef < 55),
        })
    return resultados


def top_gargalos(analise: list[dict], n: int = 5) -> list[dict]:
    """Top N gargalos: menor eficiência entre os críticos + todos os gaps."""
    gaps = [a for a in analise if a["tratamento_sugerido"] == "gap"]
    criticos = sorted(
        [a for a in analise if a["criticidade_sugerida"] == "alta"],
        key=lambda a: a["eficiencia_pct"],
    )
    combinado = gaps + [a for a in criticos if a not in gaps]
    return combinado[:n]


def resumo_projeto(analise: list[dict]) -> dict:
    """Métricas agregadas do projeto para dashboard."""
    if not analise:
        return {
            "n_processos": 0,
            "eficiencia_media": 0.0,
            "n_gargalos": 0,
            "n_gaps": 0,
            "n_ia_po_sugeridos": 0,
            "areas_criticas": [],
        }

    n = len(analise)
    ef_media = sum(a["eficiencia_pct"] for a in analise) / n
    n_gargalos = sum(1 for a in analise if a["is_gargalo"])
    n_gaps = sum(1 for a in analise if a["tratamento_sugerido"] == "gap")
    n_iapo = sum(1 for a in analise if a["tratamento_sugerido"] == "ia_po")

    # Áreas com maior densidade de gargalos
    por_area: dict[str, list[dict]] = {}
    for a in analise:
        por_area.setdefault(a["area"], []).append(a)
    areas_criticas = sorted(
        [
            (area, sum(1 for x in itens if x["is_gargalo"]) / len(itens))
            for area, itens in por_area.items()
        ],
        key=lambda t: -t[1],
    )
    areas_criticas = [a for a, pct in areas_criticas if pct > 0][:3]

    return {
        "n_processos": n,
        "eficiencia_media": round(ef_media, 1),
        "n_gargalos": n_gargalos,
        "n_gaps": n_gaps,
        "n_ia_po_sugeridos": n_iapo,
        "areas_criticas": areas_criticas,
    }


def aplicar_sugestoes(
    analise: list[dict],
    salvar_fn,
    projeto_id: int,
    apenas_gargalos: bool = False,
) -> int:
    """Persiste as sugestões usando salvar_fn(projeto_id, processo_id, trat, crit, obs).

    Se apenas_gargalos=True, só salva gargalos. Retorna quantas foram aplicadas.
    """
    aplicadas = 0
    for a in analise:
        if apenas_gargalos and not a["is_gargalo"]:
            continue
        obs = (
            f"Auto-sugerido: score área {a['score_area']:.1f}/6, "
            f"eficiência prevista {a['eficiencia_pct']}%"
        )
        salvar_fn(
            projeto_id,
            a["processo_id"],
            a["tratamento_sugerido"],
            a["criticidade_sugerida"],
            obs,
        )
        aplicadas += 1
    return aplicadas
