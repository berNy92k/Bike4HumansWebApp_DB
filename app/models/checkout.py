import enum
from datetime import datetime

from sqlalchemy import Integer, DateTime, ForeignKey, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base

class CheckoutStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class Checkout(Base):
    __tablename__ = "checkouts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False, index=True, unique=True)
    currency: Mapped[str] = mapped_column(String, default="PLN", nullable=False)
    status: Mapped[str] = mapped_column(String, default="PENDING", nullable=False)
    total_price: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User")
    items = relationship("CheckoutItem", back_populates="checkout", cascade="all, delete-orphan")

class CheckoutItem(Base):
    __tablename__ = "checkout_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    checkout_id: Mapped[int] = mapped_column(ForeignKey("checkouts.id"), nullable=False, index=True)
    bike_id: Mapped[int] = mapped_column(ForeignKey("bikes.id"), nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow,nullable=False)

    checkout = relationship("Checkout", back_populates="items")
    bike = relationship("Bike")