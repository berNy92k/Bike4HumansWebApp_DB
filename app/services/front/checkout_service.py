from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Cart, CartItem, Bike
from app.models.checkout import Checkout, CheckoutItem
from app.repositories.bike_repository import BikeRepository
from app.repositories.cart_repository import CartRepository
from app.repositories.checkout_repository import CheckoutRepository


class CheckoutService:

    def __init__(self, db: Session):
        self.bike_repository = BikeRepository(db)
        self.cart_repository = CartRepository(db)
        self.checkout_repository = CheckoutRepository(db)

    def create_checkout(self, user_id: int):
        cart: Cart = self.cart_repository.get_cart_by_user_id(user_id)
        if not cart or not cart.items or len(cart.items) == 0:
            raise HTTPException(status_code=404, detail="Cart not found or empty")

        total_price: float = 0.0
        checkout_items: list[CheckoutItem] = []

        for item in cart.items:
            bike: Bike = self.bike_repository.get_bike_by_id(item.bike_id)
            total_price += bike.price * item.quantity

            checkout_items.append(CheckoutItem(
                bike_id = bike.id,
                quantity = bike.quantity
            ))

        checkout = Checkout(
            user_id = cart.user_id,
            currency = cart.currency,
            total_price = total_price,
        )
        checkout.items = checkout_items

        self.checkout_repository.create_or_update(checkout)