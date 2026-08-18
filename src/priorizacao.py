"""Priorização de Casos de Uso — Aula 2 IA-PPPM (Prof. Dr. José Bezerra, BSBr, 2026-08-17).

Score executivo ponderado em 5 critérios (Impacto 30% · Viabilidade 20% · Dados 20% ·
Risco 15% · Valor 15%) + ranking Fazer agora / Preparar / Não priorizar.

Corte obrigatório (slide 30): sem dono humano da decisão, o caso NÃO ESTÁ PRONTO —
ranking forçado para "Não priorizar" independente do score.

Matriz Impacto × Viabilidade (slide 29): quadrante visual antes de aplicar filtros de
risco, dados e governança.

100% determinístico, zero LLM.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CRITERIOS_PATH = DATA_DIR / "criterios_priorizacao.json"

CRITERIO_IDS = ("impacto", "viabilidade", "dados", "risco", "valor")


@dataclass
class CasoDeUso:
    id: str
    nome: str
    contexto: str = ""
    dor: str = ""
    dados: str = ""
    decisao: str = ""
    dono: str | None = None
    metrica_valor: str = ""
    notas: dict[str, int] = field(default_factory=dict)


def carregar_criterios() -> dict:
    return json.loads(CRITERIOS_PATH.read_text(encoding="utf-8"))


def _pesos_default() -> dict[str, float]:
    return {c["id"]: c["peso"] for c in carregar_criterios()["criterios"]}


def score_ponderado(notas: dict[str, int], pesos: dict[str, float] | None = None) -> float:
    """Score em escala 0-5 (nota 1-5 × peso somando 1.0). Notas ausentes contam zero."""
    if pesos is None:
        pesos = _pesos_default()
    total = sum(float(notas.get(cid, 0)) * float(pesos.get(cid, 0)) for cid in pesos)
    return round(total, 2)


def status_prontidao(caso: CasoDeUso) -> str:
    """Corte obrigatório do slide 30: sem dono humano, caso NÃO ESTÁ PRONTO."""
    if not caso.dono or not str(caso.dono).strip():
        return "Não pronto — sem dono humano"
    return "Pronto"


def ranking(caso: CasoDeUso, score: float, thresholds: dict | None = None) -> str:
    """Fazer agora / Preparar / Não priorizar. Corte obrigatório força 'Não priorizar'."""
    if status_prontidao(caso).startswith("Não pronto"):
        return "Não priorizar"
    if thresholds is None:
        thresholds = carregar_criterios()["thresholds"]
    if score >= thresholds["fazer_agora"]:
        return "Fazer agora"
    if score >= thresholds["preparar"]:
        return "Preparar"
    return "Não priorizar"


def quadrante(notas: dict[str, int]) -> str:
    """Matriz Impacto × Viabilidade do slide 29. Corte em 4 (alto ≥ 4)."""
    impacto = int(notas.get("impacto", 0) or 0)
    viab = int(notas.get("viabilidade", 0) or 0)
    if impacto >= 4 and viab >= 4:
        return "Comece aqui"
    if impacto >= 4 and viab < 4:
        return "Investigue"
    if impacto < 4 and viab >= 4:
        return "Baixa prioridade"
    return "Evite agora"


def priorizar_lote(casos: list[CasoDeUso]) -> list[dict]:
    """Aplica score + status + ranking + quadrante e ordena por score decrescente."""
    criterios = carregar_criterios()
    pesos = {c["id"]: c["peso"] for c in criterios["criterios"]}
    thresholds = criterios["thresholds"]
    resultado = []
    for caso in casos:
        score = score_ponderado(caso.notas, pesos)
        resultado.append(
            {
                "id": caso.id,
                "nome": caso.nome,
                "score": score,
                "status_prontidao": status_prontidao(caso),
                "ranking": ranking(caso, score, thresholds),
                "quadrante": quadrante(caso.notas),
                "notas": dict(caso.notas),
                "dono": caso.dono,
            }
        )
    resultado.sort(key=lambda r: r["score"], reverse=True)
    return resultado


def top_n(resultado: list[dict], n: int = 3) -> list[dict]:
    """Retorna os N casos com ranking 'Fazer agora' de maior score.

    Se não houver N com 'Fazer agora', completa com 'Preparar'. Nunca inclui
    'Não priorizar' (respeita o corte obrigatório).
    """
    aceitos = [r for r in resultado if r["ranking"] != "Não priorizar"]
    fazer = [r for r in aceitos if r["ranking"] == "Fazer agora"]
    preparar = [r for r in aceitos if r["ranking"] == "Preparar"]
    return (fazer + preparar)[:n]


def carregar_empresa_alfa() -> list[CasoDeUso]:
    """Exemplo Empresa Alfa do slide 37 do deck oficial."""
    seed = carregar_criterios()["empresa_alfa"]["casos"]
    casos = []
    for c in seed:
        casos.append(
            CasoDeUso(
                id=c["id"],
                nome=c["nome"],
                contexto=c.get("contexto", ""),
                dor=c.get("dor", ""),
                dados=c.get("dados", ""),
                decisao=c.get("decisao", ""),
                dono=c.get("dono"),
                metrica_valor=c.get("metrica_valor", ""),
                notas={cid: 0 for cid in CRITERIO_IDS},
            )
        )
    return casos
