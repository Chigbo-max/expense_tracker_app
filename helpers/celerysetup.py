from celery import Celery, Task


class ContextTask(Task):

    def __call__(self, *args, **kwargs):
        from app import app
        with app.app_context():
            return Task.__call__(self, *args, **kwargs)


def setup_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND'],
        include=app.config.get('CELERY_INCLUDE', []),
        task_cls=ContextTask
    )

    celery.conf.update(app.config)

    for module in app.config.get('CELERY_INCLUDE', []):
        __import__(module)

    return celery


celery = None