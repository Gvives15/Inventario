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


class ChatwootMessageSchema(Schema):
    id: int
    content: Optional[str] = None
    message_type: Optional[str] = None


class ChatwootContactRefSchema(Schema):
    id: int


class ChatwootConversationSchema(Schema):
    id: int
    contact: Optional[ChatwootContactRefSchema] = None


class ChatwootWebhookIn(Schema):
    event: str
    id: Optional[str] = None
    content: Optional[str] = None
    message_type: Optional[str] = None
    conversation: Optional[ChatwootConversationSchema] = None
    message: Optional[ChatwootMessageSchema] = None
