from fastapi import APIRouter

from .api import router as api_router
from .views import router as views_router


router = APIRouter()

router.include_router(api_router)
router.include_router(views_router, include_in_schema=False)  # frontend не отображаем в Swagger
