"""Import/Export de projeto em JSON — portabilidade entre sessões e alunos.

Serializa o estado completo (Aula 1 + Aula 2) em JSON versionado. Permite ao
aluno salvar o próprio projeto localmente e reimportar em nova sessão sem
depender de persistência no servidor Streamlit Cloud.

100% determinístico, zero LLM.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from typing import Any

from src.governanca import Rastro
from src.priorizacao import CasoDeUso

SCHEMA = "consultor-ia-pppm/projeto"
VERSAO_SCHEMA = "1.0"


def exportar(estado: dict) -> dict:
    """Serializa o estado completo em dict pronto para virar JSON.

    `estado` é um dicionário com chaves opcionais:
      - contexto, diagnostico, mapa, pilotos_selecionados (Aula 1)
      - aula2_casos: list[CasoDeUso]
      - aula2_gov_respostas: dict[caso_id, dict[bloco_id, bool]]
      - aula2_gov_rastro: dict[caso_id, Rastro]
    """
    casos_serializados = []
    for c in estado.get("aula2_casos", []) or []:
        casos_serializados.append(
            asdict(c) if isinstance(c, CasoDeUso) else dict(c)
        )
    rastro_serializado: dict[str, dict] = {}
    for cid, r in (estado.get("aula2_gov_rastro", {}) or {}).items():
        rastro_serializado[cid] = asdict(r) if isinstance(r, Rastro) else dict(r)
    return {
        "schema": SCHEMA,
        "versao": VERSAO_SCHEMA,
        "exportado_em": datetime.now().isoformat(timespec="seconds"),
        "aula1": {
            "contexto": dict(estado.get("contexto") or {}),
            "diagnostico": dict(estado.get("diagnostico") or {}),
            "mapa": dict(estado.get("mapa") or {}),
            "pilotos_selecionados": list(estado.get("pilotos_selecionados") or []),
        },
        "aula2": {
            "casos": casos_serializados,
            "governanca": {
                "respostas": dict(estado.get("aula2_gov_respostas") or {}),
                "rastro": rastro_serializado,
            },
        },
    }


def exportar_json(estado: dict, indent: int = 2) -> str:
    return json.dumps(exportar(estado), indent=indent, ensure_ascii=False, default=str)


class ErroImportacao(ValueError):
    pass


def _validar_schema(dados: Any) -> None:
    if not isinstance(dados, dict):
        raise ErroImportacao("JSON precisa ser um objeto no topo.")
    if dados.get("schema") != SCHEMA:
        raise ErroImportacao(
            f"Schema desconhecido: {dados.get('schema')!r}. Esperado {SCHEMA!r}."
        )
    versao = str(dados.get("versao") or "")
    if not versao.startswith("1."):
        raise ErroImportacao(
            f"Versão de schema incompatível: {versao!r}. Este app lê versão 1.x."
        )
    if "aula1" not in dados and "aula2" not in dados:
        raise ErroImportacao("Arquivo não contém dados de Aula 1 nem Aula 2.")


def importar(dados: dict) -> dict:
    """Converte JSON de volta em dicionário pronto para injetar no session_state.

    Retorna um dict com as MESMAS chaves que `exportar` espera receber. O caller
    (UI) faz `st.session_state[k] = v` para cada par.
    """
    _validar_schema(dados)
    aula1 = dados.get("aula1") or {}
    aula2 = dados.get("aula2") or {}

    casos = []
    for c in aula2.get("casos") or []:
        casos.append(
            CasoDeUso(
                id=c.get("id", ""),
                nome=c.get("nome", ""),
                contexto=c.get("contexto", ""),
                dor=c.get("dor", ""),
                dados=c.get("dados", ""),
                decisao=c.get("decisao", ""),
                dono=c.get("dono"),
                metrica_valor=c.get("metrica_valor", ""),
                notas=dict(c.get("notas") or {}),
            )
        )

    gov = aula2.get("governanca") or {}
    rastros: dict[str, Rastro] = {}
    for cid, r in (gov.get("rastro") or {}).items():
        rastros[cid] = Rastro(
            caso_id=r.get("caso_id", cid),
            entrada=r.get("entrada", ""),
            processamento=r.get("processamento", ""),
            saida=r.get("saida", ""),
            validacao=r.get("validacao", ""),
            registro=r.get("registro", ""),
        )

    return {
        "contexto": dict(aula1.get("contexto") or {}),
        "diagnostico": dict(aula1.get("diagnostico") or {}),
        "mapa": dict(aula1.get("mapa") or {}),
        "pilotos_selecionados": list(aula1.get("pilotos_selecionados") or []),
        "aula2_casos": casos,
        "aula2_gov_respostas": dict(gov.get("respostas") or {}),
        "aula2_gov_rastro": rastros,
    }


def importar_json(texto: str) -> dict:
    try:
        dados = json.loads(texto)
    except json.JSONDecodeError as e:
        raise ErroImportacao(f"JSON inválido: {e}") from e
    return importar(dados)


def resumo_importacao(estado: dict) -> str:
    """Retorna resumo humano do que foi importado (usado na UI)."""
    ctx = estado.get("contexto") or {}
    linhas = [
        f"Projeto: {ctx.get('empresa') or '(sem empresa)'} — {ctx.get('nome') or 'sem responsável'}",
        f"Aula 1 · diagnóstico preenchido: "
        + ("sim" if any((estado.get("diagnostico") or {}).values()) else "não"),
        f"Aula 1 · pilotos: {len(estado.get('pilotos_selecionados') or [])}",
        f"Aula 2 · casos: {len(estado.get('aula2_casos') or [])}",
        f"Aula 2 · governança de {len(estado.get('aula2_gov_rastro') or {})} caso(s)",
    ]
    return "\n".join(linhas)
