from ninja import NinjaAPI
from inventory.domain.errors import InventoryError
from api.routes.auth_router import router as auth_router
from inventory.routes import router as inventory_router
from contact.routes import router as contact_router
from api.auth.jwt_bearer import JWTBearer

api = NinjaAPI()

@api.exception_handler(InventoryError)
def inventory_error_handler(request, exc: InventoryError):
    return api.create_response(request, {"detail": str(exc)}, status=400)

api.add_router("/auth", auth_router)
api.add_router("/inventory", inventory_router, auth=JWTBearer())
api.add_router("/contacts", contact_router, auth=JWTBearer())

@api.get("/health")
def health():
    return {"status": "ok"}
