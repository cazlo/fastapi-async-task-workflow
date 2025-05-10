from fastapi import APIRouter
from app.api.celery_task import increment
from celery.result import AsyncResult
from pydantic import BaseModel

router = APIRouter()


class TaskInput(BaseModel):
    delay: int


class TaskResponse(BaseModel):
    task_id: str
    status: str
    ready: bool
    result: int | None


@router.post("/increment_task", response_model=TaskResponse)
async def queue_increment_task(input_data: TaskInput):
    task_result = increment.apply_async(args=(input_data.delay,))
    return TaskResponse(
        task_id=task_result.id,
        status="started",
        ready=task_result.ready(),
        result=task_result.result if task_result.ready() else None,
    )


@router.get("/increment_task/{task_id}", response_model=TaskResponse)
async def get_increment_task_result(task_id: str):
    task_result = AsyncResult(task_id)
    print(task_result)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "ready": task_result.ready(),
        "result": task_result.result if task_result.ready() else None,
    }
