from sqlalchemy.orm import Session

from app.models.order import Order, OrderStatus


class OrderRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_order_by_id(self, order_id):
        return self.db.query(Order).where(Order.id == order_id).first()

    def get_order_by_user_id(self, user_id: int):
        return self.db.query(Order).where(Order.user_id == user_id).first()

    def get_order_by_user_id_and_status(self, user_id: int, status: OrderStatus):
        return (self.db.query(Order)
                .where(Order.user_id == user_id)
                .where(Order.status == status)
                .first())

    def get_order_by_user_id_and_order_id(self, user_id: int, order_id: int):
        return (self.db.query(Order)
                .where(Order.user_id == user_id)
                .where(Order.id == order_id)
                .first())

    def get_order_by_order_id_and_user_id(self, order_id: str, user_id: int):
        return (self.db.query(Order)
                .where(Order.user_id == user_id)
                .where(Order.order_id == order_id)
                .first())

    def get_orders_paginated(self, page: int, size: int):
        query = self.db.query(Order).order_by(Order.id.desc())
        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()
        return items, total

    def create_or_update(self, order: Order):
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)

    def update_order(self, order):
        self.db.add(order)
        self.db.commit()

    def delete(self, order: Order):
        self.db.delete(order)
        self.db.commit()
