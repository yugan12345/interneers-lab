# Product API

A REST API built with Django for managing warehouse products. Supports full CRUD operations, pagination, and validation — all using in-memory storage.

## Table of Contents
- [Description](#description)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)
- [Validations](#validations)
- [Pagination](#pagination)
- [Error Handling](#error-handling)
- [License](#license)

---

## Description

This project is a Django-based REST API that allows you to manage products in a warehouse. It was built to practice REST API design principles including:

- Clean URL structure using nouns over verbs
- Proper use of HTTP methods (GET, POST, PUT, DELETE)
- Meaningful error responses
- Paginated list endpoints

All data is stored in memory — no database is required.

---

## Installation
```bash
# 1. Clone the repository
git clone <your-repo-url>
cd <your-repo-name>

# 2. Install Django
pip install django

# 3. Run the server
python manage.py runserver
```

---

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | /products/ | Get all products (paginated) |
| POST | /products/ | Create a new product |
| GET | /products/{id}/ | Get a single product |
| PUT | /products/{id}/ | Update a product |
| DELETE | /products/{id}/ | Delete a product |

---

## Usage

### Create a product
Send a POST request to `/products/` with this JSON body:
```json
{
    "name": "iPhone 15",
    "description": "Latest Apple smartphone",
    "category": "Electronics",
    "price": 999.99,
    "brand": "Apple",
    "quantity": 50
}
```

### Get all products
```
GET /products/
```

### Get a single product
```
GET /products/1/
```

### Update a product
Send a PUT request to `/products/1/` with only the fields you want to change:
```json
{
    "price": 899.99,
    "quantity": 45
}
```

### Delete a product
```
DELETE /products/1/
```

---

## Validations

All fields are required when creating a product. The following rules apply:

- `name` — required, max 255 characters
- `description` — required
- `category` — required
- `price` — required, must be a positive number
- `brand` — required
- `quantity` — required, must be a positive integer

---

## Pagination

The fetch all products endpoint supports pagination via query parameters:
```
GET /products/?page=1&page_size=5
```

Response includes:
```json
{
    "page": 1,
    "page_size": 5,
    "total_products": 10,
    "total_pages": 2,
    "products": [...]
}
```

---

## Error Handling

All errors return a structured JSON response:
```json
{
    "error": "Validation failed",
    "message": "One or more fields are invalid.",
    "details": {
        "price": "Price must be a positive number"
    }
}
```

---