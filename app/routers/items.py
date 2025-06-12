from fastapi import APIRouter, HTTPException
from app.models.item import ItemRequest, ItemPriceResponse
from app.services.exa_service import exa_service
from app.utils.logging_config import get_logger, log_api_request, log_success, log_error

logger = get_logger(__name__)

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.post("/search-price", response_model=ItemPriceResponse)
async def search_item_price(item: ItemRequest):
    """
    Search for item prices using Exa API
    
    - **item_name**: Name of the item to search for
    - **item_quantity**: Quantity of the item (must be positive)
    - **item_price**: Current/expected price of the item (must be positive)
    """
    log_api_request("POST", "/items/search-price")
    
    try:
        logger.info(f"🔍 Received request to search prices for: [bold cyan]{item.item_name}[/bold cyan]")
        logger.info(f"📊 Request details: quantity={item.item_quantity}, expected_price=${item.item_price}")
        
        # Create search query
        search_query = exa_service.create_search_query(item)
        
        # Search for prices
        price_results = exa_service.search_item_prices(item)
        
        # Create response
        response = ItemPriceResponse(
            original_item=item,
            search_query=search_query,
            found_prices=price_results,
            total_results=len(price_results),
            search_successful=True,
            error_message=None
        )
        
        log_success(f"Found {len(price_results)} price results for {item.item_name}")
        log_api_request("POST", "/items/search-price", 200)
        return response
        
    except Exception as e:
        log_error(f"Error processing price search request: {str(e)}")
        
        # Return error response
        error_response = ItemPriceResponse(
            original_item=item,
            search_query="",
            found_prices=[],
            total_results=0,
            search_successful=False,
            error_message=str(e)
        )
        
        log_api_request("POST", "/items/search-price", 500)
        raise HTTPException(status_code=500, detail=error_response.model_dump())


@router.get("/health")
async def health_check():
    """Simple health check endpoint"""
    log_api_request("GET", "/items/health", 200)
    return {"status": "healthy", "service": "price-check-demo"}