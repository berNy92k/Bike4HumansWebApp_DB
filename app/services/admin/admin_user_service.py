from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository


class AdminUserService:

    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def get_all_users(self):
        return self.user_repository.get_all_users()
