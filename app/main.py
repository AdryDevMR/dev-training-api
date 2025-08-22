from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.config import settings
from app.database import init_db
from app.api import users_router, tasks_router
from app.utils.logging import get_logger
from app.utils.responses import APIResponse

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting up User Account and Tasks API...")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down User Account and Tasks API...")


# Create FastAPI application
app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=settings.description,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["POST"],  # Only POST methods allowed
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler that ensures only 200/500 status codes."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return APIResponse.server_error("An unexpected error occurred")


# Include API routers
app.include_router(
    users_router,
    prefix=f"{settings.api_prefix}/users",
    tags=["users"]
)

app.include_router(
    tasks_router,
    prefix=f"{settings.api_prefix}/tasks",
    tags=["tasks"]
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "User Account and Tasks API",
        "version": settings.version,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.log_level.lower()
    )
