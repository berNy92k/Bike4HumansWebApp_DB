from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.manufacturer import Manufacturer
from app.repositories.manufacturer_repository import ManufacturerRepository
from app.schemas.admin.manufacturers.admin_manufacturer_create_dto import ManufacturerCreateDto
from app.schemas.admin.manufacturers.admin_manufacturer_update_dto import ManufacturerUpdateDto


class ManufacturerService:

    def __init__(self, db: Session):
        self.manufacturer_repository = ManufacturerRepository(db)

    def get_all_manufacturers(self):
        return self.manufacturer_repository.get_all_manufacturers()

    def get_manufacturer_by_id(self, manufacturer_id):
        manufacturer = self.manufacturer_repository.get_manufacturer_by_id(manufacturer_id)

        if not manufacturer:
            raise HTTPException(status_code=404, detail="Manufacturer not found")

        return manufacturer

    def create_manufacturer(self, manufacturer_create_dto: ManufacturerCreateDto):
        manufacturer = Manufacturer(**manufacturer_create_dto.model_dump())

        self.manufacturer_repository.create_manufacturer(manufacturer)

    def update_manufacturer_all_fields(self, manufacturer_id: int, manufacturer_update_dto: ManufacturerUpdateDto):
        manufacturer = self.get_manufacturer_by_id(manufacturer_id)
        update_manufacturer_data = manufacturer_update_dto.model_dump()

        for f, v in update_manufacturer_data.items():
            setattr(manufacturer, f, v)

        self.manufacturer_repository.update_manufacturer(manufacturer)

    def update_manufacturer_separate_fields(self, manufacturer_id, manufacturer_update_dto):
        manufacturer = self.get_manufacturer_by_id(manufacturer_id)
        update_manufacturer_data = manufacturer_update_dto.model_dump(exclude_unset=True)

        for f, v in update_manufacturer_data.items():
            setattr(manufacturer, f, v)

        self.manufacturer_repository.update_manufacturer(manufacturer)

    def delete_manufacturer_by_id(self, manufacturer_id):
        manufacturer = self.get_manufacturer_by_id(manufacturer_id)

        self.manufacturer_repository.delete(manufacturer)
