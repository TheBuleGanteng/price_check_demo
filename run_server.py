#!/usr/bin/env python3
"""
Script to run the Price Check Demo API server
"""

import uvicorn
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Load environment variables
load_dotenv()

console = Console()

if __name__ == "__main__":
    # Create a fancy startup banner
    startup_text = Text()
    startup_text.append("🚀 Starting Price Check Demo API...\n\n", style="bold green")
    startup_text.append("📝 API Documentation: ", style="white")
    startup_text.append("http://localhost:8000/docs\n", style="blue underline")
    startup_text.append("🔍 Root endpoint: ", style="white")
    startup_text.append("http://localhost:8000/\n", style="blue underline")
    startup_text.append("💰 Price search: ", style="white")
    startup_text.append("http://localhost:8000/items/search-price\n", style="blue underline")
    startup_text.append("❤️  Health check: ", style="white")
    startup_text.append("http://localhost:8000/items/health\n", style="blue underline")
    
    panel = Panel(
        startup_text,
        title="[bold cyan]Price Check Demo API[/bold cyan]",
        border_style="green",
        padding=(1, 2)
    )
    
    console.print(panel)
    console.print("\n[yellow]Press Ctrl+C to stop the server[/yellow]\n")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )