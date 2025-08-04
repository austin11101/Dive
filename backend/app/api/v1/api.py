from fastapi import APIRouter
from app.api.v1.endpoints import auth
# from app.api.v1.endpoints import users, cv, templates, ai
# TODO: Create these modules

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    auth.router, prefix="/auth", tags=["authentication"]
)
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# TODO: Create users module
# api_router.include_router(cv.router, prefix="/cv", tags=["cv"])
# TODO: Create cv module
# api_router.include_router(templates.router, prefix="/templates", tags=["templates"])
# TODO: Create templates module
# api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
# TODO: Create ai module
