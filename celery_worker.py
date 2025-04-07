from app import create_app

from helpers.celerysetup import celery
app = create_app()
celery.conf.update(app.config)