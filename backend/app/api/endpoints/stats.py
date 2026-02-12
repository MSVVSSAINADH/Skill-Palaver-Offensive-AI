from fastapi import APIRouter
from app.core.stats import stats_service

router = APIRouter()

@router.get("/")
def get_dashboard_stats():
    return stats_service.get_stats()
