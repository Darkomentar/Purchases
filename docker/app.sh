#!/bin/bash

alembic upgrade head && 


gunicorn app.fast_api_programm:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000