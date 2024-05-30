from datetime import datetime

from pydantic import BaseModel


class InventoryBase(BaseModel):
    name: str
    description: str
    price: float
    in_stock: bool

class InventoryCreateBase(InventoryBase):
    name: str
    description: str
    price: float
    in_stock: bool
    created_by: int

class InventoryCreateResponse(BaseModel):
    id: int

class InventoryResponse(InventoryBase):
    id: int
    created_by: str
    created_at: datetime
    updated_at: datetime

class InventoryEdit(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    in_stock: bool | None = None
