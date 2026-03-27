from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import CartItem
from app.models.cart import Cart
from app.repositories.bike_repository import BikeRepository
from app.repositories.cart_repository import CartRepository
from app.schemas.admin.bike.admin_bike_list_request_dto import BikeListRequestDto
from app.schemas.admin.bike.admin_bike_list_response_dto import BikeListResponseDto
from app.schemas.admin.bike.admin_bike_read_dto import BikeReadDto


class CartService:

    def __init__(self, db: Session):
        self.cart_repository = CartRepository(db)
        self.bike_repository = BikeRepository(db)

    def add_item_to_cart(self, user_id: int, bike_id: int):
        bike = self.bike_repository.get_bike_by_id(bike_id)
        if not bike:
            raise HTTPException(status_code=404, detail="Bike not found")

        cart_item = CartItem(
            bike_id=bike_id,
            quantity=1,
        )

        cart = self.cart_repository.get_cart_by_user_id(user_id)
        if not cart:
            cart = Cart(
                user_id=user_id,
                currency="PLN",
                status="PENDING",
            )

        
        cart.items.append(cart_item)
        
        self.cart_repository.create_or_update(cart)

    def get_cart_by_user_id(self, user_id: int):
        cart = self.cart_repository.get_cart_by_user_id(user_id)

        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        return cart
