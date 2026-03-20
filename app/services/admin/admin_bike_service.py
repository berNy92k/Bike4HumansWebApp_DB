from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.bike import Bike
from app.repositories.bike_repository import BikeRepository
from app.schemas.admin.bike.admin_bike_create_dto import BikeCreateDto
from app.schemas.admin.bike.admin_bike_update_dto import BikeUpdateDto


class AdminBikeService:

    def __init__(self, db: Session):
        self.bike_repository = BikeRepository(db)

    def get_all_bikes(self):
        return self.bike_repository.get_all_bikes()

    def get_bike_by_id(self, bike_id):
        bike = self.bike_repository.get_bike_by_id(bike_id)

        if not bike:
            raise HTTPException(status_code=404, detail="Bike not found")

        return bike

    def create_bike(self, bike_create_dto: BikeCreateDto):
        bike = Bike(**bike_create_dto.model_dump())

        self.bike_repository.create_bike(bike)

    def update_bike_all_fields(self, bike_id: int, bike_update_dto: BikeUpdateDto):
        bike = self.get_bike_by_id(bike_id)
        update_bike_data = bike_update_dto.model_dump()

        for f, v in update_bike_data.items():
            setattr(bike, f, v)

        self.bike_repository.update_bike(bike)

    def update_bike_separate_fields(self, bike_id, bike_update_dto):
        bike = self.get_bike_by_id(bike_id)
        update_bike_data = bike_update_dto.model_dump(exclude_unset=True)

        for f, v in update_bike_data.items():
            setattr(bike, f, v)

        self.bike_repository.update_bike(bike)

    def delete_bike_by_id(self, bike_id):
        bike = self.get_bike_by_id(bike_id)

        self.bike_repository.delete(bike)
