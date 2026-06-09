import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # noqa

from src.app.exception_handlers import register_exception_handlers
from src.app.games.router import router as games_router


# Basic logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI()
app.include_router(games_router)
register_exception_handlers(app)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Adjust as needed
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.get("/")
def root() -> str:
    logging.info("Health check endpoint called.")
    return "ok"
