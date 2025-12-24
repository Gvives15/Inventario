from ninja import NinjaAPI
from inventory.src.domain.errors import InventoryError
from inventory.src.api.routes.auth_router import router as auth_router
from inventory.src.api.routes.inventory_router import router as inventory_router
from inventory.src.api.auth.jwt_bearer import JWTBearer

api = NinjaAPI()

@api.exception_handler(InventoryError)
def inventory_error_handler(request, exc: InventoryError):
    return api.create_response(request, {"detail": str(exc)}, status=400)

api.add_router("/auth", auth_router)
api.add_router("/inventory", inventory_router, auth=JWTBearer())

@api.get("/health")
def health():
    return {"status": "ok"}
