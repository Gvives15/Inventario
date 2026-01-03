def render(summary: dict) -> str:
    lines = [f"Pedido confirmado (#{summary.get('order_id')})."]
    lines.append("Resumen:")
    for item in summary.get("items", []):
        ref = item.get("product_ref", "")
        name = item.get("product_name", "")
        qty = item.get("qty", 0)
        if name:
            lines.append(f"- {qty}x {name} ({ref})")
        else:
            lines.append(f"- {ref} x{qty}")
    lines.append("Próximo paso: te contactamos para coordinar entrega.")
    return "\n".join(lines)
