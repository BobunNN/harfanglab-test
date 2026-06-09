from uuid import UUID

from sqlmodel import Session, select

from src.app.games.models import VideoGame
from src.app.games.schemas import VideoGameFilters, VideoGamePatch


def create_video_game(session: Session, new_video_game: VideoGame) -> VideoGame:
    session.add(new_video_game)
    session.commit()
    session.refresh(new_video_game)
    return new_video_game


def patch_video_game(
    session: Session, video_game_update: VideoGamePatch, uuid: UUID
) -> VideoGame:
    video_game_record = session.get(VideoGame, uuid)
    update_data = video_game_update.model_dump(exclude_unset=True)

    video_game_record.sqlmodel_update(update_data)
    session.add(video_game_record)
    session.commit()
    session.refresh(video_game_record)
    return video_game_record


def delete_video_game(session: Session, uuid: UUID):
    game = session.get(VideoGame, uuid)
    session.delete(game)
    session.commit()
    return {"ok": True}


def search_video_games(session: Session, filters: VideoGameFilters) -> list[VideoGame]:
    query = select(VideoGame)
    if filters.name:
        query = query.where(VideoGame.name.ilike(f"%{filters.name}%"))
    if filters.studio:
        query = query.where(VideoGame.studio.ilike(f"%{filters.studio}%"))
    if filters.platform:
        query = query.where(VideoGame.platform == filters.platform)
    if filters.release_date_from:
        query = query.where(VideoGame.release_date >= filters.release_date_from)
    if filters.release_date_to:
        query = query.where(VideoGame.release_date <= filters.release_date_to)
    if filters.min_ratings is not None:
        query = query.where(VideoGame.ratings >= filters.min_ratings)
    if filters.max_ratings is not None:
        query = query.where(VideoGame.ratings <= filters.max_ratings)
    query = query.offset(filters.offset).limit(filters.limit)
    return list(session.exec(query).all())


def select_one(session: Session, uuid: UUID) -> VideoGame | None:
    return session.get(VideoGame, uuid)
