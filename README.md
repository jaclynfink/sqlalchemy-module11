A FastAPI project with a SQLAlchemy `User` model, Pydantic schemas, password hashing, unit/integration tests, and CI/CD to Docker Hub.

## Features

- **FastAPI** REST API
- **SQLAlchemy** ORM user model
  - `username`
  - `email`
  - `password_hash`
  - `created_at`
- **Pydantic** schemas
  - `UserCreate` for input validation
  - `UserRead` for safe API responses
- **Password security**
  - Passlib `CryptContext`
  - `bcrypt_sha256` hashing + verification helpers
- **Testing**
  - Unit tests (hashing, schema validation, etc.)
  - Integration tests with real Postgres
- **CI/CD (GitHub Actions)**
  - Run tests
  - Container security scan (Trivy)
  - Build and push image to Docker Hub

---

## Local Setup

### 1) Clone and enter project

```bash
git clone <your-repo-url>
cd sqlalchemy-module10
```

### 2) Create and activate virtual environment (macOS)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Configure environment

Create `.env` (or export directly in shell) with your DB connection:

```bash
export DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/myappdb"
```

### 5) Run the app

```bash
uvicorn app.main:app --reload
```

Open:
- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

---

## Running Tests

### Unit tests

```bash
pytest -q tests/unit
```

### New calculation unit tests

Run only the new calculation-focused unit tests (factory, schema validation, and model behavior):

```bash
pytest -q tests/unit/test_calculation_factory.py tests/unit/test_calculation_model.py tests/unit/test_calculation_schemas.py
```

### Integration tests (requires Postgres)

```bash
export DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/myappdb"
pytest -q tests/integration
```

### New calculation integration tests (requires Postgres)

```bash
export DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/myappdb"
pytest -q tests/integration/test_calculation_integration.py
```

### Full test suite

```bash
pytest -q
```

---

## Docker

### Build image

```bash
docker build -t sqlalchemy-module10:local .
```

### Run with local Postgres container

```bash
docker network create appnet

docker run -d \
  --name mypg \
  --network appnet \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=myappdb \
  -p 5432:5432 \
  postgres:latest

docker run --rm -it \
  --name myapp \
  --network appnet \
  -e DATABASE_URL="postgresql+psycopg2://user:password@mypg:5432/myappdb" \
  -p 8000:8000 \
  sqlalchemy-module10:local
```

---

## CI/CD Pipeline

Workflow: `.github/workflows/test.yml`

On push/PR to `main`, pipeline runs:

1. **test**: unit + integration tests  
2. **security**: Trivy image scan  
3. **deploy** (main only): push image to Docker Hub

### Required GitHub Secrets

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN` (must include **read + write** scopes)