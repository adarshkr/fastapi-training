from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

storage = {}

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    in_stock: bool = True

@router.get("/{item_id}")
def read_item(item_id: str, q: str = None):
    item = storage.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if q:
        return {"item": item, "q": q}
    return {"item": item}

@router.post("/{item_id}")
def create_item(item_id: str, item: Item):
    if item_id in storage:
        raise HTTPException(status_code=400, detail="Item already exists")
    storage[item_id] = item.dict()
    return {"item_id": item_id, "item": item}

@router.put("/{item_id}")
def update_item(item_id: str, item: Item):
    if item_id not in storage:
        raise HTTPException(status_code=404, detail="Item not found")
    storage[item_id] = item.dict()
    return {"item_id": item_id, "item": item}

@router.delete("/{item_id}")
def delete_item(item_id: str):
    if item_id not in storage:
        raise HTTPException(status_code=404, detail="Item not found")
    del storage[item_id]
    return {"detail": "Item deleted"}