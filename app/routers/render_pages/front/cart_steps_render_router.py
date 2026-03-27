from typing import Annotated

from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.models import User, Cart, CartItem
from app.routers.utils.admin_utils_router import redirect_to_login
from app.services.auth.auth_service import AuthService
from app.services.front.bike_service import BikeService
from app.services.front.cart_service import CartService

router = APIRouter(
    prefix="/cart",
    include_in_schema=False
)

db_dependency = Annotated[Session, Depends(get_db)]
templates = Jinja2Templates(directory="app/templates")


@router.get("/step1", status_code=status.HTTP_200_OK)
async def render_cart_step1(request: Request, db: db_dependency):
    try:
        user: User = await AuthService(db).validate_access(request)

        cart: Cart = CartService(db).get_cart_by_user_id(user.id)
        bike = BikeService(db).get_bike_by_id(cart.items[0].bike_id)

        return templates.TemplateResponse(
            "front/cart/step1.html",
            {
                "request": request,
                "bike": bike,
                "cart": cart,
            },
        )
    except HTTPException:
        return redirect_to_login()


@router.get("/step2", status_code=status.HTTP_200_OK)
async def render_cart_step2(request: Request):
    return templates.TemplateResponse(
        "front/cart/step2.html",
        {"request": request},
    )


@router.get("/step3", status_code=status.HTTP_200_OK)
async def render_cart_step3(request: Request):
    return templates.TemplateResponse(
        "front/cart/step3.html",
        {"request": request},
    )
