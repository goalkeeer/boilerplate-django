#!/bin/bash
CELERY_PROC_COUNT_MAIN="${CELERY_PROC_COUNT_MAIN:-2}"

exec python -u -m celery -A _project_ worker \
    --loglevel info \
    --concurrency "$CELERY_PROC_COUNT_MAIN" \
    -n main@%h
