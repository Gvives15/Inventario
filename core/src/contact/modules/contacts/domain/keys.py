FACT_KEYS_REQUIRED = {"name", "zone", "business_type"}
FACT_KEYS_OPTIONAL = {
    "address_text",
    "delivery_notes",
    "payment_method_default",
    "invoice_type",
    "preferred_list_code",
    "delivery_window",
}
ALL_FACT_KEYS = FACT_KEYS_REQUIRED | FACT_KEYS_OPTIONAL


def is_allowed_fact_key(key: str) -> bool:
    return key in ALL_FACT_KEYS
