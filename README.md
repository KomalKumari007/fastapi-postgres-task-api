# FastAPI Postgres Task API

A backend task management API built with FastAPI, PostgreSQL, and Docker.

## Project Structure
- **`main.py`**: FastAPI application entry point and API routes.
- **`database.py`**: Database configuration and session management.
- **`docker-compose.yml`**: Docker configuration for the PostgreSQL database.
- **`requirements.txt`**: Project dependencies.

## Prerequisites
- Python 3.10+
- Docker & Docker Desktop

## Setup & Installation

1. **Start the Database via Docker:**
   ```bash
   docker compose up -d
