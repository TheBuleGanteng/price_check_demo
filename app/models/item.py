from pydantic import BaseModel, Field
from typing import Optional, List


class ItemRequest(BaseModel):
    """Model for incoming item data"""
    item_name: str = Field(..., description="Name of the item to search for")
    item_quantity: int = Field(..., gt=0, description="Quantity of the item")
    item_price: float = Field(..., gt=0, description="Current/expected price of the item")


class PriceResult(BaseModel):
    """Model for price search results"""
    source_title: str = Field(..., description="Title of the source")
    source_url: str = Field(..., description="URL of the source")
    price_info: str = Field(..., description="Price information found")
    snippet: str = Field(..., description="Relevant snippet from the source")


class ItemPriceResponse(BaseModel):
    """Model for API response"""
    original_item: ItemRequest = Field(..., description="Original item data")
    search_query: str = Field(..., description="Search query used")
    found_prices: List[PriceResult] = Field(default=[], description="List of price results found")
    total_results: int = Field(..., description="Total number of results found")
    search_successful: bool = Field(..., description="Whether the search was successful")
    error_message: Optional[str] = Field(None, description="Error message if search failed")