import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, List
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler
from rich.console import Console
from rich.traceback import install

# Install rich traceback handler for better error display
install(show_locals=True)

# Create a console instance
console = Console()

# Define the logs directory using relative path
LOGS_DIR = Path(__file__).parent.parent.parent / "logs"


def setup_logging(log_level: str = "INFO", log_to_file: bool = True) -> logging.Logger:
    """
    Set up rich logging with timestamps, file/line numbers, and colors
    Also optionally log to file with rotation
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Whether to also log to file
        
    Returns:
        Logger instance
    """
    
    # Remove any existing handlers
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    handlers: List[logging.Handler] = []
    
    # Configure rich handler for console output
    rich_handler = RichHandler(
        console=console,
        show_time=True,
        show_level=True,
        show_path=True,
        markup=True,
        rich_tracebacks=True,
        tracebacks_show_locals=True,
        locals_max_length=10,
        locals_max_string=80,
    )
    
    # Set up the formatter with more details for rich handler
    rich_handler.setFormatter(
        logging.Formatter(
            fmt="%(message)s",
            datefmt="[%X]"
        )
    )
    handlers.append(rich_handler)
    
    log_filename: Optional[Path] = None
    
    # Add file handler if requested
    if log_to_file:
        # Create logs directory if it doesn't exist
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Create log filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d")
        log_filename = LOGS_DIR / f"app_{timestamp}.log"
        
        # Configure file handler with rotation
        file_handler = RotatingFileHandler(
            filename=str(log_filename),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        
        # Set up detailed formatter for file output
        file_formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)-20s | %(filename)-15s:%(lineno)-4d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        handlers.append(file_handler)
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(message)s",
        datefmt="[%X]",
        handlers=handlers
    )
    
    # Set specific loggers to appropriate levels
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    
    # Log the setup completion
    logger = logging.getLogger(__name__)
    if log_to_file and log_filename:
        logger.info(f"Logging setup complete - Console + File: {log_filename}")
    else:
        logger.info("Logging setup complete - Console only")
    
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance with the specified name
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name or __name__)


# Custom log functions for different levels with emojis
def log_startup(message: str) -> None:
    """Log startup messages with rocket emoji"""
    logger = get_logger("startup")
    logger.info(f"🚀 {message}")


def log_success(message: str) -> None:
    """Log success messages with check mark emoji"""
    logger = get_logger("success")
    logger.info(f"✅ {message}")


def log_warning(message: str) -> None:
    """Log warning messages with warning emoji"""
    logger = get_logger("warning")
    logger.warning(f"⚠️  {message}")


def log_error(message: str) -> None:
    """Log error messages with error emoji"""
    logger = get_logger("error")
    logger.error(f"❌ {message}")


def log_api_request(method: str, path: str, status_code: Optional[int] = None) -> None:
    """Log API requests with method and path"""
    logger = get_logger("api")
    if status_code:
        if 200 <= status_code < 300:
            emoji = "✅"
        elif 400 <= status_code < 500:
            emoji = "⚠️"
        else:
            emoji = "❌"
        logger.info(f"{emoji} {method} {path} - {status_code}")
    else:
        logger.info(f"📥 {method} {path}")


def log_exa_search(query: str, results_count: int) -> None:
    """Log Exa search operations"""
    logger = get_logger("exa")
    logger.info(f"🔍 Exa search: '{query}' -> {results_count} results")