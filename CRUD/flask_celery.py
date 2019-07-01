# Important file to integrate flask and celery
from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend='db+postgresql://postgres:123456789@localhost/books_store',
        broker='amqp://localhost//'
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery