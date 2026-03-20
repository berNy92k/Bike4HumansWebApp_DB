from sqlalchemy.orm import Session

from app.models.bike import Bike


class BikeRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all_bikes(self):
        return self.db.query(Bike).all()

    def get_bike_by_id(self, bike_id):
        return self.db.query(Bike).where(Bike.id == bike_id).first()

    def create_bike(self, bike):
        self.db.add(bike)
        self.db.commit()

    def update_bike(self, bike):
        self.db.add(bike)
        self.db.commit()

    def delete(self, bike: Bike):
        self.db.delete(bike)
        self.db.commit()