import enum
from datetime import datetime

from sqlalchemy import Integer, DateTime, ForeignKey, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    DELIVERY = "delivery"
    COMPLETED = "completed"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False, index=True, unique=True)
    currency: Mapped[str] = mapped_column(String, default="PLN", nullable=False)
    status: Mapped[str] = mapped_column(String, default=OrderStatus.PENDING.name, nullable=False)
    total_price: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    payment_method_id: Mapped[int] = mapped_column(ForeignKey("payment_methods.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow,
                                                 nullable=False)

    user = relationship("User")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False, index=True)
    bike_id: Mapped[int] = mapped_column(ForeignKey("bikes.id"), nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow,
                                                 nullable=False)

    order = relationship("Order", back_populates="items")
    bike = relationship("Bike")
