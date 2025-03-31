from django.apps import AppConfig
import redis
from dotenv import load_dotenv
import os

load_dotenv()


class McDonaldsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mc_donalds'

red = redis.Redis(
    host='redis-17520.c328.europe-west3-1.gce.redns.redis-cloud.com',
    port='17520',
    password=os.getenv('REDIS_PASSWORD')
)
