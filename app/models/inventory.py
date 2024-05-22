from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict
from sqlalchemy import ForeignKey, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.user import User

from app.db.base_class import Base

class Inventory(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    in_stock: Mapped[bool]
    created_by: Mapped[int] = mapped_column(ForeignKey("user.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

    UniqueConstraint("name", "created_by", name="inventory_name_created_by_key"),

    user: Mapped["User"] = relationship()

    def to_dict(self) -> Dict[Any, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "in_stock": self.in_stock,
            "created_by": self.user.username,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
