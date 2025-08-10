from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi import Request, FastAPI

limiter = Limiter(key_func=get_remote_address)

def setup_rate_limiting(app: FastAPI) -> None:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) # type: ignore
    app.add_middleware(SlowAPIMiddleware)

def rate_limit_strict():
    return limiter.limit("5/minute")

def rate_limit_moderate():
    return limiter.limit("30/minute")

def rate_limit_relaxed():
    return limiter.limit("100/minute")

class RateLimitConfig:
    GENERAL = "100/minute"
    CRUD = "50/minute"
    STOCK = "30/minute"
    BULK = "10/minute"
    READ = "150/minute"
    WRITE = "20/minute"
