from sqlalchemy.orm import Session

from app.models.manufacturer import Manufacturer


class ManufacturerRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all_manufacturers(self):
        return self.db.query(Manufacturer).all()

    def get_manufacturer_by_id(self, manufacturer_id):
        return self.db.query(Manufacturer).where(Manufacturer.id == manufacturer_id).first()

    def create_manufacturer(self, manufacturer):
        self.db.add(manufacturer)
        self.db.commit()

    def update_manufacturer(self, manufacturer):
        self.db.add(manufacturer)
        self.db.commit()

    def delete(self, manufacturer: Manufacturer):
        self.db.delete(manufacturer)
        self.db.commit()
