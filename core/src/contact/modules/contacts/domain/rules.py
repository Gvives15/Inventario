from typing import Any


def normalize_string(s: str) -> str:
    return s.strip()


def validate_fact_value(key: str, value_json: Any) -> None:
    required_string_keys = {"name", "zone", "business_type"}
    if key in required_string_keys:
        if not isinstance(value_json, str):
            raise ValueError("value must be string")
        vv = normalize_string(value_json)
        if len(vv) < 2:
            raise ValueError("value too short")
        if vv in {"-", ".", "m"}:
            raise ValueError("placeholder not allowed")


def is_valid_sku_for_stats(sku: str) -> bool:
    if sku.isdigit():
        return False
    if len(sku) < 3:
        return False
    return True
