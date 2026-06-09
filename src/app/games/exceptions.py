from fastapi import HTTPException


class GameNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Game not found")
