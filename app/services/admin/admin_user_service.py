from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.admin.user.admin_user_create_dto import UserCreateDto

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AdminUserService:

    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def get_all_users(self):
        return self.user_repository.get_all_users()

    def create_user(self, user_dto: UserCreateDto):
        user = User(
            username=user_dto.username,
            email=user_dto.email,
            name=user_dto.name,
            surname=user_dto.surname,
            is_active=user_dto.is_active,
            email_verified=user_dto.email_verified,
            hashed_password=bcrypt_context.hash(user_dto.password),
            role_id=user_dto.role_id,
        )
        self.user_repository.create_user(user)
