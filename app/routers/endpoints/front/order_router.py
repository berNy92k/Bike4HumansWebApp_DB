from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.database.database import get_db
from app.services.auth.auth_service import get_current_user
from app.services.front.order_service import OrderService

current_user_dependency = Annotated[dict, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/order",
    tags=["Order"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(logged_user: current_user_dependency, db: db_dependency):
    service = OrderService(db)
    service.create_order(logged_user.get("user_id"))
