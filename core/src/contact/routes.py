from ninja import Router
from contact.schemas.webhook_schemas import WhatsAppInboundIn, WhatsAppInboundOut, ChatwootWebhookIn
from contact.modules.conversations.application.handlers.handle_whatsapp_inbound_h import execute as handle_whatsapp_inbound
from contact.modules.gateways.chatwoot.application.handlers.handle_chatwoot_webhook_h import execute as handle_chatwoot_webhook
from typing import Any, Dict
import json
from contact.modules.gateways.whatsapp_cloud.application.handlers.whatsapp_webhook_h import execute_verify as wa_verify, execute_inbound as wa_inbound

router = Router()

@router.get("/")
def list_contacts(request):
    return {"message": "Hello from contacts"}


@router.post("/webhooks/whatsapp/inbound", response=WhatsAppInboundOut, auth=None)
def whatsapp_inbound_ep(request, payload: WhatsAppInboundIn):
    reply = handle_whatsapp_inbound(payload.dict())
    return {"reply": reply}


@router.post("/webhooks/chatwoot/", auth=None, response={200: Dict[str, Any], 401: Dict[str, Any]})
def chatwoot_webhook_ep(request, payload: ChatwootWebhookIn):
    data, status = handle_chatwoot_webhook(request.headers, payload.dict())
    return status, data

@router.get("/webhooks/whatsapp_cloud/", auth=None, response={200: Dict[str, Any], 401: Dict[str, Any]})
def whatsapp_cloud_verify_ep(request):
    data, status = wa_verify(request.GET)
    return status, data

@router.post("/webhooks/whatsapp_cloud/", auth=None, response={200: Dict[str, Any], 401: Dict[str, Any], 400: Dict[str, Any]})
def whatsapp_cloud_inbound_ep(request):
    payload = {}
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except Exception:
        payload = {}
    data, status = wa_inbound(request.headers, request.body, payload)
    return status, data
