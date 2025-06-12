from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import items
from dotenv import load_dotenv
import logging
from contextlib import asynccontextmanager

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Price Check Demo API is starting up...")
    yield
    # Shutdown
    logger.info("Price Check Demo API is shutting down...")


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