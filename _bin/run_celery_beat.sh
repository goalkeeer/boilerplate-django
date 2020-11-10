#!/bin/bash

CELERY_BEAT_PID_PATH=/tmp/celerybeat.pid
rm -f $CELERY_BEAT_PID_PATH

exec python -u \
-m celery -A _project_ beat \
--loglevel info \
--pidfile="${CELERY_BEAT_PID_PATH}" \
--schedule="/tmp/celerybeat-schedule.db"
