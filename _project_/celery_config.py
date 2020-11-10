import os

from .settings import DATA_DIR, REDIS_URL, TIME_ZONE

result_backend = REDIS_URL
broker_url = REDIS_URL
timezone = TIME_ZONE
task_serializer = 'json'
accept_content = ['json']  # Ignore other content
result_serializer = 'json'
result_expires = 3600

beat_schedule_filename = os.path.join(DATA_DIR, 'celerybeat.db')

beat_schedule = {}
