from fastapi import APIRouter

from router.text_report_router import text_report_router

api_router = APIRouter(prefix='/public')

api_router.include_router(text_report_router, prefix='/report')
