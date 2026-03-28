from typing import Annotated

from fastapi import APIRouter, Depends, Request, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.models import User, Checkout
from app.routers.utils.admin_utils_router import redirect_to_login
from app.services.auth.auth_service import AuthService
from app.services.front.checkout_service import CheckoutService

router = APIRouter(
    prefix="/order",
    include_in_schema=False
)

db_dependency = Annotated[Session, Depends(get_db)]
templates = Jinja2Templates(directory="app/templates")


@router.get("/order", status_code=status.HTTP_200_OK)
async def render_payment_result(db: db_dependency, request: Request):
    try:
        user: User = await AuthService(db).validate_access(request)

        checkout: Checkout = CheckoutService(db).get_checkout_by_user_id(user.id)

        return templates.TemplateResponse(
            "front/order/order.html",
            {
                "request": request,
                "checkout": checkout,
                "checkout_id": checkout.id,
                "tax": 0,
                "payment_method_id": checkout.payment_method_id,
                "payment_status": payment_status
            },
        )
    except HTTPException:
        return redirect_to_login()
