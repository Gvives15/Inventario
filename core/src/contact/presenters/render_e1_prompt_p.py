def render_missing_fields(missing: list[str]) -> str:
    if missing:
        return "Faltan: " + ", ".join(missing) + ". Formato: Nombre:/Zona:/Tipo:"
    return render_e1_prompt()


def render_e1_prompt() -> str:
    return (
        "Por favor completá tus datos en este formato:\n Nombre: <tu nombre>\nZona: <tu zona>\nTipo: <tu negocio>"
    )