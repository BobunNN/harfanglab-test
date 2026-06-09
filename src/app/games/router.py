from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.app.dependencies import get_db
from src.app.games import service
from src.app.games.models import VideoGame
from src.app.games.schemas import VideoGameCreate, VideoGameFilters, VideoGamePatch

router = APIRouter(prefix="/video-games", tags=["video-games"])


@router.get("/", response_model=list[VideoGame])
def search_video_games(filters: VideoGameFilters = Depends(), session: Session = Depends(get_db)):
    return service.search_video_games(session, filters)


@router.post("/", response_model=VideoGame, status_code=201)
def create_video_game(payload: VideoGameCreate, session: Session = Depends(get_db)):
    return service.create_video_game(session, payload)


@router.get("/{uuid}", response_model=VideoGame)
def get_video_game(uuid: UUID, session: Session = Depends(get_db)):
    return service.get_video_game(session, uuid)


@router.patch("/{uuid}", response_model=VideoGame)
def patch_video_game(uuid: UUID, payload: VideoGamePatch, session: Session = Depends(get_db)):
    return service.patch_video_game(session, uuid, payload)


@router.delete("/{uuid}", status_code=204)
def delete_video_game(uuid: UUID, session: Session = Depends(get_db)):
    service.delete_video_game(session, uuid)
