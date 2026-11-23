from aiogram import Router
from .common import router as common_router
from .voice import router as voice_router

main_router = Router()
main_router.include_router(common_router)
main_router.include_router(voice_router)
