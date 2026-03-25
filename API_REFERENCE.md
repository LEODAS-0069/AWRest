# API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently: None (can add JWT)
Future: Bearer token in Authorization header

## Response Format

All responses are JSON with standard format:

```json
{
  "success": true,
  "data": {},
  "error": null
}
```

---

## Products Endpoints

### List Products

**Endpoint**: `GET /products`

**Query Parameters**:
- `skip` (integer, default: 0) - Number of products to skip
- `limit` (integer, default: 20) - Number of products to return

**Request**:
```bash
curl -X GET "http://localhost:5000/api/products?skip=0&limit=20"
```

**Response** (200 OK):
```json
{
  "success": true,
  "count": 3,
  "products": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "product_id": "LABUBU-001",
      "name": "Labubu Hot Spring Ver.",
      "character_name": "Labubu",
      "price": 150.00,
      "condition": "Mint",
      "description": "Rare hot spring edition...",
      "seller_id": "seller-123",
      "status": "active",
      "created_at": "2024-03-20T10:30:00Z",
      "quantity": 1
    }
  ]
}
```

---

### Get Product by ID

**Endpoint**: `GET /products/{id}`

**Path Parameters**:
- `id` (string, required) - MongoDB ObjectId

**Request**:
```bash
curl -X GET "http://localhost:5000/api/products/507f1f77bcf86cd799439011"
```

**Response** (200 OK):
```json
{
  "success": true,
  "product": {
    "_id": "507f1f77bcf86cd799439011",
    "name": "Labubu Hot Spring Ver.",
    "price": 150.00,
    "condition": "Mint",
    "description": "Rare hot spring edition...",
    "character_name": "Labubu",
    "seller_id": "seller-123",
    "status": "active"
  }
}
```

**Response** (404 Not Found):
```json
{
  "success": false,
  "error": "Product not found"
}
```

---

### Search Products

**Endpoint**: `POST /products/search`

**Content-Type**: `application/json`

**Request Body**:
```json
{
  "query": "labubu basquiat",
  "skip": 0,
  "limit": 20
}
```

**Request**:
```bash
curl -X POST "http://localhost:5000/api/products/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "hot spring",
    "skip": 0,
    "limit": 10
  }'
```

**Response** (200 OK):
```json
{
  "success": true,
  "count": 2,
  "query": "hot spring",
  "products": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "name": "Labubu Hot Spring Ver.",
      "price": 150.00,
      "character_name": "Labubu",
      "condition": "Mint",
      "description": "Rare hot spring edition with pristine packaging"
    }
  ]
}
```

---

### Create Product

**Endpoint**: `POST /products`

**Content-Type**: `application/json`

**Request Body**:
```json
{
  "name": "Labubu Kabuki Ver.",
  "character_name": "Labubu",
  "price": 200.00,
  "condition": "Mint",
  "description": "Japanese traditional Kabuki design limited edition",
  "seller_id": "seller-456",
  "image_url": "https://example.com/image.jpg",
  "quantity": 1
}
```

**Required Fields**:
- name (string)
- character_name (string)
- price (number)
- seller_id (string)

**Request**:
```bash
curl -X POST "http://localhost:5000/api/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Labubu Kabuki Ver.",
    "character_name": "Labubu",
    "price": 200.00,
    "condition": "Mint",
    "description": "Japanese traditional Kabuki design",
    "seller_id": "seller-456"
  }'
```

**Response** (201 Created):
```json
{
  "success": true,
  "product_id": "507f1f77bcf86cd799439012",
  "message": "Product created successfully"
}
```

**Response** (400 Bad Request):
```json
{
  "success": false,
  "error": "Missing field: price"
}
```

---

### Update Product

**Endpoint**: `PUT /products/{id}`

**Content-Type**: `application/json`

**Path Parameters**:
- `id` (string, required) - MongoDB ObjectId

**Request Body** (any fields to update):
```json
{
  "price": 175.00,
  "condition": "Like New",
  "status": "sold"
}
```

**Request**:
```bash
curl -X PUT "http://localhost:5000/api/products/507f1f77bcf86cd799439011" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 175.00,
    "status": "sold"
  }'
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Product updated successfully"
}
```

---

### Delete Product

**Endpoint**: `DELETE /products/{id}`

**Path Parameters**:
- `id` (string, required) - MongoDB ObjectId

**Request**:
```bash
curl -X DELETE "http://localhost:5000/api/products/507f1f77bcf86cd799439011"
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Product deleted successfully"
}
```

---

## Orders Endpoints

### Create Order

**Endpoint**: `POST /orders`

**Content-Type**: `application/json`

**Request Body**:
```json
{
  "user_id": "user-123",
  "product_id": "LABUBU-001",
  "quantity": 1,
  "total_price": 150.00,
  "shipping_address": "123 Main St, City, State 12345"
}
```

**Request**:
```bash
curl -X POST "http://localhost:5000/api/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-123",
    "product_id": "LABUBU-001",
    "quantity": 1,
    "total_price": 150.00,
    "shipping_address": "123 Main St, City, State 12345"
  }'
```

**Response** (201 Created):
```json
{
  "success": true,
  "order_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Order created successfully"
}
```

**Response** (400 Bad Request):
```json
{
  "success": false,
  "error": "Tornado service error: [Connection error]"
}
```

---

### Get Order Details

**Endpoint**: `GET /orders/{id}`

**Path Parameters**:
- `id` (string, required) - Order UUID

**Request**:
```bash
curl -X GET "http://localhost:5000/api/orders/550e8400-e29b-41d4-a716-446655440000"
```

**Response** (200 OK):
```json
{
  "success": true,
  "order": {
    "order_id": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": 1711000000,
    "user_id": "user-123",
    "product_id": "LABUBU-001",
    "quantity": 1,
    "total_price": 150.0,
    "status": "pending",
    "shipping_address": "123 Main St, City, State 12345",
    "created_at": "2024-03-20T12:00:00Z"
  }
}
```

---

### Update Order Status

**Endpoint**: `PATCH /orders/{id}`

**Content-Type**: `application/json`

**Path Parameters**:
- `id` (string, required) - Order UUID

**Request Body**:
```json
{
  "status": "processing"
}
```

**Allowed Statuses**:
- `pending` - Order created, awaiting payment
- `processing` - Payment confirmed, preparing shipment
- `shipped` - Order shipped
- `delivered` - Order delivered
- `cancelled` - Order cancelled
- `failed` - Payment failed

**Request**:
```bash
curl -X PATCH "http://localhost:5000/api/orders/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "processing"
  }'
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Order updated successfully"
}
```

---

## System Endpoints

### Health Check

**Endpoint**: `GET /health`

**Request**:
```bash
curl -X GET "http://localhost:5000/health"
```

**Response** (200 OK):
```json
{
  "status": "healthy",
  "service": "flask-api-gateway",
  "timestamp": "2024-03-20T12:30:00Z"
}
```

---

### System Status

**Endpoint**: `GET /api/status`

**Request**:
```bash
curl -X GET "http://localhost:5000/api/status"
```

**Response** (200 OK):
```json
{
  "flask_gateway": "healthy",
  "mongodb": "healthy",
  "tornado_service": "healthy",
  "timestamp": "2024-03-20T12:30:00Z"
}
```

**Response** (503 Service Unavailable) - if services are down:
```json
{
  "flask_gateway": "healthy",
  "mongodb": "unhealthy",
  "tornado_service": "unreachable",
  "timestamp": "2024-03-20T12:30:00Z"
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Product retrieved successfully |
| 201 | Created | Product/Order created |
| 400 | Bad Request | Missing required field |
| 404 | Not Found | Product doesn't exist |
| 500 | Server Error | Database connection error |
| 503 | Service Unavailable | Tornado service down |

### Error Response Format

```json
{
  "success": false,
  "error": "Error description"
}
```

---

## Pagination

For list endpoints supporting pagination:

**Query Parameters**:
- `skip` (default: 0) - Products to skip
- `limit` (default: 20, max: 100) - Products to return

**Example**:
```bash
# Get products 20-40
curl "http://localhost:5000/api/products?skip=20&limit=20"

# Get products 40-60
curl "http://localhost:5000/api/products?skip=40&limit=20"
```

---

## Rate Limiting

Current implementation: No rate limiting (can be added)

Recommended limits:
- 100 requests per minute per IP for public endpoints
- 1000 requests per minute for authenticated users
- 10 concurrent orders endpoint requests

---

## Testing

### Local Testing

```bash
# Start application
docker-compose up -d

# Test health
curl http://localhost:5000/health

# Test products list
curl http://localhost:5000/api/products

# Test search
curl -X POST http://localhost:5000/api/products/search \
  -H "Content-Type: application/json" \
  -d '{"query":"labubu"}'

# Test create product
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Test Labubu",
    "character_name":"Labubu",
    "price":100,
    "condition":"Mint",
    "seller_id":"test-seller"
  }'

# Test create order
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id":"test-user",
    "product_id":"test-product",
    "quantity":1,
    "total_price":100,
    "shipping_address":"Test Address"
  }'
```

---

Last Updated: March 2024
