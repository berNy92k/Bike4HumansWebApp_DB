import enum
from datetime import datetime

from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.models.cart import Cart


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(150), nullable=False, unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=False)
    surname: Mapped[str] = mapped_column(String(150), nullable=False, unique=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow,
                                                 nullable=False)

    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), nullable=False, index=True)
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"), nullable=False, index=True)

    cart: Mapped[Cart] = relationship("Cart", back_populates="user")
    address: Mapped[Cart] = relationship("Address", back_populates="users")


class AddressType(str, enum.Enum):
    SHIPPING = "shipping"
    BILLING = "billing"


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    type: Mapped[str] = mapped_column(String, default=AddressType.SHIPPING.name, nullable=False)
    company_name: Mapped[str] = mapped_column(String, nullable=True)
    vat_number: Mapped[str] = mapped_column(String, nullable=True)
    address_line_1: Mapped[str] = mapped_column(String, nullable=False)
    address_line_2: Mapped[str] = mapped_column(String, nullable=True)
    city: Mapped[str] = mapped_column(String, nullable=False)
    postal_code: Mapped[str] = mapped_column(String, nullable=False)
    country_code: Mapped[str] = mapped_column(String, nullable=False)
    state_province: Mapped[str] = mapped_column(String, nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow,
                                                 nullable=False)

    users: Mapped[User] = relationship("User", back_populates="address")
