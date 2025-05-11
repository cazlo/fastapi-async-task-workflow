from fastapi import APIRouter
from app.api.celery_task import increment
from celery.result import AsyncResult
from celery.states import REVOKED
from pydantic import BaseModel

router = APIRouter()


class TaskInput(BaseModel):
    delay: int         # how much time the task sleeps for before doing the increment
    countdown: int = 0 # delay before the task can be started


class TaskResponse(BaseModel):
    task_id: str
    status: str
    ready: bool
    result: int | None


@router.post("/increment_task", response_model=TaskResponse, status_code=201)
async def queue_increment_task(input_data: TaskInput):
    task_result = increment.apply_async(args=(input_data.delay,), countdown=input_data.countdown)
    ready = task_result.ready()
    return TaskResponse(
        task_id=task_result.id,
        status="QUEUED",
        ready=ready,
        result=task_result.result if ready else None,
    )


@router.get("/increment_task/{task_id}", response_model=TaskResponse)
async def get_increment_task_result(task_id: str):
    task_result = AsyncResult(task_id)
    ready = task_result.ready()
    return TaskResponse(
        task_id=task_result.id,
        status=task_result.status,
        ready=ready,
        result=task_result.result if ready and not task_result.status == REVOKED else None,
    )

@router.delete("/increment_task/{task_id}", response_model=TaskResponse)
async def get_increment_task_result(task_id: str):
    task_result = AsyncResult(task_id)
    task_result.revoke() # this will remove it from queue but not stop the job from processing if it has already started
    task_result = AsyncResult(task_id)
    ready = task_result.ready()
    return TaskResponse(
        task_id=task_result.id,
        status=task_result.status,
        ready=task_result.ready(),
        result=task_result.result if ready and not task_result.status == REVOKED else None,
    )