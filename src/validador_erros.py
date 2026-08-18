"""Validador dos 5 Erros de IA em Projetos — Aula 2 IA-PPPM (Prof. Dr. José Bezerra, BSBr).

Roda cada caso de uso contra 5 regras determinísticas derivadas dos slides 7-12
do deck oficial. Retorna lista de alertas por caso. 100% determinístico, zero LLM.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from src.priorizacao import CasoDeUso

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
REGRAS_PATH = DATA_DIR / "regras_5_erros.json"


@dataclass
class Alerta:
    erro_id: str
    nome: str
    severidade: str
    motivo: str
    correcao: str


def carregar_regras() -> dict:
    return json.loads(REGRAS_PATH.read_text(encoding="utf-8"))


def _tem_keyword(texto: str, keywords: list[str]) -> list[str]:
    if not texto:
        return []
    t = texto.lower()
    achadas = []
    for k in keywords:
        pattern = r"(?<![a-z0-9])" + re.escape(k.lower()) + r"(?![a-z0-9])"
        if re.search(pattern, t):
            achadas.append(k)
    return achadas


def _len_texto(texto: str | None) -> int:
    return len((texto or "").strip())


def _verifica_e1(caso: CasoDeUso, regra: dict) -> Alerta | None:
    campo_composto = f"{caso.nome} {caso.dor}"
    achadas = _tem_keyword(campo_composto, regra["keywords_ferramenta"])
    if achadas and _len_texto(caso.dor) < regra["tamanho_minimo_dor"]:
        return Alerta(
            erro_id="E1",
            nome=regra["nome"],
            severidade="alta",
            motivo=(
                f"Caso menciona ferramenta ({', '.join(achadas)}) mas descreve a dor "
                f"com menos de {regra['tamanho_minimo_dor']} caracteres."
            ),
            correcao=regra["correcao_de_rota"],
        )
    return None


def _verifica_e2(caso: CasoDeUso, regra: dict) -> Alerta | None:
    campo = f"{caso.nome} {caso.decisao}"
    achadas = _tem_keyword(campo, regra["keywords_fascinio"])
    if achadas and _len_texto(caso.metrica_valor) == 0:
        return Alerta(
            erro_id="E2",
            nome=regra["nome"],
            severidade="media",
            motivo=f"Termos técnicos ({', '.join(achadas)}) sem métrica de valor associada.",
            correcao=regra["correcao_de_rota"],
        )
    return None


def _verifica_e3(caso: CasoDeUso, regra: dict) -> Alerta | None:
    if _len_texto(caso.dados) < regra["tamanho_minimo_dados"]:
        return Alerta(
            erro_id="E3",
            nome=regra["nome"],
            severidade="alta",
            motivo=(
                f"Descrição de dados com menos de {regra['tamanho_minimo_dados']} "
                f"caracteres ({_len_texto(caso.dados)} atual)."
            ),
            correcao=regra["correcao_de_rota"],
        )
    return None


def _verifica_e4(caso: CasoDeUso, regra: dict) -> Alerta | None:
    if not caso.dono or not str(caso.dono).strip():
        return Alerta(
            erro_id="E4",
            nome=regra["nome"],
            severidade="alta",
            motivo="Nenhum humano identificado como dono da decisão.",
            correcao=regra["correcao_de_rota"],
        )
    return None


def _verifica_e5(caso: CasoDeUso, regra: dict) -> Alerta | None:
    if _len_texto(caso.metrica_valor) < regra["tamanho_minimo_metrica"]:
        return Alerta(
            erro_id="E5",
            nome=regra["nome"],
            severidade="media",
            motivo=f"Métrica de valor com menos de {regra['tamanho_minimo_metrica']} caracteres.",
            correcao=regra["correcao_de_rota"],
        )
    return None


VERIFICADORES = {
    "E1": _verifica_e1,
    "E2": _verifica_e2,
    "E3": _verifica_e3,
    "E4": _verifica_e4,
    "E5": _verifica_e5,
}


def validar(caso: CasoDeUso) -> list[Alerta]:
    regras = {r["id"]: r for r in carregar_regras()["erros"]}
    alertas = []
    for eid, verif in VERIFICADORES.items():
        r = regras.get(eid)
        if not r:
            continue
        alerta = verif(caso, r)
        if alerta:
            alertas.append(alerta)
    return alertas


def validar_lote(casos: list[CasoDeUso]) -> dict[str, list[Alerta]]:
    return {c.id: validar(c) for c in casos}


def resumo_lote(casos: list[CasoDeUso]) -> dict[str, int]:
    contagem = {eid: 0 for eid in VERIFICADORES}
    for c in casos:
        for a in validar(c):
            contagem[a.erro_id] += 1
    return contagem
