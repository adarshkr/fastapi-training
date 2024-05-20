from fastapi import FastAPI
from routes import items, sync_async, items_v2, items_v3, background_task, user, user_v1, upload

app = FastAPI()

app.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(sync_async.router, prefix="/process", tags=["process"])
app.include_router(items_v2.router, prefix="/items_v2", tags=["items_v2"])
app.include_router(items_v3.router, prefix="/items_v3", tags=["items_v3"])
app.include_router(background_task.router, prefix="/background", tags=["background"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(user_v1.router, prefix="/user_v1", tags=["user_v1"])
app.include_router(upload.router, prefix="/upload", tags=["upload"])