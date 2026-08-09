import json
import sqlite3
from datetime import datetime
from pathlib import Path

_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "diag.db"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS projetos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    empresa TEXT,
    porte TEXT,
    cargo_gp TEXT,
    n_projetos INTEGER DEFAULT 0,
    pmo_ativo INTEGER DEFAULT 0,
    estrategia INTEGER DEFAULT 0,
    dados INTEGER DEFAULT 0,
    casos_uso INTEGER DEFAULT 0,
    governanca INTEGER DEFAULT 0,
    beneficios INTEGER DEFAULT 0,
    mapa_contexto TEXT DEFAULT '',
    mapa_dor TEXT DEFAULT '',
    mapa_dados TEXT DEFAULT '',
    mapa_riscos TEXT DEFAULT '',
    mapa_valor TEXT DEFAULT '',
    pilotos_json TEXT DEFAULT '[]',
    criado_em TEXT NOT NULL,
    atualizado_em TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS projeto_pmbok (
    projeto_id INTEGER NOT NULL,
    processo_id TEXT NOT NULL,
    tratamento TEXT NOT NULL DEFAULT 'nenhum',
    criticidade TEXT NOT NULL DEFAULT 'media',
    observacao TEXT DEFAULT '',
    PRIMARY KEY (projeto_id, processo_id),
    FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_pmbok_projeto ON projeto_pmbok(projeto_id);
"""

TRATAMENTOS = ["nenhum", "ia", "ia_po", "gap"]
CRITICIDADES = ["baixa", "media", "alta"]


def _conn() -> sqlite3.Connection:
    _DB_PATH.parent.mkdir(exist_ok=True)
    c = sqlite3.connect(_DB_PATH)
    c.execute("PRAGMA foreign_keys = ON")
    c.row_factory = sqlite3.Row
    return c


def init_db() -> None:
    with _conn() as c:
        c.executescript(_SCHEMA)


def listar_projetos() -> list[dict]:
    init_db()
    with _conn() as c:
        rows = c.execute(
            "SELECT * FROM projetos ORDER BY atualizado_em DESC"
        ).fetchall()
    return [_row_to_projeto(r) for r in rows]


def obter_projeto(projeto_id: int) -> dict | None:
    init_db()
    with _conn() as c:
        row = c.execute("SELECT * FROM projetos WHERE id = ?", (projeto_id,)).fetchone()
    return _row_to_projeto(row) if row else None


def obter_projeto_por_nome(nome: str) -> dict | None:
    init_db()
    with _conn() as c:
        row = c.execute("SELECT * FROM projetos WHERE nome = ?", (nome,)).fetchone()
    return _row_to_projeto(row) if row else None


def salvar_projeto(dados: dict, projeto_id: int | None = None) -> int:
    init_db()
    agora = datetime.now().isoformat(timespec="seconds")
    pilotos_json = json.dumps(dados.get("pilotos", []), ensure_ascii=False)
    campos = {
        "nome": dados["nome"],
        "empresa": dados.get("empresa", ""),
        "porte": dados.get("porte", ""),
        "cargo_gp": dados.get("cargo_gp", ""),
        "n_projetos": int(dados.get("n_projetos", 0) or 0),
        "pmo_ativo": int(bool(dados.get("pmo_ativo", False))),
        "estrategia": int(dados.get("estrategia", 0) or 0),
        "dados": int(dados.get("dados", 0) or 0),
        "casos_uso": int(dados.get("casos_uso", 0) or 0),
        "governanca": int(dados.get("governanca", 0) or 0),
        "beneficios": int(dados.get("beneficios", 0) or 0),
        "mapa_contexto": dados.get("mapa_contexto", ""),
        "mapa_dor": dados.get("mapa_dor", ""),
        "mapa_dados": dados.get("mapa_dados", ""),
        "mapa_riscos": dados.get("mapa_riscos", ""),
        "mapa_valor": dados.get("mapa_valor", ""),
        "pilotos_json": pilotos_json,
        "atualizado_em": agora,
    }
    with _conn() as c:
        if projeto_id is None:
            campos["criado_em"] = agora
            cols = ", ".join(campos.keys())
            marks = ", ".join(["?"] * len(campos))
            cur = c.execute(
                f"INSERT INTO projetos ({cols}) VALUES ({marks})",
                list(campos.values()),
            )
            return cur.lastrowid
        else:
            sets = ", ".join([f"{k} = ?" for k in campos.keys()])
            c.execute(
                f"UPDATE projetos SET {sets} WHERE id = ?",
                list(campos.values()) + [projeto_id],
            )
            return projeto_id


def excluir_projeto(projeto_id: int) -> None:
    init_db()
    with _conn() as c:
        c.execute("DELETE FROM projetos WHERE id = ?", (projeto_id,))


def listar_tratamentos_pmbok(projeto_id: int) -> dict[str, dict]:
    """Retorna dict {processo_id: {tratamento, criticidade, observacao}}"""
    init_db()
    with _conn() as c:
        rows = c.execute(
            "SELECT processo_id, tratamento, criticidade, observacao "
            "FROM projeto_pmbok WHERE projeto_id = ?",
            (projeto_id,),
        ).fetchall()
    return {
        r["processo_id"]: {
            "tratamento": r["tratamento"],
            "criticidade": r["criticidade"],
            "observacao": r["observacao"],
        }
        for r in rows
    }


def salvar_tratamento_pmbok(
    projeto_id: int,
    processo_id: str,
    tratamento: str,
    criticidade: str,
    observacao: str = "",
) -> None:
    init_db()
    with _conn() as c:
        c.execute(
            """
            INSERT INTO projeto_pmbok (projeto_id, processo_id, tratamento, criticidade, observacao)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(projeto_id, processo_id) DO UPDATE SET
                tratamento = excluded.tratamento,
                criticidade = excluded.criticidade,
                observacao = excluded.observacao
            """,
            (projeto_id, processo_id, tratamento, criticidade, observacao),
        )


def excluir_tratamento_pmbok(projeto_id: int, processo_id: str) -> None:
    init_db()
    with _conn() as c:
        c.execute(
            "DELETE FROM projeto_pmbok WHERE projeto_id = ? AND processo_id = ?",
            (projeto_id, processo_id),
        )


def _row_to_projeto(row: sqlite3.Row) -> dict:
    d = dict(row)
    try:
        d["pilotos"] = json.loads(d.pop("pilotos_json") or "[]")
    except json.JSONDecodeError:
        d["pilotos"] = []
    d["pmo_ativo"] = bool(d["pmo_ativo"])
    return d


def contar_projetos() -> int:
    init_db()
    with _conn() as c:
        row = c.execute("SELECT COUNT(*) AS n FROM projetos").fetchone()
    return row["n"] if row else 0
