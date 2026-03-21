from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all_users(self):
        return self.db.query(User).order_by(User.created_at.desc()).all()

    def create_user(self, user: User):
        self.db.add(user)
        self.db.commit()