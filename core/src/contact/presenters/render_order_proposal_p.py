def render(summary: dict) -> str:
    lines = [f"Propuesta #{summary.get('order_id')}"]
    for item in summary.get("items", []):
        lines.append(f"- {item['product_ref']} x{item['qty']}")
    return "\n".join(lines)
