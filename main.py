
# This code adds a new Item model, a query parameter to the read_item function, a delete_item function, and error handling using HTTPException. It also changes the create_item function to use the Item model for the request body.
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

storage = {}

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    in_stock: bool = True

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: str, q: str = None):
    # Query parameters are defined as function arguments.
    # They are automatically interpreted as optional.
    item = storage.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found!!!")
    if q:
        return {"item": item, "q": q}
    return {"item": item}

@app.post("/items/{item_id}")
def create_item(item_id: str, item: Item):
    # Request bodies are defined using Pydantic models.
    # They provide automatic request validation and serialization.
    if item_id in storage:
        raise HTTPException(status_code=400, detail="Item already exists")
    storage[item_id] = item.dict()
    return {"item_id": item_id, "item": item}

@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    # FastAPI allows you to define all standard HTTP methods.
    # Here we're defining a DELETE operation.
    if item_id not in storage:
        raise HTTPException(status_code=404, detail="Item not found")
    del storage[item_id]
    return {"detail": "Item deleted"}
