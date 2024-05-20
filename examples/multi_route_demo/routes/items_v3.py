# In this version, I've added a new ItemInResponse model that includes the item_id along with the item. I've also updated the response_model parameters of the route decorators to use this new model. This will ensure that the responses from these routes always match the shape of the ItemInResponse model.
from fastapi import APIRouter, HTTPException, Body, Path
from pydantic import BaseModel, Field

router = APIRouter()

storage = {}

class Item(BaseModel):
    name: str = Field(..., title="The name of the item", max_length=100)
    description: str = Field(None, title="The description of the item", max_length=300)
    price: float = Field(..., title="The price of the item", gt=0)
    in_stock: bool = Field(True, title="Whether the item is in stock")

class ItemInResponse(BaseModel):
    item_id: str
    item: Item

@router.get("/{item_id}", response_model=ItemInResponse)
def read_item(item_id: str = Path(..., title="The ID of the item to get", example="1234")):
    item = storage.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "item": item}

@router.post("/{item_id}", response_model=ItemInResponse)
def create_item(item_id: str = Path(..., title="The ID of the item to create", example="1234"), 
                item: Item = Body(..., example={"name": "Foo", "description": "A very nice Item", "price": 99.99, "in_stock": True})):
    if item_id in storage:
        raise HTTPException(status_code=400, detail="Item already exists")
    storage[item_id] = item.dict()
    return {"item_id": item_id, "item": item}

@router.delete("/{item_id}", response_model=ItemInResponse)
def delete_item(item_id: str = Path(..., title="The ID of the item to delete", example="1234")):
    if item_id not in storage:
        raise HTTPException(status_code=404, detail="Item not found")
    item = storage[item_id]
    del storage[item_id]
    return {"item_id": item_id, "item": item}