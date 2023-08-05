"""
    Files
"""
CONFIG_FILE_SEARCH_PATH = "ConfigurationSearchPath.json"
ENV_FILE_SEARCH_PATH = "appconfig.json"
DEV_ENV_FILE_SEARCH_PATH = "dev.appconfig.json"
QA_ENV_FILE_SEARCH_PATH = "qa.appconfig.json"
PROD_ENV_FILE_SEARCH_PATH = "prod.appconfig.json"

"""
    Files keys
"""
PORT = "port"
DEBUG = "debug"

"""
    Cache keys
"""
CACHE_KEY_MESSAGE_CHANNEL = "MESSAGE_{0}"
CACHE_KEY_CHANNEL = "CHANNEL_{0}"
CACHE_KEY_CHANNEL_PATH_ID = "CHANNEL_PATH_{0}"
CACHE_KEY_CONFIG_HIERARCHY_ALIAS = "CONFIG_HIERARCHY_ALIAS_{!r}"
CACHE_KEY_CONFIG_HIERARCHY_CLIENT = "CONFIG_HIERARCHY_CLIENT_{!r}"
CACHE_KEY_CONFIG_HIERARCHY_APPLICATION = "CONFIG_HIERARCHY_APPLICATION_{!r}"
CACHE_KEY_CONFIG_MIME_TYPES = "CONFIG_MIME_TYPES"

"""
    REST API params
"""
CHANNEL_CHANNEL_ID = "channel_id"
CHANNEL_USER_ID = "user_id"
MCCS_APP_ID = "ApplicationID"
MCCS_PASSCODE = "AccessCode"
MCCS_DEVICE_ID = "DeviceID"
MCCS_USER_ID = "user_id"
MCCS_ROLE_ID = "role_id"
MCCS_NO_CONFIG = '{"config":{}}'
MCCS_ERROR = "errors"
API_STATUS_CODE = "statuscode"

"""
    DATABASE REQUEST TYPES
"""
REQUEST_SELECT = "select"
REQUEST_INSERT = "insert"
REQUEST_DELETE = "delete"
REQUEST_UPDATE = "update"

"""
    TABLE Name params
"""
FROM_ROLE_PERMISSIONS = "rolepermissions"
FROM_USER_PERMISSIONS = "userpermissions"
FROM_ROLES = "roles"
