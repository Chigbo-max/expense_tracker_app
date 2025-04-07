import os

from celery.schedules import crontab
from flask.cli import load_dotenv
from mongoengine import connect

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    MONGO_URI = os.environ.get('MONGO_URI')
    FRONTEND_URI = os.environ.get('FRONTEND_URI')
    MONGO_HOST = '192.168.0.168'
    MONGO_PORT = 27017

    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
    CELERY_INCLUDE = ['apps.services.tasks']

    CELERY_BEAT_SCHEDULE = {
        'monthly-rollovers': {
            'task': 'apps.services.tasks.process_rollover',
             'schedule': crontab(minute=5),
            # 'schedule': crontab(day_of_month=1, minute=15, hour=0),
        }
    }



def init_database():
    try:
        connect(host=Config.MONGO_URI)
        print("Database connection established")
    except Exception as e:
        print("Error connecting to database", e)
        exit(1)



