import json
from pathlib import Path

_NIVEIS_PATH = Path(__file__).resolve().parent.parent / "data" / "niveis.json"

with open(_NIVEIS_PATH, encoding="utf-8") as f:
    _NIVEIS = json.load(f)


def get_nivel(total: int) -> dict:
    for nivel in _NIVEIS:
        low, high = nivel["faixa"]
        if low <= total <= high:
            return nivel
    if total < _NIVEIS[0]["faixa"][0]:
        return _NIVEIS[0]
    return _NIVEIS[-1]


def listar_niveis() -> list[dict]:
    return list(_NIVEIS)
