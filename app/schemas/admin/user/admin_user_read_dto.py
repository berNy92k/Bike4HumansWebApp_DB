from datetime import datetime

from pydantic import BaseModel


class UserReadDto(BaseModel):
    id: int
    username: str
    email: str
    name: str
    surname: str
    role: str
    is_active: bool
    email_verified: bool
    last_login: datetime | None = None
    created_at: datetime
    updated_at: datetime