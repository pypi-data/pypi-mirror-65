# default libraries
import uuid
from dataclasses import dataclass

# Globalframework packages
from globalframework.enumeration import LoggerType, LoggerSeverityType
from globalframework.logger.log import Logger


def _get_uuid():
    return uuid.uuid1()


class GFError(Exception):
    """Global Framework general exceptions"""

    def __init__(self, err):
        pass


class CachingError(GFError):
    """General error related to GF Caching package"""

    def __init__(self, err):
        pass


class SecurityError(GFError):
    """General error related to GF Security package"""

    def __init__(self, err):
        pass


class LoggerError(GFError):
    """Fcs.globalframework.logger General error"""

    def __init__(self, err):
        pass


class InternationalisationError(GFError):
    """Fcs.globalframework.internationalisation general error"""

    def __init__(self, err):
        pass


class ValidationError(GFError):
    """Fcs.globalframework.validation general error"""

    def __init__(self, err):
        pass


class EmailError(GFError):
    """Fcs.globalframework.mail general error"""

    def __init__(self, err):
        pass


class DataError(GFError):
    """Fcs.globalframework.data general error"""
    pass


class DataConfigurationError(DataError):
    """Fcs.globalframework.data Configuration general error"""
    pass


class GFDatabaseError(DataError):
    """Fcs.globalframework.data general error"""
    pass


class InterfaceError(GFDatabaseError):
    """Fcs.globalframework.data database Exception raised for errors that are related to the database
    interface rather than the database itself."""
    pass


class DatabaseError(GFDatabaseError):
    """Fcs.globalframework.data database general error"""
    pass


class QueueError(GFError):
    """Fcs.globalframework.queue general error"""


def error_raiser(exception, exception_type, logger: Logger, exception_msg: str):
    error_msg = format_exception_msg(exception.args, exception_msg)
    logger.write(error_msg.log_msg, error_msg.msg_type, error_msg.guid)
    raise exception_type(exception_msg)


def exception_raiser(err, exception_type: Exception, message: str = None):
    msg = ''
    if hasattr(err, 'args'):
        msg = format_exception_msg(err.args, message)
    else:
        msg = format_exception_msg(err, message)
    logger = Logger(LoggerType.FCSGLOBALFRAMEWORK.name)
    logger.write(msg.log_msg,
                 msg.msg_type,
                 msg.guid)
    raise exception_type(msg.user_msg)


@dataclass
class DisplayMessage:
    log_msg: str
    user_msg: str
    guid: str
    msg_type: LoggerSeverityType


def format_exception_msg(err, exception_type_msg: str = None):
    user_msg = "{0} - [Please review error: {1}]"
    guid = _get_uuid()
    error_code = err[0]
    error_msg = ''
    if err.__len__() > 1:
        error_msg = err[1]
    dis_msg = DisplayMessage("{0}: Error Code:{1}, Message:{2}".format(exception_type_msg, error_code, error_msg), user_msg.format(exception_type_msg, guid), guid, LoggerSeverityType.ERROR.name)
    return dis_msg


def format_warning_msg(exception_type_msg: str):
    user_msg = "{0} - [Please review warning: {1}]"
    guid = _get_uuid()
    dis_msg = DisplayMessage("Message {0}".format(exception_type_msg), user_msg.format(
        exception_type_msg, guid), guid, LoggerSeverityType.WARNING.name)
    return dis_msg
