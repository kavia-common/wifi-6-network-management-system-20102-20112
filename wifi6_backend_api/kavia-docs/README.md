# WiFi 6 Backend API

This container implements the backend API for the WiFi 6 Network Management System, using [FastAPI](https://fastapi.tiangolo.com/) for rapid, typed RESTful development.

## Architecture

- **Tech Stack:** FastAPI, Python 3, Pydantic, OAuth2 JWT Authentication, CORS enabled
- **Endpoints:** RESTful, grouped by:
    - `/users` - Registration, login, and user info
    - `/devices` - Manage WiFi 6 devices (CRUD)
    - `/configs` - Manage WiFi 6 configuration profiles (CRUD)
- **Security:** All mutations and sensitive reads require a valid JWT access token provided via the `Authorization: Bearer ...` HTTP header.

## Main Modules & Files

- `main.py`: FastAPI app definition, CORS, routers, health check
- `users.py`: User registration, login logic, JWT issuance/verification
- `devices.py`: Device model and CRUD endpoints
- `configs.py`: Configuration profiles and endpoints
- `utils.py`: Password hashing, JWT utilities
- `interfaces/openapi.json`: OpenAPI schema (auto-generated)

## Endpoints Overview

| Path                              | Method       | Purpose                               | Auth Required |
|------------------------------------|-------------|---------------------------------------|:-------------:|
| `/users/register`                  | POST        | Register new user                     |      No       |
| `/users/login`                     | POST        | Obtain JWT access token (login)       |      No       |
| `/users/me`                        | GET         | Current user data                     |     Yes       |
| `/devices/`                        | GET/POST    | List/add devices                      |     Yes       |
| `/devices/{device_id}`             | GET/PUT/DEL | Get, update or delete single device   |     Yes       |
| `/configs/`                        | GET/POST    | List/add configuration profiles       |     Yes       |
| `/configs/{config_id}`             | GET/PUT/DEL | Get, update or delete config          |     Yes       |
| `/configs/device/{device_id}`      | GET         | List configs tied to a device         |     Yes       |
| `/`                                | GET         | Health check endpoint                 |      No       |

- For detailed schema, see `interfaces/openapi.json`.

## Authentication

- Registration: Via `/users/register` (POST, JSON body)
- Login: Via `/users/login` (POST, form-encoded) -> returns JWT access_token
- Use JWT as `Authorization: Bearer <token>` on all protected endpoints

Example Python request:
```python
import requests
# Login
r = requests.post("http://localhost:3001/users/login", data={"username":"me@domain.com", "password":"pw"})
jwt = r.json()["access_token"]

# Authenticated API call
resp = requests.get("http://localhost:3001/devices/", headers={"Authorization": f"Bearer {jwt}"})
```

## Local Development

- Install dependencies: `pip install -r requirements.txt`
- Run: `uvicorn src.api.main:app --reload --host 0.0.0.0 --port 3001`
- API Docs (Swagger UI): [http://localhost:3001/docs](http://localhost:3001/docs)

**Note:** In-memory data storage only—production systems should integrate a persistent database and rotate/secure all credentials and secret keys.
