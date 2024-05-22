from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.inventory import Inventory
from app.schemas.inventory import InventoryCreateBase, InventoryEdit


class CRUDInventory(CRUDBase[Inventory, InventoryCreateBase, InventoryEdit]):
    def get_inventory_by_name(self, session: Session, *, name: str) -> Inventory | None:
        inventory = session.query(Inventory).filter(Inventory.name == name).first()

        if not inventory:
            return None

        return inventory


inventory = CRUDInventory(Inventory)
