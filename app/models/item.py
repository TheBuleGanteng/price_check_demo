from pydantic import BaseModel, Field
from typing import Optional


class ItemRequest(BaseModel):
    """Model for incoming item data"""
    item_name: str = Field(..., description="Name of the item to search for")
    item_quantity: int = Field(..., gt=0, description="Quantity of the item")
    item_price: Optional[float] = Field(None, description="Price of the item (populated by LLM)")


class ItemResponse(BaseModel):
    """Model for API response - same structure as request but with populated price"""
    item_name: str = Field(..., description="Name of the item")
    item_quantity: int = Field(..., description="Quantity of the item") 
    item_price: Optional[float] = Field(None, description="Price found by the system")