#!/bin/bash
# Render start script - usando gunicorn con uvicorn workers para producción
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-8000}