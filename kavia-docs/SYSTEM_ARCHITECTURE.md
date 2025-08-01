# WiFi 6 Network Management System: System Architecture

## Overview

The WiFi 6 Network Management System is a full-stack application for the management and configuration of WiFi 6 devices. It features a modern, minimalistic React frontend and a robust FastAPI backend. The system allows authenticated users to register/login, view connected devices, manage WiFi configurations, and perform CRUD operations on both devices and configurations.

## Architecture Diagram

```mermaid
flowchart TD
    subgraph Browser
        FE[Frontend (React App)]
    end
    subgraph "wifi6_frontend_app\n(React Single Page App)"
        FE
    end

    subgraph Server
        BE[Backend API (FastAPI)]
    end
    subgraph "wifi6_backend_api\n(FastAPI REST API)"
        BE
    end

    FE -- "REST (HTTP/JSON)" --> BE
    BE -.->|"In-memory DB\n(demo only)"| BE
```

## Component Roles

### 1. Frontend - `wifi6_frontend_app`
- **Framework:** React (SPA)
- **User-facing features:** 
    - User authentication (login/register)
    - Dashboard view with summary
    - Devices page: List/add/edit/delete WiFi 6 devices
    - Configs page: List/add/edit/delete WiFi 6 configurations
- **API Usage:** All data fetched & mutated via the REST API provided by the backend
- **Authentication Storage:** JWT access token kept in browser Local Storage and used as a Bearer token in API requests

### 2. Backend - `wifi6_backend_api`
- **Framework:** FastAPI
- **Responsibilities:**
    - User registration, authentication (JWT, OAuth2 password flow)
    - REST endpoints for CRUD operations on Devices and Configs
    - Simple in-memory storage for users, devices, configs (demo/testing only)
    - CORS enabled for frontend integration

## Integration & Flow

1. **User Authentication**
    - Registration: POST `/users/register` (JSON body)
    - Login: POST `/users/login` (form-encoded, returns JTW access_token)
    - Frontend stores JWT in localStorage; attaches bearer token to all subsequent API requests

2. **Data Flow**
    - All device/config operations are allowed only for authenticated users
    - Backend verifies and decodes JWT tokens for authorization

3. **Separation of Concerns**
    - All business and validation logic is on backend (FastAPI)
    - Frontend is responsible for display, navigation, and making authenticated API requests

## Security Considerations

- JWT tokens never sent via cookies; always passed as Authorization headers
- CORS configuration is open for demo, should be restricted for production
- No direct database is used: all persistence is in-memory for demo; production should add database and secure secrets

## API Endpoint Summary

**Endpoints:**
- `/users/register` - Register new users
- `/users/login` - Login, returns JWT token
- `/users/me` - Fetch current user (auth*)
- `/devices/` - CRUD endpoints for devices (auth*)
- `/configs/` - CRUD endpoints for configurations (auth*)
- `/configs/device/{device_id}` - List all configs for a given device

(* Requires Authorization: Bearer <JWT>)
