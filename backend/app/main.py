import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import password, social, learning, awareness, stats
from app.core.config import settings

# Configure Centralized Logging
logging.basicConfig(
    level=logging.getLevelName(settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name, version="1.0.0", description="Cybersecurity Training Platform API")

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected internal server error occurred. Please contact the administrator."},
    )

# Configure CORS
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:5176",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(password.router, prefix="/api/password", tags=["password"])
app.include_router(social.router, prefix="/api/social", tags=["social"])
app.include_router(learning.router, prefix="/api/learning", tags=["learning"])
app.include_router(awareness.router, prefix="/api/awareness", tags=["awareness"])
app.include_router(stats.router, prefix="/api/stats", tags=["stats"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Cybersecurity Training Platform API"}
