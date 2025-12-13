# Django Authentication API

## Quick Setup

### 1. Installation
```bash
pip install django djangorestframework
python manage.py makemigrations accounts
python manage.py migrate
```

### 2. Configuration
Add to `settings.py`:
```python
AUTH_USER_MODEL = 'accounts.CustomUser'
INSTALLED_APPS += ['rest_framework', 'rest_framework.authtoken', 'accounts']
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}
```

## API Endpoints

### Register User
```bash
POST /api/auth/register/
{
  "username": "john",
  "email": "john@email.com",
  "password": "pass123",
  "password2": "pass123",
  "first_name": "John",
  "last_name": "Doe"
}
```
→ Returns token for authentication

### Login
```bash
POST /api/auth/login/
{
  "username": "john",
  "password": "pass123"
}
```
→ Returns authentication token

### Get Profile
```bash
GET /api/auth/profile/
Header: Authorization: Token YOUR_TOKEN_HERE
```

### Follow/Unfollow Users
```bash
POST /api/auth/follow/3/
Header: Authorization: Token YOUR_TOKEN_HERE
```
→ Toggles follow status for user ID 3

## User Model Features
- **Extended fields**: bio, profile_picture
- **Social features**: followers/following system
- **Token authentication**: Secure API access
- **Admin ready**: Custom admin interface

## Authentication Flow
1. Register → Get token
2. Use token in `Authorization` header
3. Access protected endpoints
4. Token persists until logout

## Testing
```bash
python manage.py createsuperuser  # Admin access
python manage.py runserver  # Start dev server
```