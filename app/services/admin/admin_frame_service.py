from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.frame import Frame
from app.repositories.frame_repository import FrameRepository
from app.schemas.admin.frames.admin_frame_create_dto import FrameCreateDto
from app.schemas.admin.frames.admin_frame_update_dto import FrameUpdateDto


class AdminFrameService:

    def __init__(self, db: Session):
        self.frame_repository = FrameRepository(db)

    def get_all_frames(self):
        return self.frame_repository.get_all_frames()

    def get_frame_by_id(self, frame_id):
        frame = self.frame_repository.get_frame_by_id(frame_id)

        if not frame:
            raise HTTPException(status_code=404, detail="Frame not found")

        return frame

    def create_frame(self, frame_create_dto: FrameCreateDto):
        frame = Frame(**frame_create_dto.model_dump())

        self.frame_repository.create_frame(frame)

    def update_frame_all_fields(self, frame_id: int, frame_update_dto: FrameUpdateDto):
        frame = self.get_frame_by_id(frame_id)
        update_frame_data = frame_update_dto.model_dump()

        for f, v in update_frame_data.items():
            setattr(frame, f, v)

        self.frame_repository.update_frame(frame)

    def update_frame_separate_fields(self, frame_id, frame_update_dto):
        frame = self.get_frame_by_id(frame_id)
        update_frame_data = frame_update_dto.model_dump(exclude_unset=True)

        for f, v in update_frame_data.items():
            setattr(frame, f, v)

        self.frame_repository.update_frame(frame)

    def delete_frame_by_id(self, frame_id):
        frame = self.get_frame_by_id(frame_id)

        self.frame_repository.delete(frame)
