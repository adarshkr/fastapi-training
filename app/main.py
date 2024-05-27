
# This code adds a new Item model, a query parameter to the read_item function, a delete_item function, and error handling using HTTPException. It also changes the create_item function to use the Item model for the request body.
from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
import uvicorn
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.db.base import Base
from app.db.db import db_engine, acquire_db_session
from app.models.inventory import Inventory
app = FastAPI()


Base.metadata.create_all(bind=db_engine)

class InventoryRequest(BaseModel):
    name: str
    description: str
    price: float
    in_stock: bool = True

class InventoryUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    in_stock: bool | None = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/inventory/{item_id}")
def read_item(item_id: int, q: str = None, session: Session = Depends(acquire_db_session)):
    # Query parameters are defined as function arguments.
    # They are automatically interpreted as optional.
    item = session.query(Inventory).filter(Inventory.id == item_id).first()
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found!!!")

    return {"item": item}

@app.get("/inventory")
def read_items(items_list: list[int | None] = Query(default=None), session: Session = Depends(acquire_db_session)):
    query = session.query(Inventory)

    if items_list:
        query = query.filter(Inventory.id.in_(items_list))
        
    return query.all()

@app.post("/inventory")
def create_item(item: InventoryRequest, session: Session = Depends(acquire_db_session)):
    # Request bodies are defined using Pydantic models.
    # They provide automatic request validation and serialization.

    inventory = session.query(Inventory).filter(Inventory.name == item.name).first()

    if inventory:
        raise HTTPException(status_code=400, detail="Item already exists")
    
    new_inventory = session.add(Inventory(**item.model_dump()))
    session.commit()
    
    # session.refresh(new_inventory)


    return {"id": new_inventory.id}

@app.put("/inventory/{item_id}")
def update_item(item_id:int, item: InventoryUpdateRequest, session: Session = Depends(acquire_db_session)):
    # Request bodies are defined using Pydantic models.
    # They provide automatic request validation and serialization.

    inventory = session.query(Inventory).filter(Inventory.id == item_id).first()

    if not inventory:
        raise HTTPException(status_code=404, detail="Item not found!!!")
    
    obj_data = jsonable_encoder(item)

    if isinstance(inventory, dict):
        update_data = item
    else:
        update_data = item.model_dump(exclude_unset=True, exclude_none=True)

    for field in obj_data:
        if field in update_data:
            setattr(inventory, field, update_data[field])

    session.add(inventory)
    session.commit()
    
    return {"status":"success"}

@app.delete("/inventory/{item_id}")
def delete_item(item_id: int, session: Session = Depends(acquire_db_session)):
    # FastAPI allows you to define all standard HTTP methods.
    # Here we're defining a DELETE operation.
    inventory = session.query(Inventory).filter(Inventory.id == item_id).first()

    if not inventory:
        raise HTTPException(status_code=404, detail="Item not found!!!")
    
    session.delete(inventory)
    session.commit()

    return {"status":"success"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
