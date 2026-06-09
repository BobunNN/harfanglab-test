from fastapi import HTTPException


class GameNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Game not found")


class GameTooSimilarException(HTTPException):
    def __init__(self, similar_name: str):
        super().__init__(status_code=409, detail=f"A game with a similar name already exists: '{similar_name}'")
