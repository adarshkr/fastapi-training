from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base

class User(Base):
    name: Mapped[str]
    lastname: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )
