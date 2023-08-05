"""Container for all enum values used by Fcs.globalframework."""
# default in libraries
from enum import Enum


class AppTypes(Enum):
    ALL = 1
    NEXTGEN = 2
    RECOVERY = 3


class PathCol(Enum):
    CLIENT_ID = 0


class ConfiCol(Enum):
    CONFIG_ID = 0
    CONFIG_ALIAS = 1
    CONFIG_VALUE = 2


class FrequencyType(Enum):
    EVERY_HOUR = 1
    EVERY_4_HOUR = 4
    EVERY_8_HOUR = 8
    EVERY_12_HOUR = 12
    EVERY_24_HOUR = 24
    EVERY_30_DAYS = 720


class QueryType(Enum):
    SELECT = 1
    INSERT = 2
    UPDATE = 3
    DELETE = 4


class LoggerType(Enum):
    ROOT = 1
    ROOTAWS = 2
    FCSGLOBALFRAMEWORK = 3
    FCSCOMPONENTS = 4


class LoggerSeverityType(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4
    DEBUG = 5


class ConfigurationTypes(Enum):
    APPLICATION_DATABASE = 'ApplicationDatabase'
    CACHING = "Caching"
    ENVIRONMENT = "Environment"
    TOKEN = "Token"
    EMAIL = "EmailSetting"
    QUEUE = "QueueSetting"
    HASH = "HashSetting"


class OperatingSystemTypes(Enum):
    ALL = 1
    WINDOWS = 2
    LINUX = 3


class DatabaseTypes(Enum):
    MSSQL = "Mssql"
    MYSQL = "Mysql"
    POSTGRES = "Postgre"


class DatabaseConnectionArgs(Enum):
    TIMEOUT = "Timeout"
    DRIVER = "Driver"
    PROVIDER = "Provider"
    CONNECTION_STRING = "Connection"


class SettingKey(Enum):
    NAMED_CONFIGURATION = "DBConfiguration"


class LookupUserStatuses(Enum):
    ONBOARDING = 1
    WORKING = 2
    ONLEAVE = 3
    RESIGNED = 4
    DISABLED = 5
    DELETED = 6


class SystemTokens(Enum):
    SECURITY_TOKEN = "Security"
    SESSION_TOKEN = "Session"


class LookupSecurityPolicyCategories(Enum):
    USER = 1
    PASSWORD = 2


class LookupSecurityPolicies(Enum):
    SESSION_EXPIRY_IN_MINS = 4


class LookupRoleTypes(Enum):
    COMMON = 1 
    # Internal preset role Types
    CUSTOM = 2
    # Client defined roles


class LookupServiceCategories(Enum):
    CORE = 1
    # Core services base on generic licenses
    UNIQUE = 2
    # Module specific ie: HouseKeeping, Engineering and etc
    COMMON = 3 


class HttpStatuses(Enum):
    STATUS_200 = 200
    # Standard response for successful HTTP requests
    STATUS_201 = 201
    # The request has been fulfilled, resulting in the creation of a new resource.
    STATUS_202 = 202
    # The request has been accepted for processing, but the processing has not been completed.
    STATUS_304 = 304
    # Indicates that the resource has not been modified since the version specified
    STATUS_400 = 400
    # The server cannot or will not process the request due to an apparent client error (e.g., malformed request syntax, size too large, invalid request message framing, or deceptive request routing).
    STATUS_401 = 401
    # Similar to 403 Forbidden, but specifically for use when authentication is required and has failed or has not yet been provided.
    STATUS_403 = 403
    # The request contained valid data and was understood by the server, but the server is refusing action.
    STATUS_404 = 404
    # The requested resource could not be found but may be available in the future.
    STATUS_500 = 500
    # A generic error message, given when an unexpected condition was encountered and no more specific message is suitable.
    STATUS_501 = 501 
    # The server either does not recognize the request method, or it lacks the ability to fulfil the request.
    STATUS_502 = 503
    # The server was acting as a gateway or proxy and received an invalid response from the upstream server.
    STATUS_503 = 503
    # The server cannot handle the request (because it is overloaded or down for maintenance). Generally, this is a temporary state.
    STATUS_504 = 504
    # The server was acting as a gateway or proxy and did not receive a timely response from the upstream server.


class HttpVerbs(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"

class PermissionBitwise(Enum):
    VIEW = 1
    INSERT = 2
    UPDATE = 4
    DELETE = 8
