from fastapi import APIRouter, Depends
from app.api.v1.auth.route import auth_router
from app.api.v1.user.route import user_router
from app.api.v1.inventory.route import inventory_router
from app.api.dependencies.security import validate_user

api_router = APIRouter()
api_router.include_router(
    auth_router,
)
api_router.include_router(
    user_router,
    dependencies=[Depends(validate_user)],
)
api_router.include_router(
    inventory_router,
    dependencies=[Depends(validate_user)],
)