# default in libraries
import os
import json
from shutil import copyfile


# Globalframework packages
from globalframework.errors import DataConfigurationError, format_warning_msg, format_exception_msg
from globalframework.enumeration import ConfigurationTypes, OperatingSystemTypes, LoggerType, SettingKey
from globalframework.constants import CONFIG_FILE_SEARCH_PATH
from globalframework.logger.log import Logger
from globalframework.data.modal import (
    DatabaseConfiguration, CacheConfiguration, EnvironmentConfiguration
)


#region FileUtils
class Setting:

    def __init__(self):
        pass

    def check_file_exist(self, path: str):
        """Check if file exist"""
        return os.path.isfile(path)

    def load_file_content(self, path: str):
        """Load file into stream"""
        with open(path) as sf:
            content = sf.read()
            return content

    def load_file_content_byte(self, path: str):
        """Load file into stream as bytes"""
        with open(path, 'rb') as rab:
            content = rab.read()
            return content

    def load_jsonfile_content(self, path: str):
        """Load json file into a dictionary"""
        with open(path, 'r') as jsf:
            json_content = json.load(jsf)
            return json_content

    def write_file(self, path: str, content: str):
        """Write to file"""
        with open(path) as f:
            f.write(content)

    def write_file_byte(self, path: str, content: bytes):
        """write content as byte to file"""
        with open(path, 'wb') as f:
            f.write(content)

    def copy_file(self, path: str, target: str):
        """copy path and rename copied to target"""
        copyfile(path, target)

    def rename_file(self, file: str, new_name):
        """Rename a given file"""
        filepath = os.path.dirname(os.path.abspath(file))
        newfilename = os.path.basename(file)
        new_file_name = filepath + new_name + newfilename
        return new_file_name

    def delete_file(self, path: str):
        """Delete specified file"""
        os.remove(path)

    def decrypt_setting(self):
        """"""
        raise NotImplementedError

#endregion FileUtils

#region Settings


class Configurations():
    def __init__(self):
        pass

    def _load_configuration_search_path(self):
        setting = Setting()
        config_search_path = os.path.dirname(os.path.realpath(__file__))
        env = EnvironmentConfiguration()
        curr_op = env.get_operating_system()
        diresc = "\\"
        if curr_op == OperatingSystemTypes.LINUX.name:
            diresc = "/"

        config_search_path = config_search_path + diresc + CONFIG_FILE_SEARCH_PATH

        if setting.check_file_exist(config_search_path):
            search_paths = setting.load_jsonfile_content(config_search_path)
            for dirloc in search_paths:
                child = search_paths[dirloc]
                if child['Location'] == None:
                    # figure out the relative path
                    # TODO : Anand come back to this if needed
                    pass
                if child['Location']:
                    config_file = child['Location'] + child['Filename']
                    if setting.check_file_exist(config_file):
                        return config_file

        raise DataConfigurationError("Unable to determine search path")

    def load_configurations(self, request: str):
        setting = Setting()
        configuration_file_path = self._load_configuration_search_path()
        if setting.check_file_exist(configuration_file_path):
            configs = setting.load_jsonfile_content(configuration_file_path)
            if configs != None:
                requested_configuration = configs[request]
                return requested_configuration

        raise DataConfigurationError("Unable to load configurations")


class DatabaseSetting(Setting):
    def __init__(self, db_conn_setting="", **kwargs):
        self.db_conn_setting = ""
        self.database_configuration = ConfigurationTypes.APPLICATION_DATABASE.value

        if SettingKey.NAMED_CONFIGURATION.value in kwargs:
            self.database_configuration = kwargs.get(
                SettingKey.NAMED_CONFIGURATION.value)

        if db_conn_setting != "":
            try:
                self.db_conn_setting = json.loads(db_conn_setting)[
                    self.database_configuration]
            except Exception as e:
                msg = format_exception_msg(
                    e, "Unable to extract database configuration")
                logger = Logger()
                logger.write(msg.log_msg, msg.msg_type, msg.guid)
                raise DataConfigurationError(msg.user_msg)

    def get_database_connection(self):
        """Get Db connection details"""
        if self.db_conn_setting == "":
            # Search in default location for the connection files
            configuration = Configurations()
            self.db_conn_setting = configuration.load_configurations(
                self.database_configuration)

        if self.db_conn_setting is not None:
            dc = DatabaseConfiguration(
                self.db_conn_setting["Connection"],
                self.db_conn_setting["Timeout"],
                self.db_conn_setting["Driver"],
                self.db_conn_setting["Provider"],
            )
            return dc
        msg = format_exception_msg("Database configuration missing")
        logger = Logger()
        logger.write(msg.log_msg, msg.msg_type, msg.guid)
        raise DataConfigurationError(msg.user_msg)


class CacheSetting(Setting):
    def __init__(self, cache_conn_setting=''):
        self.cache_conn_setting = ''
        self.logger = Logger(LoggerType.FCSGLOBALFRAMEWORK.name)
        if cache_conn_setting != '':
            try:
                self.cache_conn_setting = json.loads(
                    cache_conn_setting)["Caching"]
            except Exception as e:
                msg = format_exception_msg(
                    e, "Unable to extract caching configuration")
                self.logger.write(
                    msg.log_msg, msg.msg_type.WARNING.name, msg.guid)

    def get_cache_connection(self):
        """Get cache connection details"""
        if self.cache_conn_setting == '':
            configuration = Configurations()
            self.cache_conn_setting = configuration.load_configurations(
                ConfigurationTypes.CACHING.value)

        if self.cache_conn_setting is not None:
            # Search in default location for the connection files
            cc = CacheConfiguration(self.cache_conn_setting["Provider"],
                                    self.cache_conn_setting["IpAddress"],
                                    self.cache_conn_setting["Ports"],
                                    self.cache_conn_setting["ConnectTimeout"],
                                    self.cache_conn_setting["Timeout"])
            return cc

        msg = format_warning_msg("Caching configuration missing")
        self.logger.write(msg.log_msg, msg.msg_type.WARNING.name, msg.guid)


class EmailSetting(Setting):
    def __init__(self, email_conn_setting=''):
        self.email_conn_setting = ''
        self.logger = Logger(LoggerType.FCSGLOBALFRAMEWORK.name)
        if email_conn_setting != '':
            try:
                self.email_conn_setting = json.loads(
                    email_conn_setting)["EmailSetting"]
            except Exception as e:
                msg = format_exception_msg(
                    e, "Unable to extract caching configuration")
                self.logger.write(
                    msg.log_msg, msg.msg_type.WARNING.name, msg.guid)

    def get_email_connection(self):
        """Get cache connection details"""
        if self.email_conn_setting == '':
            configuration = Configurations()
            self.email_conn_setting = configuration.load_configurations(
                ConfigurationTypes.EMAIL.value)

        if self.email_conn_setting is not None:
            # Search in default location for the connection files
            return self.email_conn_setting

        msg = format_warning_msg("Email configuration missing")
        self.logger.write(msg.log_msg, msg.msg_type.WARNING.name, msg.guid)


class QueueSetting(Setting):
    def __init__(self, queue_conn_setting=''):
        self.queue_conn_setting = ''
        self.logger = Logger(LoggerType.FCSGLOBALFRAMEWORK.name)
        if queue_conn_setting != '':
            try:
                self.queue_conn_setting = json.loads(
                    queue_conn_setting)["QueueSetting"]
            except Exception as e:
                msg = format_exception_msg(
                    e, "Unable to extract queue configuration")
                self.logger.write(
                    msg.log_msg, msg.msg_type.WARNING.name, msg.guid)

    def get_queue_connection(self):
        """Get queue connection details"""
        if self.queue_conn_setting == '':
            configuration = Configurations()
            self.queue_conn_setting = configuration.load_configurations(
                ConfigurationTypes.QUEUE.value)

        if self.queue_conn_setting is not None:
            # Search in default location for the connection files
            return self.queue_conn_setting

        msg = format_warning_msg("Queue configuration missing")
        self.logger.write(msg.log_msg, msg.msg_type.WARNING.name, msg.guid)


class EnvironmentSetting():
    def __init__(self):
        # TODO
        pass
    


class CloudSetting():
    def __init__(self):
        # TODO
        pass
    


class HashSetting(Setting):
    def __init__(self, hash_conn_setting=''):
        self.hash_conn_setting = ''
        self.logger = Logger(LoggerType.FCSGLOBALFRAMEWORK.name)
        if hash_conn_setting != '':
            try:
                self.hash_conn_setting = json.loads(
                    hash_conn_setting)["HashSetting"]
            except Exception as e:
                msg = format_exception_msg(
                    e, "Unable to extract hash configuration")
                self.logger.write(
                    msg.log_msg, msg.msg_type.WARNING.name, msg.guid)

    def get_hash_connection(self):
        """Get hash connection details"""
        if self.hash_conn_setting == '':
            configuration = Configurations()
            self.hash_conn_setting = configuration.load_configurations(
                ConfigurationTypes.HASH.value)

        if self.hash_conn_setting is not None:
            # Search in default location for the connection files
            return self.hash_conn_setting

        msg = format_warning_msg("Hash configuration missing")
        self.logger.write(msg.log_msg, msg.msg_type.WARNING.name, msg.guid)

#endregion Settings
