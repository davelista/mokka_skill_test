# Users Router API Documentation

This document describes the **Users Router API**, detailing available endpoints, request formats, and expected responses.

---

## Get All Users
### Endpoint:  
```http
GET /users
```
### Authentication:  
- No authentication required.

### Request Example:
```bash
curl -X GET http://127.0.0.1:5000/users
```

### Response Example (`200 OK`):
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

### Possible Errors
| Status Code | Message | Description |
|-------------|---------|-------------|
| `500` | `"error": "Internal Server Error"` | Unexpected error on the server. |

---

## Create a New User
### Endpoint:  
```http
POST /users
```
### Authentication:  
- Requires **JWT Authorization**.
- Only **admin users** can create new users.

### Request Example:
```bash
curl -X POST http://127.0.0.1:5000/users \
     -H "Authorization: Bearer <TOKEN_USER>" \
     -H "Content-Type: application/json" \
     -d '{
         "email": "newuser@example.com",
         "username": "newuser",
         "firstname": "Mario",
         "lastname": "Rossi",
         "password": "newpassword"
     }'
```
### Request Body (JSON)
| Field | Type | Required | Description |
|--------|------|----|-------------|
| `email` | `string` | Yes | The email of the new user. Must be unique. |
| `username` | `string` | Yes | The username for the new user. Must be unique. |
| `firstname` | `string` | Yes | The first name of the user. |
| `lastname` | `string` | Yes | The last name of the user. |
| `password` | `string` | Yes | The password for authentication. |
| `is_admin` | `boolean` | No | Defaults to `false`, only admin users can create admins. |

### Response Example (`201 Created`):
```json
{
    "message": "User added"
}
```

### Possible Errors
| Status Code | Message | Description |
|-------------|---------|-------------|
| `400` | `"message": "Required {field} are missing"` | A required field is missing. |
| `401` | `"msg": "Missing Authorization Header"` | The request is missing the JWT token. |
| `403` | `"error": "Access deny. Only admin can create users."` | The user is not an admin and cannot create users. |
| `500` | `"error": "Internal Server Error"` | Unexpected error on the server. |

---

## Update User
### Endpoint:  
```http
PUT /users/<id>
```
### Request Example:
```bash
curl -X PUT http://127.0.0.1:5000/users/1 \
     -H "Authorization: Bearer <TOKEN_ADMIN>" \
     -H "Content-Type: application/json" \
     -d '{
         "firstname": "Updated Name",
         "lastname": "Updated Lastname",
         "username": "updatedusername",
         "email": "updated@example.com"
     }'
```
### Response Example (`200 OK`):
```json
{
    "message": "User updated successfully"
}
```

### Possible Errors
| Status Code | Message | Description |
|-------------|---------|-------------|
| `400` | `"error": "No data provided"` | No fields were provided for update. |
| `403` | `"error": "Access denied. Only admins can modify users."` | The user is not an admin. |
| `404` | `"error": "User not found"` | The user ID does not exist. |
| `500` | `"error": "Internal Server Error"` | Unexpected error on the server. |

---

## Delete User
### Endpoint:  
```http
DELETE /users/<id>
```
### Request Example:
```bash
curl -X DELETE http://127.0.0.1:5000/users/1 \
     -H "Authorization: Bearer <TOKEN_ADMIN>"
```
### Response Example (`200 OK`):
```json
{
    "message": "User deleted successfully"
}
```

### Possible Errors
| Status Code | Message | Description |
|-------------|------------------------------------|-------------|
| `403` | `"error": "Access denied. Only admins can delete users."` | The user is not an admin. |
| `404` | `"error": "User not found"` | The user ID does not exist. |
| `500` | `"error": "Internal Server Error"` | Unexpected error on the server. |

---

## Notes
- **JWT Authentication:** All protected endpoints require a valid token. Ensure you include `Authorization: Bearer <TOKEN>` in the headers.
- **Admin Restrictions:** Only admins can create, update, or delete users.
- **Password Security:** Passwords are stored securely using bcrypt hashing.

