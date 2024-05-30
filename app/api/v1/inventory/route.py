import logging

from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from app.api.v1.inventory.controller import InventoryApi
from app.core.base_response import BaseResponse
from app.db.session import acquire_db_session
from app.schemas.inventory import InventoryBase, InventoryCreateBase, InventoryCreateResponse, InventoryEdit, InventoryResponse

logger = logging.getLogger(__name__)


inventory_router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)


@inventory_router.get("", response_model=dict)
def get_inventories(
    session: Session = Depends(acquire_db_session),
) -> dict:
    try:
        inventories = InventoryApi.get_inventories(session)
        return BaseResponse.from_result(result=inventories).dict()
    except Exception as e:
        logger.error(e)
        raise e


@inventory_router.get("/{name}", response_model=dict)
def get_inventory(
    name: str,
    session: Session = Depends(acquire_db_session),
) -> dict:
    try:
        inventory = InventoryApi.get_inventory_by_name(session, name=name)
        return BaseResponse.from_result(result=InventoryResponse(**inventory)).dict()
    except Exception as e:
        logger.error(e)
        raise e


@inventory_router.post("", response_model=dict)
def create_inventory(
    request: Request,
    inventory: InventoryBase,
    session: Session = Depends(acquire_db_session),
) -> dict:
    try:
        created_by = request.user.get("id")
        inventory_id: int = InventoryApi.create_inventory(session, inventory=InventoryCreateBase(**inventory.model_dump(), created_by=created_by))
        return BaseResponse.from_result(result=InventoryCreateResponse(id=inventory_id)).dict()
    except Exception as e:
        logger.error(e)
        raise e


@inventory_router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_inventory(
    id: int,
    inventory: InventoryEdit,
    session: Session = Depends(acquire_db_session),
) -> None:
    try:
        InventoryApi.update_inventory(session, id=id, inventory=inventory)
    except Exception as e:
        logger.error(e)
        raise e


@inventory_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory(
    id: int,
    session: Session = Depends(acquire_db_session),
) -> None:
    try:
        InventoryApi.delete_inventory(session, id=id)
    except Exception as e:
        logger.error(e)
        raise e
