import os
from typing import List
from exa_py import Exa
from app.models.item import ItemRequest, PriceResult
from app.utils.logging_config import get_logger, log_exa_search, log_error

logger = get_logger(__name__)


class ExaPriceSearchService:
    """Service for searching item prices using Exa API"""
    
    def __init__(self):
        self.api_key = os.getenv("EXA_API_KEY")
        if not self.api_key:
            raise ValueError("EXA_API_KEY environment variable is required")
        
        self.client = Exa(api_key=self.api_key)
    
    def create_search_query(self, item: ItemRequest) -> str:
        """Create an optimized search query for price information"""
        # Create a search query focused on finding current prices
        query = f"{item.item_name} price buy purchase cost"
        logger.info(f"🔧 Created search query: [bold yellow]'{query}'[/bold yellow]")
        return query
    
    def search_item_prices(self, item: ItemRequest, num_results: int = 5) -> List[PriceResult]:
        """
        Search for item prices using Exa API
        
        Args:
            item: ItemRequest object with item details
            num_results: Number of search results to return
            
        Returns:
            List of PriceResult objects
        """
        try:
            search_query = self.create_search_query(item)
            
            # Perform the search with Exa
            logger.info(f"🌐 Calling Exa API for: [bold green]'{search_query}'[/bold green]")
            
            response = self.client.search_and_contents(
                query=search_query,
                num_results=num_results,
                text=True,
                highlights=True,
                type="auto"  # Let Exa decide the best search type
            )
            
            logger.info(f"📡 Exa API returned {len(response.results)} results")
            
            price_results: List[PriceResult] = []
            
            for i, result in enumerate(response.results, 1):
                logger.info(f"🔍 Processing result {i}: [blue]{result.title}[/blue]")
                
                # Extract price-related information from the content
                price_info = self._extract_price_info(result.text or "")
                
                price_result = PriceResult(
                    source_title=result.title or "No title",
                    source_url=result.url,
                    price_info=price_info,
                    snippet=result.highlights[0] if result.highlights else result.text[:200] + "..." if result.text else "No content available"
                )
                price_results.append(price_result)
                
                logger.info(f"💰 Extracted price info: [cyan]{price_info}[/cyan]")
            
            log_exa_search(search_query, len(price_results))
            return price_results
            
        except Exception as e:
            log_error(f"Error searching for item prices: {str(e)}")
            raise
    
    def _extract_price_info(self, text: str) -> str:
        """
        Extract price-related information from text content
        
        Args:
            text: Text content to search for prices
            
        Returns:
            String containing price information or indication if none found
        """
        import re
        
        if not text:
            return "No price information available"
        
        # Look for various price patterns
        price_patterns = [
            r'\$\d+(?:\.\d{2})?',  # $19.99, $100
            r'\d+\.\d{2}\s*(?:USD|dollars?)',  # 19.99 USD, 100 dollars
            r'(?:price|cost|costs?):?\s*\$?\d+(?:\.\d{2})?',  # price: $19.99, cost 100
            r'\d+\s*(?:dollars?|USD|\$)',  # 100 dollars, 50 USD
        ]
        
        found_prices: List[str] = []
        for pattern in price_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            found_prices.extend(matches)
        
        if found_prices:
            # Return first few unique prices found
            unique_prices = list(set(found_prices))[:3]
            return f"Found prices: {', '.join(unique_prices)}"
        
        # If no explicit prices found, look for price-related context
        price_keywords = ['price', 'cost', 'buy', 'purchase', 'sale', 'discount', 'deal']
        text_lower = text.lower()
        
        for keyword in price_keywords:
            if keyword in text_lower:
                # Extract sentence containing the keyword
                sentences = text.split('.')
                for sentence in sentences:
                    if keyword in sentence.lower():
                        return f"Price context: {sentence.strip()[:150]}..."
        
        return "No specific price information found"


# Create a singleton instance
exa_service = ExaPriceSearchService()