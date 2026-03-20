from sqlalchemy.orm import Session

from app.models.frame import Frame


class FrameRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all_frames(self):
        return self.db.query(Frame).all()

    def get_frame_by_id(self, frame_id):
        return self.db.query(Frame).where(Frame.id == frame_id).first()

    def create_frame(self, frame: Frame):
        self.db.add(frame)
        self.db.commit()

    def update_frame(self, frame: Frame):
        self.db.add(frame)
        self.db.commit()

    def delete(self, frame: Frame):
        self.db.delete(frame)
        self.db.commit()