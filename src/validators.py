_PORTES_VALIDOS = {"PME", "Média", "Grande", "Governo"}
_MIN_CHARS_MAPA = 30
_BLOCOS_MAPA = ("contexto", "dor", "dados", "riscos", "valor")
_DIMENSOES_DIAG = ("estrategia", "dados", "casos_uso", "governanca", "beneficios")


def validar_contexto(ctx: dict) -> tuple[bool, list[str]]:
    erros = []
    if not ctx.get("nome", "").strip():
        erros.append("Informe o nome do participante.")
    if not ctx.get("empresa", "").strip():
        erros.append("Informe o nome da empresa.")
    if ctx.get("porte") not in _PORTES_VALIDOS:
        erros.append("Selecione o porte da empresa (PME, Média, Grande ou Governo).")
    if not isinstance(ctx.get("n_projetos"), int) or ctx.get("n_projetos", 0) < 0:
        erros.append("Informe um número de projetos ativos válido (inteiro >= 0).")
    if not ctx.get("cargo", "").strip():
        erros.append("Informe o cargo do participante.")
    return (len(erros) == 0, erros)


def validar_diagnostico(diag: dict) -> tuple[bool, list[str]]:
    erros = []
    for dim in _DIMENSOES_DIAG:
        valor = diag.get(dim)
        if not isinstance(valor, int) or valor < 0 or valor > 6:
            erros.append(f"A dimensão '{dim}' deve ter valor inteiro entre 0 e 6.")
    return (len(erros) == 0, erros)


def validar_mapa(mapa: dict) -> tuple[bool, list[str]]:
    erros = []
    for bloco in _BLOCOS_MAPA:
        texto = mapa.get(bloco, "") or ""
        if len(texto.strip()) < _MIN_CHARS_MAPA:
            erros.append(
                f"O bloco '{bloco}' precisa ter ao menos {_MIN_CHARS_MAPA} caracteres."
            )
    return (len(erros) == 0, erros)
