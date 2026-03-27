from sqlalchemy.orm import Session

from app.models.checkout import Checkout


class CheckoutRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_or_update(self, checkout: Checkout):
        self.db.add(checkout)
        self.db.commit()
        self.db.refresh(checkout)

    def update_cart(self, checkout: Checkout):
        self.db.add(checkout)
        self.db.commit()

    def delete(self, checkout: Checkout):
        self.db.delete(checkout)
        self.db.commit()
