from fastapi import APIRouter
from app.schemas.request import RegressionRequest
from app.services.tasks import regression_task
from app.core.celery_app import celery_app
from celery.result import AsyncResult
from app.core.redis import redis_client

router = APIRouter()

@router.post("/run")
def run_regression(req: RegressionRequest):
    task = regression_task.delay(req.dict())
    return {"task_id": task.id}


@router.get("/status/{task_id}")
def task_status(task_id: str):
    data = redis_client.hgetall(f"task:{task_id}")
    if not data:
        return {"state": "PENDING", "percent": 0}
    return data

@router.get("/result/{task_id}")
def task_result(task_id: str):
    result = AsyncResult(task_id, app=celery_app)

    if result.state == "SUCCESS":
        return result.result

    return {
        "state": result.state
    }
