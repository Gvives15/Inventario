import re


_PATTERNS = {
    "name": re.compile(r"^\s*Nombre\s*:\s*(.+)$", re.IGNORECASE),
    "zone": re.compile(r"^\s*Zona\s*:\s*(.+)$", re.IGNORECASE),
    "business_type": re.compile(r"^\s*Tipo\s*:\s*(.+)$", re.IGNORECASE),
}


def parse(text: str) -> dict:
    result: dict = {}
    for line in text.splitlines():
        for key, pat in _PATTERNS.items():
            m = pat.match(line)
            if m:
                result[key] = m.group(1).strip()
    return result
