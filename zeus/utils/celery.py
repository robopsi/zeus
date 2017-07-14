import celery
import json

from celery.signals import task_prerun, task_postrun
from kombu import serialization
from kombu.utils.encoding import bytes_t
from raven.contrib.celery import register_signal, register_logger_signal
from uuid import UUID


class Celery(object):
    def __init__(self, app=None, sentry=None):
        # we create the celery immediately as otherwise NOTHING WORKS
        self.app = None
        self.context = None
        self.celery = celery.Celery(__name__)
        if app:
            self.init_app(app, sentry)
        register_serializer()

    def init_app(self, app, sentry):
        self.app = app
        self.celery.__autoset('broker_url', app.config['CELERY_BROKER_URL'])
        self.celery.__autoset('result_backend', app.config['CELERY_RESULT_BACKEND'])
        self.celery.conf.update(app.config)

        task_prerun.connect(self._task_prerun)
        task_postrun.connect(self._task_postrun)

        if sentry:
            register_signal(sentry.client)
            register_logger_signal(sentry.client)

    def task(self, *args, **kwargs):
        return self.celery.task(*args, **kwargs)

    def get_celery_app(self):
        return self.celery

    def _task_prerun(self, task, **kwargs):
        if self.app is None:
            return
        context = task._flask_context = self.app.app_context()
        context.push()

    def _task_postrun(self, task, **kwargs):
        try:
            context = task._flask_context
        except AttributeError:
            return
        context.pop()


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, value):
        if isinstance(value, UUID):
            return str(value)
        elif isinstance(value, bytes_t):
            return value.decode()
        return value


def register_serializer():
    serialization.register(
        'zeus_json',
        lambda v: json.dumps(v, cls=EnhancedJSONEncoder),
        json.loads,
        content_type='application/json',
        content_encoding='utf-8'
    )
