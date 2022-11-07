# CloudStorageManager

This service allows to manage files in several cloud providers using one API

Working cloud providers:

- AWS
- GCP

### Quick Setup:

```docker-compose up```

### Local Setup:


- Set required services Redis, MongoDB
- `pip install --upgrade pip`
- `pip install -r requirements.txt`
- Set envs from .env-example
- `uvicorn app:app --host localhost --reload`
- `celery -A worker.celery worker --loglevel=info`