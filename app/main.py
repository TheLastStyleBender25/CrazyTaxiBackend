from fastapi import FastAPI
from app.core.logger import logger
from app.db.session import Base, engine
from app.models import User, Player, RefreshToken, AvailableTaxi, OwnedTaxi, Transaction, RideMilestone, PlayerClaimedMilestone, CityLevel
from app.routes.auth_route import router as auth_router
from app.routes.garage_route import router as garage_router
from app.routes.milestone_route import router as milestone_router
from app.routes.ws_route import router as web_router
from app.routes.city_route import router as city_router
from app.services.ride_refresh_service import ride_refresh_loop
from contextlib import asynccontextmanager
import asyncio
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.extension import _rate_limit_exceeded_handler
from app.core.limiter import limiter
from app.core.exception_handler import global_exception_handler

@asynccontextmanager
async  def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    logger.info(f"life span has started")
    asyncio.create_task(ride_refresh_loop())
    yield
    logger.info(f"life span has finished")

logger.info(f"adding limiter")
app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
logger.info(f"adding rate limiter exception handling")
app.include_router(auth_router)
app.add_middleware(SlowAPIMiddleware)
logger.info(f"adding global exception handling")
app.add_exception_handler(Exception, global_exception_handler)
logger.info(f"adding routes")
app.include_router(auth_router)
app.include_router(garage_router)
app.include_router(web_router)
app.include_router(milestone_router)
app.include_router(city_router)
logger.info(f"routes added")

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
