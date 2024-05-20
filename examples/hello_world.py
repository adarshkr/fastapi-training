# Hello World Example

from fastapi import FastAPI

app = FastAPI()

# Non-persistent storage
# Here we're using a simple in-memory dictionary to simulate storage.
# In a real-world application, this could be a database.
storage = {}

@app.get("/")
async def root():
    return {"message": "Hello World"}
