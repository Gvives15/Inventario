from ninja import Router
from contact.schemas.webhook_schemas import WhatsAppInboundIn, WhatsAppInboundOut
from contact.modules.conversations.application.handlers.handle_whatsapp_inbound_h import execute as handle_whatsapp_inbound

router = Router()

@router.get("/")
def list_contacts(request):
    return {"message": "Hello from contacts"}


@router.post("/webhooks/whatsapp/inbound", response=WhatsAppInboundOut, auth=None)
def whatsapp_inbound_ep(request, payload: WhatsAppInboundIn):
    reply = handle_whatsapp_inbound(payload.dict())
    return {"reply": reply}
