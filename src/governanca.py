"""Governança + HITL — Aula 2 IA-PPPM (Prof. Dr. José Bezerra, BSBr, 2026-08-17).

Modelos determinísticos derivados dos slides 31-36 do deck oficial:
- Segurança (4 blocos): dados sensíveis, acessos, ambiente seguro, controle de uso.
- Ética (4 riscos): recomendações enviesadas, ausência de explicação, dados sem
  autorização, dependência cega da IA.
- Rastreabilidade (fluxo 5 passos): entrada → processamento → saída → validação → registro.
- HITL (3 papéis + workflow 4 passos): IA recomenda, humano valida, gestor decide.
- Princípio de ouro: quanto maior o impacto, maior a validação humana.

100% determinístico, zero LLM.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
POLITICA_PATH = DATA_DIR / "politica_governanca.json"


@dataclass
class Rastro:
    caso_id: str
    entrada: str = ""
    processamento: str = ""
    saida: str = ""
    validacao: str = ""
    registro: str = ""

    def completo(self) -> bool:
        campos = (self.entrada, self.processamento, self.saida, self.validacao, self.registro)
        return all(bool((c or "").strip()) for c in campos)

    def campos_faltantes(self) -> list[str]:
        pares = {
            "entrada": self.entrada,
            "processamento": self.processamento,
            "saida": self.saida,
            "validacao": self.validacao,
            "registro": self.registro,
        }
        return [k for k, v in pares.items() if not (v or "").strip()]


def carregar_politica() -> dict:
    return json.loads(POLITICA_PATH.read_text(encoding="utf-8"))


def nivel_hitl(score_impacto: float) -> dict:
    """Retorna o nível de validação humana exigido pelo princípio de ouro.

    Parâmetro esperado: score em escala 0-5 (o mesmo do módulo priorizacao).
    Retorna o dicionário do nível encontrado (id, descrição, aprovador...).
    """
    niveis = carregar_politica()["hitl"]["niveis"]
    for n in niveis:
        if n["impacto_min"] <= score_impacto <= n["impacto_max"]:
            return n
    return niveis[-1]


def checklist_seguranca(respostas: dict[str, bool]) -> list[dict]:
    """Retorna a lista de blocos de segurança com status marcado/não marcado.

    respostas: dict com chave = bloco.id, valor = True/False (o gestor confirmou o item).
    """
    blocos = carregar_politica()["seguranca"]["blocos"]
    resultado = []
    for b in blocos:
        resultado.append(
            {
                "id": b["id"],
                "titulo": b["titulo"],
                "regra": b["regra"],
                "atendido": bool(respostas.get(b["id"], False)),
            }
        )
    return resultado


def prontidao_governanca(respostas: dict[str, bool], rastro: Rastro) -> dict:
    """Diagnóstico determinístico de prontidão de governança de um caso.

    Regras (todas devem estar True para 'pronto'):
    - Todos os 4 blocos de segurança confirmados.
    - Rastro completo (5 passos preenchidos).
    """
    checklist = checklist_seguranca(respostas)
    seg_ok = all(item["atendido"] for item in checklist)
    rastro_ok = rastro.completo()
    itens_faltantes = [item["titulo"] for item in checklist if not item["atendido"]]
    passos_faltantes = rastro.campos_faltantes()
    return {
        "pronto": seg_ok and rastro_ok,
        "seguranca_ok": seg_ok,
        "rastro_ok": rastro_ok,
        "seguranca_faltando": itens_faltantes,
        "rastro_faltando": passos_faltantes,
    }
