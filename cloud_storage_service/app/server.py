"""
core FastAPI app
"""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from cloud_storage_service.app.routers.storage import storage_router
from cloud_storage_service.app.routers.tasks import tasks_router
from cloud_storage_service.app.routers.users import users_router

app = FastAPI()

app.include_router(storage_router)
app.include_router(tasks_router)
app.include_router(users_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    """
    Welcome in root URL
    """
    return {'message': 'Welcome to CloudStorageManager!'}
