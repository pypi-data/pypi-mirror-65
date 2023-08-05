import platform
from celery import Celery
from globalframework.data.setting import QueueSetting
from globalframework.security.encrypto_json import MIMETYPE



settings = QueueSetting().get_queue_connection()

app = Celery(broker=settings['CELERY_BROKER'])
app.conf.update(
    CELERY_ROUTES=settings['CELERY_ROUTES'],
    CELERY_TASK_SERIALIZER='fernet_json',
    CELERY_ACCEPT_CONTENT=[MIMETYPE],
    BROKER_TRANSPORT_OPTIONS=settings['BROKER_TRANSPORT_OPTIONS']
)
app.autodiscover_tasks(['globalframework.mail.queue_mailer', 'globalframework.logger.queue_log'])


def argv():
    argv = ['celery', 'worker', '--loglevel=INFO', '--queue=send_mailer,send_logger']
    if platform.system() == 'Windows':
        argv.append('--pool=gevent')
        return argv
    return argv


if __name__ == '__main__':
    app.start(argv=argv())
