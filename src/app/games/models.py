import uuid

from sqlmodel import Field

from src.app.games.schemas import VideoGameBase


class VideoGame(VideoGameBase, table=True):
    uuid: uuid.UUID | None = Field(
        default_factory=uuid.uuid4, nullable=False, primary_key=True
    )
