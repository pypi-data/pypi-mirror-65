from globalframework.errors import QueueError, exception_raiser
from globalframework.logger.log import Logger
from globalframework.celery_app import app


class QueueLogger:
    def __init__(self, logger_name='FCSGLOBALFRAMEWORK', debug=False):
        self.logger_name = logger_name
        self.debug = debug

    def write(self, message, message_type, indentifier_id=None, bypass=False):
        if bypass:
            return Logger(self.logger_name, self.debug).write(message, message_type, indentifier_id)
        try:
            return send_logger.apply_async((self.logger_name, self.debug, message, message_type, indentifier_id), argsrepr='None', kwargsrepr='None')
        except Exception as e:
            exception_raiser(e, QueueError, 'General Queue Error')


@app.task(name='send_logger')
def send_logger(logger_name, debug, message, message_type, indentifier_id):
    Logger(logger_name, debug).write(message, message_type, indentifier_id)
