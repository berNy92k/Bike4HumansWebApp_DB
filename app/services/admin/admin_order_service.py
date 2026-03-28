from sqlalchemy.orm import Session

from app.repositories.order_repository import OrderRepository
from app.schemas.admin.order.admin_order_list_request_dto import OrderListRequestDto
from app.schemas.admin.order.admin_order_list_response_dto import OrderListResponseDto
from app.schemas.admin.order.admin_order_read_dto import OrderReadDto


class AdminOrderService:

    def __init__(self, db: Session):
        self.order_repository = OrderRepository(db)

    def get_orders_paginated(self, request_dto: OrderListRequestDto) -> OrderListResponseDto:
        items, total = self.order_repository.get_orders_paginated(
            page=request_dto.page,
            size=request_dto.size,
        )
        pages = (total + request_dto.size - 1) // request_dto.size if total > 0 else 0

        orders = [OrderReadDto.model_validate(order_item) for order_item in items]

        return OrderListResponseDto(
            orders=orders,
            page=request_dto.page,
            size=request_dto.size,
            total=total,
            pages=pages,
        )

    def delete_order_by_id(self, order_id):
        order = self.order_repository.get_order_by_id(order_id)

        self.order_repository.delete(order)
