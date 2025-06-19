# Faber Fatigue DB

Find current db schema in [docs/](docs/).

## Sample .env file for Faber Fatigue DB

```env
# Database settings (adjust as per your CloudNativePG setup)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=faber
POSTGRES_PASSWORD=password
POSTGRES_DB=faber
```
So far it needs to be created manually in both the alembic directory and the main directory.


## How to run the Faber Project locally with Docker Compose

```bash
docker compose up --build -d
```

## Alembic Migrations

### Make migrations

```bash
alembic revision --autogenerate -m "<migration_message>" 
```

### Apply migrations

```bash
alembic upgrade head
```
