def parse(text: str) -> dict:
    t = (text or "").strip()
    if not t:
        return {"action": "UNKNOWN"}
    u = t.upper()
    if u in ("OK", "CONFIRMAR", "LISTO"):
        return {"action": "CONFIRM"}
    if u in ("VER", "MOSTRAR"):
        return {"action": "SHOW"}
    if t.startswith("+"):
        parts = t[1:].strip().split()
        if len(parts) == 2:
            sku, qty_s = parts
            try:
                qty = int(qty_s)
                if qty > 0:
                    return {"action": "ADD", "sku": sku.strip(), "qty": qty}
            except ValueError:
                pass
        return {"action": "UNKNOWN"}
    if t.startswith("-"):
        parts = t[1:].strip().split()
        if len(parts) == 1:
            sku = parts[0]
            return {"action": "REMOVE", "sku": sku.strip()}
        return {"action": "UNKNOWN"}
    if t.startswith("="):
        parts = t[1:].strip().split()
        if len(parts) == 2:
            sku, qty_s = parts
            try:
                qty = int(qty_s)
                if qty > 0:
                    return {"action": "SET_QTY", "sku": sku.strip(), "qty": qty}
            except ValueError:
                pass
        return {"action": "UNKNOWN"}
    return {"action": "UNKNOWN"}
