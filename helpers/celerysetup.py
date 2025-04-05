from celery import Celery, Task


class ContextTask(Task):
    def __call__(self, *args, **kwargs):
            with self.app.flask_app.app_context():
                return self.run(*args, **kwargs)



def setup_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND'],
        include=app.config.get('CELERY_INCLUDE', []),
        task_cls = 'helpers.celerysetup:ContextTask'
    )
    celery.conf.update(app.config)

    celery.flask_app = app

    for module in app.config.get('CELERY_INCLUDE', []):
        __import__(module)

    return celery