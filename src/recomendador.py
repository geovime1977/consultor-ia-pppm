import json
import unicodedata
from pathlib import Path

from src import niveis

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
_PILOTOS_PATH = _DATA_DIR / "pilotos.json"
_KEYWORDS_PATH = _DATA_DIR / "keywords_dor.json"

_GRAUS = ["baixo", "medio", "alto"]


def carregar_catalogo() -> list[dict]:
    with open(_PILOTOS_PATH, encoding="utf-8") as f:
        return json.load(f)


def carregar_keywords() -> dict:
    with open(_KEYWORDS_PATH, encoding="utf-8") as f:
        return json.load(f)


def _normalizar(texto: str) -> str:
    if not texto:
        return ""
    nfkd = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def extrair_categorias_dor(texto_dor: str) -> list[str]:
    keywords = carregar_keywords()
    alvo = _normalizar(texto_dor)
    encontradas = []
    for categoria, palavras in keywords.items():
        for palavra in palavras:
            if _normalizar(palavra) in alvo:
                encontradas.append(categoria)
                break
    return encontradas


def _subir_grau(grau: str) -> str:
    if grau not in _GRAUS:
        return grau
    idx = _GRAUS.index(grau)
    return _GRAUS[min(idx + 1, len(_GRAUS) - 1)]


def _descer_grau(grau: str) -> str:
    if grau not in _GRAUS:
        return grau
    idx = _GRAUS.index(grau)
    return _GRAUS[max(idx - 1, 0)]


def _identificar_gargalo_local(diagnostico: dict) -> str:
    ordem = ["governanca", "dados", "estrategia", "casos_uso", "beneficios"]
    valores = {k: int(diagnostico.get(k, 0) or 0) for k in ordem}
    minimo = min(valores.values())
    for dim in ordem:
        if valores[dim] == minimo:
            return dim
    return ordem[0]


def scoring_piloto(piloto: dict, nivel: int, categorias_dor: list[str]) -> dict:
    impacto = piloto["impacto_base"]
    viabilidade = piloto["viabilidade_base"]
    risco = piloto["risco_base"]

    if nivel <= 2 and viabilidade == "alto":
        viabilidade = "medio"

    intersecao = set(piloto["categorias_dor"]) & set(categorias_dor)
    if len(intersecao) >= 2 and impacto == "medio":
        impacto = "alto"

    pre_req_texto = " ".join(piloto.get("pre_requisitos", [])).lower()
    if nivel <= 2 and ("histórico" in pre_req_texto or "historico" in pre_req_texto):
        risco = _subir_grau(risco)

    if nivel >= 4 and risco == "medio":
        risco = _descer_grau(risco)

    return {"impacto": impacto, "viabilidade": viabilidade, "risco": risco}


def recomendar(diagnostico: dict, mapa: dict, top_n: int = 3) -> list[dict]:
    catalogo = carregar_catalogo()
    gargalo = _identificar_gargalo_local(diagnostico)
    total = sum(int(diagnostico.get(k, 0) or 0) for k in diagnostico)
    nivel_info = niveis.get_nivel(total)
    nivel = nivel_info["numero"]
    categorias_dor = extrair_categorias_dor(mapa.get("dor", ""))

    candidatos: list[tuple[dict, int]] = []
    for piloto in catalogo:
        score = 0

        if gargalo in piloto["dimensoes_alvo"]:
            score += 10

        for dim in piloto["dimensoes_alvo"]:
            if dim == gargalo:
                continue
            if int(diagnostico.get(dim, 0) or 0) <= 3:
                score += 3

        intersecao = set(piloto["categorias_dor"]) & set(categorias_dor)
        score += len(intersecao) * 5

        if nivel <= 2 and piloto["viabilidade_base"] == "alto":
            score += 4
        if nivel >= 4 and piloto["impacto_base"] == "alto":
            score += 4

        if nivel <= 2 and piloto["risco_base"] == "alto":
            score -= 5

        if score > 0:
            candidatos.append((piloto, score))

    if len(candidatos) < top_n:
        ja_incluidos = {p["id"] for p, _ in candidatos}
        fallback = [
            (p, 1)
            for p in catalogo
            if p["id"] not in ja_incluidos
            and p["viabilidade_base"] == "alto"
            and p["risco_base"] == "baixo"
        ]
        candidatos.extend(fallback)

    candidatos.sort(key=lambda x: x[1], reverse=True)

    resultado = []
    for piloto, score in candidatos[:top_n]:
        scoring = scoring_piloto(piloto, nivel, categorias_dor)
        entrada = dict(piloto)
        entrada["scoring"] = scoring
        entrada["score_bruto"] = score
        resultado.append(entrada)
    return resultado
