from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from ....services.visit_counter import VisitCounterService
from ....schemas.counter import VisitCount
from app.logging import logger

router = APIRouter()

_visit_counter_service_instance = None

def get_visit_counter_service():
    global _visit_counter_service_instance
    if _visit_counter_service_instance is None:
        _visit_counter_service_instance = VisitCounterService()
    return _visit_counter_service_instance

@router.post("/visit/{page_id}")
async def record_visit(
    page_id: str,
    counter_service: VisitCounterService = Depends(get_visit_counter_service)
):
    """Record a visit for a website"""
    try:
        await counter_service.increment_visit(page_id)
        return {"status": "success", "message": f"Visit recorded for page {page_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/visits/{page_id}", response_model=VisitCount)
async def get_visits(
    page_id: str,
    counter_service: VisitCounterService = Depends(get_visit_counter_service)
):
    """Get visit count for a website"""
    try:
        count = await counter_service.get_visit_count(page_id)
        served_via = "in_memory"
        return VisitCount(page_id=page_id, count=count, served_via=served_via)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 