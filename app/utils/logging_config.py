import logging
from typing import Optional
from rich.logging import RichHandler
from rich.console import Console
from rich.traceback import install

# Install rich traceback handler for better error display
install(show_locals=True)

# Create a console instance
console = Console()


def setup_logging(log_level: str = "INFO"):
    """
    Set up rich logging with timestamps, file/line numbers, and colors
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    
    # Remove any existing handlers
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    # Configure rich handler
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
    
    # Set up the formatter with more details
    rich_handler.setFormatter(
        logging.Formatter(
            fmt="%(message)s",
            datefmt="[%X]"
        )
    )
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[rich_handler]
    )
    
    # Set specific loggers to appropriate levels
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)


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
def log_startup(message: str):
    """Log startup messages with rocket emoji"""
    logger = get_logger("startup")
    logger.info(f"🚀 {message}")


def log_success(message: str):
    """Log success messages with check mark emoji"""
    logger = get_logger("success")
    logger.info(f"✅ {message}")


def log_warning(message: str):
    """Log warning messages with warning emoji"""
    logger = get_logger("warning")
    logger.warning(f"⚠️  {message}")


def log_error(message: str):
    """Log error messages with error emoji"""
    logger = get_logger("error")
    logger.error(f"❌ {message}")


def log_api_request(method: str, path: str, status_code: Optional[int] = None):
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


def log_exa_search(query: str, results_count: int):
    """Log Exa search operations"""
    logger = get_logger("exa")
    logger.info(f"🔍 Exa search: '{query}' -> {results_count} results")