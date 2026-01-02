from ninja import Schema
from typing import Any, Optional


class WhatsAppInboundIn(Schema):
    provider: str
    provider_message_id: str
    whatsapp_id: str
    text: str
    raw_payload: Optional[Any] = None


class WhatsAppInboundOut(Schema):
    reply: str
