"""
API v1 routes.
"""
from fastapi import APIRouter
from app.api.v1 import requirements, sub_requirements, checklist, uploads, analytics, auth

api_router = APIRouter()

api_router.include_router(requirements.router, prefix="/requirements", tags=["requirements"])
api_router.include_router(sub_requirements.router, prefix="/requirements", tags=["sub-requirements"])
api_router.include_router(checklist.router, prefix="/requirements", tags=["checklist"])
api_router.include_router(uploads.router, prefix="/upload", tags=["uploads"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])


