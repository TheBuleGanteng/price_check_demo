# 💰 Price Check Demo API

A FastAPI-based demo application that searches for item prices using the Exa API. This project demonstrates modern Python web development with rich logging, structured data validation, and external API integration.

## ✨ Features

- 🚀 **FastAPI** - Modern, fast web framework for building APIs
- 🔍 **Exa API Integration** - Intelligent web search for price information
- 📊 **Pydantic Models** - Data validation and serialization
- 🌈 **Rich Logging** - Beautiful console logs with timestamps and file locations
- 🏗️ **Structured Architecture** - Clean separation of concerns with routers and services
- 📝 **Auto-generated Documentation** - Interactive API docs with Swagger UI
- ⚡ **Auto-reload** - Development server with hot reloading

## 🛠️ Technology Stack

- **Python 3.12+**
- **FastAPI** - Web framework
- **Exa** - AI-powered search API
- **Pydantic** - Data validation
- **Rich** - Beautiful terminal output
- **Uvicorn** - ASGI server

## 📁 Project Structure

```
price_check_demo/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── item.py          # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   └── exa_service.py   # Exa API integration
│   ├── routers/
│   │   ├── __init__.py
│   │   └── items.py         # API endpoints
│   └── utils/
│       ├── __init__.py
│       └── logging_config.py # Rich logging setup
├── .env                     # Environment variables
├── .gitignore
├── requirements.txt
├── run_server.py           # Server startup script
├── test_api.py            # API testing script
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Exa API key ([Get one here](https://exa.ai/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/price-check-demo.git
   cd price-check-demo
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your Exa API key
   ```

5. **Run the server**
   ```bash
   python run_server.py
   ```

The API will be available at `http://localhost:8000`

## 📖 API Documentation

Once the server is running, visit:

- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/items/health

## 🔧 API Endpoints

### POST `/items/search-price`

Search for item prices using Exa API.

**Request Body:**
```json
{
  "item_name": "iPhone 15",
  "item_quantity": 1,
  "item_price": 999.99
}
```

**Response:**
```json
{
  "original_item": {
    "item_name": "iPhone 15",
    "item_quantity": 1,
    "item_price": 999.99
  },
  "search_query": "iPhone 15 price buy purchase cost",
  "found_prices": [
    {
      "source_title": "Apple Store - iPhone 15",
      "source_url": "https://apple.com/iphone-15",
      "price_info": "Found prices: $999.00, $1099.00",
      "snippet": "The new iPhone 15 starts at $999..."
    }
  ],
  "total_results": 1,
  "search_successful": true,
  "error_message": null
}
```

### GET `/items/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "price-check-demo"
}
```

## 🧪 Testing

Run the test script to verify the API is working:

```bash
python test_api.py
```

## 🌱 Development

### Environment Variables

Create a `.env` file with:

```env
EXA_API_KEY=your_exa_api_key_here
LOG_LEVEL=INFO
```

### Running in Development Mode

```bash
python run_server.py
```

The server will automatically reload when you make changes to the code.

### Code Structure

- **Models** (`app/models/`): Pydantic models for data validation
- **Services** (`app/services/`): Business logic and external API integrations
- **Routers** (`app/routers/`): API endpoint definitions
- **Utils** (`app/utils/`): Shared utilities like logging configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [Exa](https://exa.ai/) for the powerful search API
- [Rich](https://github.com/Textualize/rich) for beautiful terminal output

## 📞 Support

If you have any questions or issues, please open an issue on GitHub.

---

Made with ❤️ and ☕