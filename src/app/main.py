import logging
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware  # noqa

from src.app.exception_handlers import register_exception_handlers
from src.app.games.router import router as games_router


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(games_router)
register_exception_handlers(app)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info("%s %s %d %.1fms", request.method, request.url.path, response.status_code, duration_ms)
    return response

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
