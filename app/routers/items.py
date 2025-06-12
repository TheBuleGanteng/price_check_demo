from fastapi import APIRouter, HTTPException
from app.models.item import ItemRequest, ItemResponse
from app.services.exa_service import exa_service
from app.utils.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.post("/search-price", response_model=ItemResponse)
async def search_item_price(item: ItemRequest):
    """
    Search for item price using Exa API
    
    - **item_name**: Name of the item to search for
    - **item_quantity**: Quantity of the item (must be positive)
    - **item_price**: Will be populated by the system (should be null in request)
    """
    logger.info(f"running search_item_price ... POST /items/search-price")
    
    try:
        logger.info(f"running search_item_price ... Received request to search price for: [bold cyan]{item.item_name}[/bold cyan]")
        logger.info(f"running search_item_price ... Request details: quantity={item.item_quantity}")
        
        # Search for the price using Exa
        found_price = exa_service.search_item_price(item)
        
        # Create response with the same structure but populated price
        response = ItemResponse(
            item_name=item.item_name,
            item_quantity=item.item_quantity,
            item_price=found_price
        )
        
        if found_price:
            logger.info(f"running search_item_price ... Found price ${found_price} for {item.item_name}")
        else:
            logger.warning(f"running search_item_price ... No price found for {item.item_name}")
            
        logger.info(f"running search_item_price ... POST /items/search-price - 200")
        return response
        
    except Exception as e:
        logger.error(f"running search_item_price ... Error processing price search request: {str(e)}")
        logger.error(f"running search_item_price ... POST /items/search-price - 500")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Simple health check endpoint"""
    logger.info(f"running health_check ... GET /items/health - 200")
    return {"status": "healthy", "service": "price-check-demo"}