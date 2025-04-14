# 🔐 Auth Service

A robust authentication microservice built with FastAPI, SQLModel, and PostgreSQL, featuring event-driven architecture for seamless integration with other services. Available on Docker Hub for quick and easy integration into your applications.

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

## 🐳 Docker Deployment

To use this service in your projects, pull the image from Docker Hub:

```bash
docker pull sali72/auth-service:latest
```

### Required Environment Variables

Create a `.env` file with the following required variables:

```env
# Database Configuration
POSTGRES_SERVER=your-db-host
POSTGRES_PORT=5432
POSTGRES_USER=your-db-user
POSTGRES_PASSWORD=your-db-password
POSTGRES_DB=auth_service

# Security
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Email Configuration (Required for password reset)
SMTP_TLS=True
SMTP_PORT=587
SMTP_HOST=your-smtp-host
SMTP_USER=your-smtp-user
SMTP_PASSWORD=your-smtp-password
EMAILS_FROM_EMAIL=your-from-email
EMAILS_FROM_NAME=your-from-name

# Initial Superuser (Required for first setup)
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=your-password

# Event Configuration (Optional)
EVENTS_ENABLED=True
EVENT_TARGETS={"user_created": ["http://your-service/users/"], "user_deleted": ["http://your-service/users/"]}
```

### Example docker-compose.yml

```yaml
version: '3.8'
services:

  auth-service:
    image: sali72/auth-service:latest
    # add --root-path if use proxy
    command: fastapi dev --host 0.0.0.0 --reload app/main.py --root-path /api-root
    ports:
      - "5000:8000"
    env_file:
      - .env
    depends_on:
      - db
    networks:
      - your-network

  db:
    image: postgres:12
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:

networks:
  your-network:
    driver: bridge
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
