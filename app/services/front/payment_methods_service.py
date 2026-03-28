from sqlalchemy.orm import Session

from app.repositories.payment_methods_repository import PaymentMethodRepository


class PaymentMethodService:

    def __init__(self, db: Session):
        self.payment_method_repository = PaymentMethodRepository(db)

    def get_methods(self):
        return self.payment_method_repository.get_methods()
