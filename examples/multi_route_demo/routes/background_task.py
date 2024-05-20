# In this example, the write_log function is a long-running task that we don't want to wait for before sending a response to the client. So, we add it to the background_tasks using the add_task method. The task will be started in the background, and FastAPI will send the response to the client immediately.
from fastapi import BackgroundTasks, APIRouter
from pydantic import BaseModel
import time

router = APIRouter()

class Item(BaseModel):
    name: str
    message: str

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        time.sleep(10)  # This could be a long running task
        log.write(message)

@router.post("/items/")
async def create_item(item: Item, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, item.message)
    return {"item": item, "message": "Message has been written to log in the background"}