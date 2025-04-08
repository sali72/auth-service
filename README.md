# 🔐 Auth Service

A robust authentication microservice built with FastAPI, SQLModel, and PostgreSQL, featuring event-driven architecture for seamless integration with other services.

## 🚀 Features

- **🔑 Authentication & Authorization**
  - JWT-based authentication
  - Role-based access control (Superuser support)
  - Password recovery and reset functionality
  - Email verification support

- **📡 Event-Driven Architecture**
  - Real-time user creation/deletion notifications
  - Configurable event targets
  - Retry mechanism for reliable event delivery
  - Database event triggers

- **🔒 Security**
  - Password hashing
  - JWT token management
  - Email-based password recovery
  - Environment-based configuration

## 🛠️ Tech Stack

- **FastAPI** - Modern, fast web framework
- **SQLModel** - SQL database in Python, designed for simplicity and compatibility
- **PostgreSQL** - Robust relational database
- **Docker** - Containerization for easy deployment
- **Pydantic** - Data validation and settings management

## 🏗️ Architecture

The service follows a clean architecture with:
- API routes for user management and authentication
- Database event listeners for automatic event publishing
- Configurable event publisher for service integration
- Environment-based configuration management

## 🚀 Getting Started

1. **Prerequisites**
   - Docker and Docker Compose
   - Python 3.8+

2. **Environment Setup**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Running with Docker**
   ```bash
   docker-compose up -d
   ```

4. **Development**
   ```bash
   docker-compose up -d
   # The service will be available at http://localhost:5000
   ```

## 📚 API Documentation

Once running, access the interactive API documentation at:
- Swagger UI: `http://localhost:5000/docs`
- ReDoc: `http://localhost:5000/redoc`

## 🔄 Event Configuration

Configure event targets in `.env`:
```env
EVENTS_ENABLED=true
EVENT_TARGETS={"user_created": ["http://target-service/users/"], "user_deleted": ["http://target-service/users/"]}
```

## 📝 License

This project is based on [tiangolo's full-stack-fastapi-template](https://github.com/tiangolo/full-stack-fastapi-template) and is licensed under the MIT License.
