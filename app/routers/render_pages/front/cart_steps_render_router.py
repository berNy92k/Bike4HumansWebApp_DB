from typing import Annotated

from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.models import User, Cart, Checkout, PaymentMethod
from app.routers.utils.admin_utils_router import redirect_to_login
from app.services.auth.auth_service import AuthService
from app.services.front.cart_service import CartService
from app.services.front.checkout_service import CheckoutService
from app.services.front.payment_methods_service import PaymentMethodService

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

        return templates.TemplateResponse(
            "front/cart/step1.html",
            {
                "request": request,
                "cart": cart,
            },
        )
    except HTTPException:
        return redirect_to_login()


@router.get("/step2", status_code=status.HTTP_200_OK)
async def render_cart_step2(request: Request, db: db_dependency):
    try:
        user: User = await AuthService(db).validate_access(request)

        checkout: Checkout = CheckoutService(db).get_checkout_by_user_id(user.id)
        methods: PaymentMethod = PaymentMethodService(db).get_methods()

        return templates.TemplateResponse(
            "front/cart/step2.html",
            {
                "request": request,
                "checkout": checkout,
                "payment_methods": methods,
            },
        )
    except HTTPException:
        return redirect_to_login()


@router.get("/step3", status_code=status.HTTP_200_OK)
async def render_cart_step3(request: Request):
    return templates.TemplateResponse(
        "front/cart/step3.html",
        {"request": request},
    )
