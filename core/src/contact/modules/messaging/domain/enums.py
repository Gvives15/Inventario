from enum import Enum


class Provider(str, Enum):
    CHATWOOT = "chatwoot"


class Direction(str, Enum):
    IN = "IN"
    OUT = "OUT"


class DeliveryStatus(str, Enum):
    RECEIVED = "RECEIVED"
    PROCESSED = "PROCESSED"
    SENT = "SENT"
    FAILED = "FAILED"

