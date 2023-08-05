from globalframework.errors import QueueError, exception_raiser
from globalframework.mail import mailer
from globalframework.celery_app import app


def send(*args, bypass=False, **kwargs):
    if bypass:
        return mailer.send(*args, **kwargs)
    try:
        return send_mailer.apply_async(args, kwargs, argsrepr='None', kwargsrepr='None')
    except Exception as e:
        exception_raiser(e, QueueError, 'General Queue Error')


@app.task(name='send_mailer')
def send_mailer(*args, **kwargs):
    mailer.send(*args, **kwargs)
