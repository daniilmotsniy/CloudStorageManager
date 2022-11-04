from fastapi import FastAPI

from app.routers.storage import storage_router
from app.routers.tasks import tasks_router

app = FastAPI()

app.include_router(storage_router)
app.include_router(tasks_router)


@app.get('/')
async def root():
    return {'message': 'Welcome to CloudStorageManager!'}


# if __name__ == '__main__':
#     uvicorn.run('app:app', host='localhost', port=8080, reload=True)
