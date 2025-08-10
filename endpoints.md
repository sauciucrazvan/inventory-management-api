# API Endpoints Documentation

## Overview

This API provides inventory management functionality across multiple warehouses. All endpoints require proper HTTP methods and return JSON responses.

Base URL: `http://127.0.0.1:8000/api`

## Rate Limiting

- Read operations: 150 requests per minute
- Write operations: 20 requests per minute
- Stock operations: 30 requests per minute

## Warehouses

### Create Warehouse

**POST** `/warehouses`

Creates a new warehouse.

**Request Body:**

```json
{
  "name": "string",
  "location": "string"
}
```

**Response:**

```json
{
  "id": "uuid",
  "message": "Warehouse created successfully"
}
```

### Get All Warehouses

**GET** `/warehouses`

Returns list of all warehouses.

**Response:**

```json
[
  {
    "id": "uuid",
    "name": "string",
    "location": "string"
  }
]
```

### Get Warehouse by ID

**GET** `/warehouses/{warehouse_id}`

Returns specific warehouse details.

**Response:**

```json
{
  "id": "uuid",
  "name": "string",
  "location": "string"
}
```

### Update Warehouse (Partial)

**PATCH** `/warehouses/{warehouse_id}`

Updates specific warehouse fields.

**Request Body:**

```json
{
  "name": "string (optional)",
  "location": "string (optional)"
}
```

**Response:**

```json
{
  "message": "Warehouse updated successfully"
}
```

### Update Warehouse (Complete)

**PUT** `/warehouses/{warehouse_id}`

Replaces warehouse with new data.

**Request Body:**

```json
{
  "name": "string",
  "location": "string"
}
```

**Response:**

```json
{
  "message": "Warehouse updated successfully"
}
```

## Suppliers

### Create Supplier

**POST** `/suppliers`

Creates a new supplier.

**Request Body:**

```json
{
  "name": "string",
  "contact_email": "email@example.com"
}
```

**Response:**

```json
{
  "id": "uuid",
  "message": "Supplier created successfully"
}
```

### Get All Suppliers

**GET** `/suppliers`

Returns list of all suppliers.

**Response:**

```json
[
  {
    "id": "uuid",
    "name": "string",
    "contact_email": "email@example.com"
  }
]
```

### Get Supplier by ID

**GET** `/suppliers/{supplier_id}`

Returns specific supplier details.

**Response:**

```json
{
  "id": "uuid",
  "name": "string",
  "contact_email": "email@example.com"
}
```

### Update Supplier (Partial)

**PATCH** `/suppliers/{supplier_id}`

Updates specific supplier fields.

**Request Body:**

```json
{
  "name": "string (optional)",
  "contact_email": "email@example.com (optional)"
}
```

**Response:**

```json
{
  "message": "Supplier updated successfully"
}
```

### Update Supplier (Complete)

**PUT** `/suppliers/{supplier_id}`

Replaces supplier with new data.

**Request Body:**

```json
{
  "name": "string",
  "contact_email": "email@example.com"
}
```

**Response:**

```json
{
  "message": "Supplier updated successfully"
}
```

## Product Management

### Create Product in Warehouse

**POST** `/warehouses/{warehouse_id}/products`

Adds a new product to specific warehouse.

**Request Body:**

```json
{
  "name": "string",
  "description": "string",
  "sku": "string",
  "price": 99.99,
  "supplier_id": "uuid"
}
```

**Response:**

```json
{
  "id": "uuid",
  "message": "Product created successfully"
}
```

### Get Products in Warehouse

**GET** `/warehouses/{warehouse_id}/products`

Returns all products in specific warehouse.

**Response:**

```json
[
  {
    "id": "uuid",
    "name": "string",
    "description": "string",
    "sku": "string",
    "price": 99.99,
    "supplier_id": "uuid"
  }
]
```

### Get Product Details

**GET** `/warehouses/{warehouse_id}/products/{product_id}`

Returns specific product details including stock.

**Response:**

```json
{
  "id": "uuid",
  "name": "string",
  "description": "string",
  "sku": "string",
  "price": 99.99,
  "supplier_id": "uuid",
  "stock_quantity": 100
}
```

### Update Product (Partial)

**PATCH** `/warehouses/{warehouse_id}/products/{product_id}`

Updates specific product fields. Note: stock_quantity cannot be updated here.

**Request Body:**

```json
{
  "name": "string (optional)",
  "description": "string (optional)",
  "price": 99.99
}
```

**Response:**

```json
{
  "message": "Product updated successfully"
}
```

### Update Product (Complete)

**PUT** `/warehouses/{warehouse_id}/products/{product_id}`

Replaces product with new data. Note: stock_quantity cannot be updated here.

**Request Body:**

```json
{
  "name": "string",
  "description": "string",
  "sku": "string",
  "price": 99.99,
  "supplier_id": "uuid"
}
```

**Response:**

```json
{
  "message": "Product updated successfully"
}
```

### Delete Product

**DELETE** `/warehouses/{warehouse_id}/products/{product_id}`

Removes product from warehouse.

**Response:**

```json
{
  "message": "Product deleted successfully"
}
```

## Stock Management

### Get Warehouse Inventory

**GET** `/warehouses/{warehouse_id}/inventory`

Returns all stock in specific warehouse.

**Response:**

```json
[
  {
    "product_id": "uuid",
    "product_name": "string",
    "sku": "string",
    "quantity": 100,
    "warehouse_id": "uuid"
  }
]
```

### Get Product Stock

**GET** `/warehouses/{warehouse_id}/inventory/{product_id}`

Returns stock information for specific product in warehouse.

**Response:**

```json
{
  "product_id": "uuid",
  "product_name": "string",
  "sku": "string",
  "quantity": 100,
  "warehouse_id": "uuid"
}
```

### Increase Stock

**POST** `/warehouses/{warehouse_id}/inventory/{product_id}/increase`

Increases stock quantity for product.

**Request Body:**

```json
{
  "quantity": 50,
  "reason": "string (optional)"
}
```

**Response:**

```json
{
  "message": "Stock increased successfully",
  "new_quantity": 150
}
```

### Decrease Stock

**POST** `/warehouses/{warehouse_id}/inventory/{product_id}/decrease`

Decreases stock quantity for product.

**Request Body:**

```json
{
  "quantity": 25,
  "reason": "string (optional)"
}
```

**Response:**

```json
{
  "message": "Stock decreased successfully",
  "new_quantity": 125
}
```

### Transfer Stock

**POST** `/warehouses/{warehouse_id}/inventory/{product_id}/transfer`

Transfers stock between warehouses.

**Request Body:**

```json
{
  "target_warehouse_id": "uuid",
  "quantity": 30,
  "reason": "string (optional)"
}
```

**Response:**

```json
{
  "message": "Stock transferred successfully",
  "new_stock_quantity": 30
}
```

## Error Responses

All endpoints may return the following error responses:

**400 Bad Request**

```json
{
  "detail": "Error description"
}
```

**404 Not Found**

```json
{
  "detail": "Resource not found"
}
```

**422 Validation Error**

```json
{
  "detail": [
    {
      "loc": ["field_name"],
      "msg": "Error message",
      "type": "error_type"
    }
  ]
}
```

**429 Too Many Requests**

```json
{
  "detail": "Rate limit exceeded"
}
```

## Notes

- All UUIDs must be valid UUID format
- Stock quantity changes are tracked through dedicated stock management endpoints
- Products cannot have negative stock quantities
- Rate limiting is applied per IP address
- All timestamps are in UTC format
- Price values should be positive numbers with up to 2 decimal places
