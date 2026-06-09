from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.app.games.exceptions import GameNotFoundException, GameTooSimilarException


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(GameNotFoundException)
    def game_not_found_handler(request: Request, exc: GameNotFoundException) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(GameTooSimilarException)
    def game_too_similar_handler(request: Request, exc: GameTooSimilarException) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
