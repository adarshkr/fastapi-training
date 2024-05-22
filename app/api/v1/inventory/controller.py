from typing import Any, Dict

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.inventory import inventory as CRUDInventory
from app.schemas.inventory import InventoryCreateBase, InventoryEdit, InventoryResponse


class ExceptionCustom(HTTPException):
    pass


class InventoryApi:
    @staticmethod
    def create_inventory(session: Session, *, inventory: InventoryCreateBase) -> int:
        return CRUDInventory.create(session, obj_in=inventory).id

    @staticmethod
    def get_inventories(session: Session) -> list[InventoryResponse]:
        inventories = CRUDInventory.get_multi(session)
        return [InventoryResponse(**inventory.to_dict()) for inventory in inventories]

    @staticmethod
    def get_inventory_by_name(session: Session, *, name: str) -> Dict[Any, Any]:
        inventory = CRUDInventory.get_inventory_by_name(session, name=name)

        if not inventory:
            raise ExceptionCustom(status_code=400, detail="Inventory not found")

        return inventory.to_dict()

    @staticmethod
    def get_inventory_by_id(session: Session, *, id: int) -> Dict[Any, Any] | None:
        inventory = CRUDInventory.get(session, id=id)

        if not inventory:
            raise ExceptionCustom(status_code=400, detail="Inventory not found")

        return inventory.to_dict()

    @staticmethod
    def update_inventory(session: Session, *, id: int, inventory: InventoryEdit) -> None:
        db_obj = CRUDInventory.get(session, id=id)
        if not db_obj:
            raise ExceptionCustom(status_code=400, detail="Inventory not found")

        CRUDInventory.update(session, db_obj=db_obj, obj_in=inventory)

    @staticmethod
    def delete_inventory(session: Session, *, id: int) -> None:
        db_obj = CRUDInventory.get(session, id=id)
       
        if not db_obj:
            raise ExceptionCustom(status_code=400, detail="Inventory not found")
       
        CRUDInventory.remove(session, id=id)
