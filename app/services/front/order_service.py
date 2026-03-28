from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.checkout import Checkout, CheckoutStatus
from app.models.order import OrderItem, Order, OrderStatus
from app.repositories.bike_repository import BikeRepository
from app.repositories.checkout_repository import CheckoutRepository
from app.repositories.order_repository import OrderRepository


class OrderService:

    def __init__(self, db: Session):
        self.bike_repository = BikeRepository(db)
        self.order_repository = OrderRepository(db)
        self.checkout_repository = CheckoutRepository(db)

    def create_order(self, user_id: int):
        checkout: Checkout = self.checkout_repository.get_checkout_by_user_id(user_id)
        if not checkout or not checkout.items or len(checkout.items) == 0:
            raise HTTPException(status_code=404, detail="Checkout not found or empty")

        order_items: list[OrderItem] = []
        for item in checkout.items:
            order_items.append(OrderItem(
                bike_id=item.bike_id,
                quantity=item.quantity
            ))

        order = Order(
            user_id=checkout.user_id,
            currency=checkout.currency,
            payment_method_id=1,
            total_price=checkout.total_price,
        )
        order.items = order_items

        self.order_repository.create_or_update(order)

        checkout.status = CheckoutStatus.COMPLETED.name
        self.checkout_repository.create_or_update(checkout)

    def update_status(self, user_id: int, status: OrderStatus):
        order: Order = self.order_repository.get_order_by_user_id(user_id)
        if not order or not order.items or len(order.items) == 0:
            raise HTTPException(status_code=404, detail="Order not found or empty")

        order.status = status
        self.order_repository.create_or_update(order)

    def get_order_by_user_id(self, user_id: int):
        order: Order = self.order_repository.get_order_by_user_id(user_id)

        if not order:
            raise HTTPException(status_code=404, detail="Checkout not found")

        return order
