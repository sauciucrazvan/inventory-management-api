<p align="center">
    <img src="https://i.imgur.com/sbP28Bb.png" width="312" height="160">
    <br />
    <b>Inventory Management API</b>
</p>

The API includes endpoints that will help keep track of products, stock levels, warehouses, suppliers and inventory movements (e.g., stock-in, stock-out, transfers).

**Feel free to use it for testing purposes, modify the code in any way or shape you want without credits.**

## Table of contents

- [API Overview](#api-overview)
- [Database](#database)
- [Tech Stack](#tech-stack)
- [Setup](#setup)
- [Documentation](#documentation)
- [Project Structure](#project-structure)
- [Notes](#notes)

## API Overview

### Core Endpoints

- **Warehouses**: Full CRUD operations for warehouse management
- **Suppliers**: Complete supplier information management
- **Products**: Product catalog management within warehouses
- **Inventory**: Real-time stock tracking and operations

### Rate Limits

- Read operations: 150 requests per minute
- Write operations: 20 requests per minute
- Stock operations: 30 requests per minute

Rate limiting is applied per IP address.

## Database

The project uses SQLite for simplicity with the following main entities:

- **Warehouse**: Storage locations with capacity tracking
- **Supplier**: Vendor information and contact details
- **Product**: Item catalog with pricing and supplier links
- **Stock**: Inventory levels with warehouse associations

All entities use UUID primary keys for better scalability.

## Tech Stack

- FastAPI
- SQLAlchemy with SQLite database
- Pydantic for data validation
- Alembic for database migrations
- Slowapi for rate limiting
- Uvicorn ASGI server

## Setup

### Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

### Installation

1. Clone the repository
2. Create and activate virtual environment
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run database migrations:
   ```
   python migrate.py
   ```
5. Start the server:
   ```
   python main.py
   ```

The API will be available at `http://127.0.0.1:8000`

## Documentation

- Interactive API documentation: `http://127.0.0.1:8000/docs`
- API endpoint details: See [`endpoints.md`](endpoints.md)
- Postman Example HTTP Requests: Download [`Inventory-Management-API.postman_collection.json`](Inventory-Management-API.postman_collection.json)

## Project Structure

```
├── main.py                # Application entry point
├── api/
│   ├── app.py             # FastAPI application setup
│   ├── rate_limiter.py    # Rate limiting configuration
│   └── routes/            # API route handlers
├── models/                # Database models
├── db/                    # Database session management
├── alembic/               # Database migration files
└── migrate.py             # Migration management script
```

## Notes

This is a learning project focused on:

- FastAPI framework fundamentals
- Database design with SQLAlchemy
- API rate limiting implementation
- RESTful API design patterns
