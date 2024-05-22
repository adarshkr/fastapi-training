from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base

class Inventory(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    in_stock: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )
