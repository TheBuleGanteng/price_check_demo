import os
import json
import re
from typing import Optional
from openai import OpenAI
from app.models.item import ItemRequest
from app.utils.logging_config import get_logger

logger = get_logger(__name__)


class ExaPriceSearchService:
    """Service for searching item prices using Exa API via OpenAI client"""
    
    def __init__(self):
        self.api_key = os.getenv("EXA_API_KEY")
        if not self.api_key:
            raise ValueError("EXA_API_KEY environment variable is required")
        
        self.client = OpenAI(
            base_url="https://api.exa.ai",
            api_key=self.api_key,
        )
    
    def create_search_query(self, item: ItemRequest) -> str:
        """Create an optimized search query for price information"""
        # Create a search query that includes quantity for better results
        query = f"What is the average retail price for {item.item_quantity} new {item.item_name} in the Tennessee area?"        
        logger.debug(f"running create_search_query ... Created search query: '{query}'")
        return query
    
    def search_item_price(self, item: ItemRequest) -> Optional[float]:
        """
        Search for item price using Exa API and return a single price
        
        Args:
            item: ItemRequest object with item details
            
        Returns:
            Float price if found, None if not found
        """
        try:
            search_query = self.create_search_query(item)
            
            # Perform the search with Exa using OpenAI client
            logger.debug(f"running search_item_price ... Calling Exa API for: '{search_query}'")
            
            completion = self.client.chat.completions.create(
                model="exa",
                messages=[
                    {
                        "role": "system", 
                        "content": "Output should be price in US Dollars, as a float. Do not include any symbols, such as $. If multiple prices are found, return the most reasonable retail price. If no price is found, return null."
                    },
                    {
                        "role": "user", 
                        "content": search_query
                    }
                ],
                extra_body={
                    "text": True,
                    "output_schema": {
                        "type": "object",
                        "required": ["price"],
                        "additionalProperties": False,
                        "properties": {
                            "price": {
                                "type": ["number", "null"],
                                "description": "The retail price in US Dollars as a float, or null if no price found"
                            }
                        }
                    }
                }
            )
            
            logger.debug(f"running search_item_price ... Exa API call completed")
            
            # Extract the response
            response_content = completion.choices[0].message.content
            logger.debug(f"running search_item_price ... Raw response: {response_content}")
            
            # Parse the response to extract price
            price = self._parse_price_response(response_content)
            
            if price is not None:
                logger.debug(f"running search_item_price ... result #1 price: ${price:.2f}")
                logger.debug(f"running search_item_price ... Exa search: '{search_query}' -> 1 result")
                logger.debug(f"running search_item_price ... Final price selected: ${price:.2f}")
            else:
                logger.debug(f"running search_item_price ... result #1 price: No price found")
                logger.debug(f"running search_item_price ... Exa search: '{search_query}' -> 0 results")
                logger.warning(f"running search_item_price ... No price found in search results")
                
            return price
            
        except Exception as e:
            logger.error(f"running search_item_price ... Error searching for item price: {str(e)}")
            raise
    
    def _parse_price_response(self, response_content: Optional[str]) -> Optional[float]:
        """
        Parse the Exa API response to extract price
        
        Args:
            response_content: Raw response content from Exa API
            
        Returns:
            Float price if found, None if not found
        """
        if not response_content:
            return None
        
        try:
            # Try to parse as JSON first
            try:
                parsed_data = json.loads(response_content)
                if isinstance(parsed_data, dict) and "price" in parsed_data:
                    # Extract price with proper type handling
                    price_field = parsed_data["price"] # type: ignore
                    
                    # Type narrow using isinstance checks
                    if isinstance(price_field, (int, float)):
                        price = float(price_field)
                        if 0 < price < 1000000:  # Reasonable price range
                            return round(price, 2)
                        return None
                    elif price_field is None:
                        return None
                    else:
                        # Unexpected type, fall through to regex parsing
                        pass
                        
            except (json.JSONDecodeError, KeyError, ValueError, TypeError):
                pass

            
            # Fallback: try to extract number directly from response
            # Look for floating point numbers in the response
            number_patterns = [
                r'(\d+\.\d{2})',  # 19.99
                r'(\d+\.\d{1})',  # 19.9
                r'(\d+)',         # 19
            ]
            
            for pattern in number_patterns:
                matches = re.findall(pattern, response_content)
                if matches:
                    try:
                        price = float(matches[0])
                        if 0 < price < 1000000:  # Reasonable price range
                            return round(price, 2)
                    except (ValueError, TypeError):
                        continue
            
            return None
            
        except Exception as e:
            logger.error(f"running _parse_price_response ... Error parsing response: {str(e)}")
            return None


# Create a singleton instance
exa_service = ExaPriceSearchService()