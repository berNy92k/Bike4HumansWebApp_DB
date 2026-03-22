from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.role import Role
from app.models.user import User
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.admin.user.admin_user_create_dto import UserCreateDto
from app.schemas.admin.user.role.admin_role_create_dto import RoleCreateDto
from app.schemas.admin.user.role.admin_role_update_dto import RoleUpdateDto

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AdminUserService:

    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)
        self.role_repository = RoleRepository(db)

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

    def get_all_roles(self):
        return self.role_repository.get_all_roles()

    def get_role_by_id(self, role_id: int):
        role = self.role_repository.get_role_by_id(role_id)

        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        return role

    def create_role(self, role_dto: RoleCreateDto):
        role = Role(**role_dto.model_dump())
        self.role_repository.create_role(role)

    def update_role_by_id(self, role_id: int, role_dto: RoleUpdateDto):
        role = self.get_role_by_id(role_id)

        role.name = role_dto.name
        role.description = role_dto.description

        self.role_repository.update_role(role)

    def delete_role_by_id(self, role_id):
        role = self.get_role_by_id(role_id)
        self.role_repository.delete_role(role)
