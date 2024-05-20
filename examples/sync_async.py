# Sync Async Example
from fastapi import FastAPI
import time
import asyncio

app = FastAPI()

@app.get("/sync")
def sync_route():
    # This is a synchronous route.
    # While this route is processing a request, the server cannot process other requests.
    # This can lead to performance issues if the route takes a long time to process a request.
    time.sleep(1)  # Simulate a long process.
    return {"message": "This is a synchronous route"}

@app.get("/async")
async def async_route():
    # This is an asynchronous route.
    # While this route is waiting for a response (e.g., from a database or an API), the server can process other requests.
    # This can lead to better performance for routes that spend a lot of time waiting for responses.
    await asyncio.sleep(1)  # Simulate a long process.
    return {"message": "This is an asynchronous route"}