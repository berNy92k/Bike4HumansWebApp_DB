import datetime
from datetime import timezone, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.models import User
from app.schemas.auth.user_create_dto import UserCreateDto
from app.services.auth.user_service import UserService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
SECRET_KEY = "aADASDsadasd213123123"
ALGORITHM = "HS256"

db_dependency = Annotated[Session, Depends(get_db)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

templates = Jinja2Templates(directory="app/templates")


### Pages ###
@router.get("/login", response_class=HTMLResponse, include_in_schema=False)
async def render_login_page(request: Request):
    return templates.TemplateResponse("authentication/login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse, include_in_schema=False)
async def render_register_page(request: Request):
    return templates.TemplateResponse("authentication/register.html", {"request": request})


### ENDPOINTS ###
@router.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user: UserCreateDto):
    service = UserService(db)
    service.create_user(user)


@router.post("/token", status_code=status.HTTP_201_CREATED)
async def create_token(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user: User = _authenticate_user(form_data.username, form_data.password, db)

    minutes : int = 5
    token = _generate_jwt_token(form_data.username, user.id, user.role_id, timedelta(minutes=minutes))

    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=token, httponly=True, samesite="lax",
                        secure=False, max_age=minutes * 60, path="/")
    return response


def _authenticate_user(username: str, password: str, db: Session) -> User:
    service = UserService(db)
    user: User = service.find_user_by_username(username)
    print(user)
    if not bcrypt_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="User is not authorized")

    return user


def _generate_jwt_token(username: str, user_id: int, role_id: int, expire_delta: timedelta):
    token = {"sub": username, "id": user_id, "role_id": role_id}
    expire = datetime.datetime.now(timezone.utc) + expire_delta
    token.update({"exp": expire})

    return jwt.encode(token, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        role_id: str = payload.get("role_id")
        exp: datetime.datetime = payload.get("exp")

        if username is None or user_id is None or role_id is None or exp is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authorized")

        return {"username": username, "user_id": user_id, "role_id": role_id, "exp": exp}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authorized")
