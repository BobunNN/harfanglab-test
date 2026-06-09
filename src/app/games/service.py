from uuid import UUID

from sqlmodel import Session

from src.app.games import repository
from src.app.games.exceptions import GameNotFoundException
from src.app.games.models import VideoGame
from src.app.games.schemas import VideoGameCreate, VideoGameFilters, VideoGamePatch


def create_video_game(session: Session, payload: VideoGameCreate) -> VideoGame:
    game = VideoGame.model_validate(payload)
    return repository.create_video_game(session, game)


def get_video_game(session: Session, uuid: UUID) -> VideoGame:
    game = repository.select_one(session, uuid)
    if not game:
        raise GameNotFoundException()
    return game


def patch_video_game(session: Session, uuid: UUID, payload: VideoGamePatch) -> VideoGame:
    game = repository.select_one(session, uuid)
    if not game:
        raise GameNotFoundException()
    return repository.patch_video_game(session, payload, uuid)


def search_video_games(session: Session, filters: VideoGameFilters) -> list[VideoGame]:
    return repository.search_video_games(session, filters)


def delete_video_game(session: Session, uuid: UUID) -> dict:
    game = repository.select_one(session, uuid)
    if not game:
        raise GameNotFoundException()
    return repository.delete_video_game(session, uuid)
