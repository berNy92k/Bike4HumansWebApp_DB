from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Cart, Bike
from app.models.cart import CartStatus
from app.models.checkout import Checkout, CheckoutItem
from app.repositories.bike_repository import BikeRepository
from app.repositories.checkout_repository import CheckoutRepository
from app.repositories.order_repository import OrderRepository


class OrderService:

    def __init__(self, db: Session):
        self.bike_repository = BikeRepository(db)
        self.checkout_repository = CheckoutRepository(db)
        self.order_repository = OrderRepository(db)

    def create_order(self, user_id: int):
        cart: Cart = self.cart_repository.get_cart_by_user_id(user_id)
        if not cart or not cart.items or len(cart.items) == 0:
            raise HTTPException(status_code=404, detail="Cart not found or empty")

        total_price: Decimal = Decimal("0.0")
        checkout_items: list[CheckoutItem] = []

        for item in cart.items:
            bike: Bike = self.bike_repository.get_bike_by_id(item.bike_id)
            total_price += bike.price * item.quantity

            checkout_items.append(CheckoutItem(
                bike_id=bike.id,
                quantity=item.quantity
            ))

        checkout = Checkout(
            user_id=cart.user_id,
            currency=cart.currency,
            payment_method_id=1,
            total_price=float(total_price),
        )
        checkout.items = checkout_items

        self.checkout_repository.create_or_update(checkout)

        cart.status = CartStatus.COMPLETED.name
        self.cart_repository.create_or_update(cart)

    def get_order_by_user_id(self, user_id: int):
        checkout: Checkout = self.checkout_repository.get_checkout_by_user_id(user_id)

        if not checkout:
            raise HTTPException(status_code=404, detail="Checkout not found")

        return checkout
