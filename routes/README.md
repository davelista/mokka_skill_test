# Router API Documentation

This document describes the **Router API**, detailing the available endpoints, request formats, and expected responses.

---

## Users API

### Get All Users

#### Endpoint:

```http
GET /users
```

#### Authentication:

- Not required.

#### Request Example:

```bash
curl -X GET http://127.0.0.1:5000/users
```

#### Response Example (`200 OK`):

```json
[
    {
        "id": 1,
        "email": "admin@example.com",
        "username": "adminuser",
        "firstname": "Admin",
        "lastname": "User",
        "is_admin": true
    },
    {
        "id": 2,
        "email": "user@example.com",
        "username": "testuser",
        "firstname": "John",
        "lastname": "Doe",
        "is_admin": false
    }
]
```

#### Possible Errors

| Status Code | Message                          | Description                    |
| ----------- | ---------------------------------- | ------------------------------ |
| `500`       | `"error": "Internal Server Error"` | Unexpected server error. |

---

### Login

#### Endpoint:

```http
POST /login
```

#### Authentication:

- Not required.

#### Request Example:

```bash
curl -X POST http://127.0.0.1:5000/login \
     -H "Content-Type: application/json" \
     -d '{
         "email": "user@example.com",
         "password": "password123"
     }'
```

#### Response Example (`200 OK`):

```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCIg..."
}
```

#### Possible Errors

| Status Code | Message | Description |
| ------------------------------- | --------- | ----------- |
| `401` | `"error": "Invalid credentials"` | Email or password incorrect. |
| `500` | `"error": "Internal Server Error"` | Unexpected server error. |

---

## Orders API

### Get All Orders

#### Endpoint:

```http
GET /orders
```

#### Authentication:

- Requires **JWT Authorization**.
- Only **admins** can access.

#### Request Example:

```bash
curl -X GET http://127.0.0.1:5000/orders \
     -H "Authorization: Bearer <TOKEN_ADMIN>"
```

#### Response Example (`200 OK`):

```json
{
    "total_orders": 150,
    "order_status_counts": {
        "pending": 50,
        "shipped": 40,
        "delivered": 50,
        "cancelled": 10
    },
    "orders": [
        {
            "id": 1,
            "user_id": 2,
            "status": "pending",
            "total_price": 99.99
        }
    ]
}
```

---

### Get Orders by Status

#### Endpoint:

```http
GET /orders/<status>
```

#### Request Example:

```bash
curl -X GET http://127.0.0.1:5000/orders/pending \
     -H "Authorization: Bearer <TOKEN_ADMIN>"
```

#### Possible Errors

| Status Code | Message | Description |
| ----------- | -------------------------------------------------- | ------------------------------ |
| `400`       | `"error": "Invalid status. Allowed values: [...]"` | Invalid status. |
| `500`       | `"error": "Internal Server Error"`                 | Unexpected server error. |

---

### Get Product Analytics

#### Endpoint:

```http
GET /orders_details/<product_id>
```
#### Request Example:

```bash
curl -X GET http://127.0.0.1:5000/orders_details/1 \
     -H "Authorization: Bearer <TOKEN_ADMIN>"
```

#### Response Example (`200 OK`):

```json
{
    "product_id": 1,
    "product_name": "Smartphone XYZ",
    "total_orders": 120,
    "total_revenue": 15000.75,
    "average_revenue": 125.00
}
```

---

### Get Best Buyer

#### Endpoint:

```http
GET /orders/best_buyer
```

#### Request Example:

```bash
curl -X GET http://127.0.0.1:5000/orders/best_buyer \
     -H "Authorization: Bearer <TOKEN_ADMIN>"
```

#### Response Example (`200 OK`):

```json
{
    "user_id": 5,
    "email": "topbuyer@example.com",
    "username": "topbuyer",
    "firstname": "Alice",
    "lastname": "Brown",
    "total_orders": 50
}
```

---

### Get Orders per User

#### Endpoint:

```http
GET /orders/user_orders
```

#### Request Example:

```bash
curl -X GET http://127.0.0.1:5000/orders/user_orders \
     -H "Authorization: Bearer <TOKEN_ADMIN>"
```

#### Response Example (`200 OK`):

```json
[
    {
        "user_id": 2,
        "username": "testuser",
        "total_orders": 30
    }
]
```

---

### Get Average Orders per User

#### Endpoint:

```http
GET /orders/average_orders
```

#### Request Example:

```bash
curl -X GET http://127.0.0.1:5000/orders/average_orders \
     -H "Authorization: Bearer <TOKEN_ADMIN>"
```

#### Response Example (`200 OK`):

```json
{
    "average_orders_per_user": 5.2
}
```

---

### Get Revenue per Month

#### Endpoint:

```http
GET /orders/month
```
#### Request Example:

```bash
curl -X GET http://127.0.0.1:5000/orders/month \
     -H "Authorization: Bearer <TOKEN_ADMIN>"
```

#### Response Example (`200 OK`):

```json
[
    {
        "month": "2024-01",
        "total_revenue": 12500.75
    }
]
```

---

## Notes

- **JWT Authentication:** Protected endpoints require a valid token in the format `Authorization: Bearer <TOKEN>`.
- **Admin Restrictions:** Only administrators can access sensitive order information.
- **Password Security:** Passwords are securely stored using bcrypt hashing.
