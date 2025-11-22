
## Authentication
- **Token Authentication**: Required for protected endpoints
- **Get Token**: `POST /api-token-auth/` with `username` and `password`
- **Use Token**: Include `Authorization: Token your_token_here` in headers

##  Permissions
- **Public Access**: Anyone can view books (`GET /api/books/`)
- **Protected Access**: Only authenticated users can create, update, or delete books

## Quick Start
1. Get token:
```bash
curl -X POST http://localhost:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'