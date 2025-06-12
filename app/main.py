from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import items
from app.utils.logging_config import setup_logging, get_logger
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import os

# Load environment variables
load_dotenv()

# Set up rich logging
setup_logging(log_level=os.getenv("LOG_LEVEL", "DEBUG"))
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("running lifespan ... Price Check Demo API is starting up...")
    logger.info("running lifespan ... Setting up middleware and routes...")
    yield
    # Shutdown
    logger.info("running lifespan ... Price Check Demo API is shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Price Check Demo API",
    description="A demo API that searches for item prices using Exa",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(items.router)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Price Check Demo API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/items/health"
    }





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)