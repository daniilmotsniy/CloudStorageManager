"""
this module contains Celery tasks check API
"""

from celery.result import AsyncResult
from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends

from app.core.auth import get_current_active_user

tasks_router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    dependencies=[Depends(get_current_active_user)],
)


@tasks_router.get('/tasks/{task_id}')
def get_status(task_id):
    """
    Allows to check status of celery task
    :param task_id: celery task id
    :return: processing status and result
    """
    task_result = AsyncResult(task_id)
    result = {
        'task_id': task_id,
        'task_status': task_result.status,
        'task_result': task_result.result
    }
    return JSONResponse(result)
