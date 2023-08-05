from abc import ABCMeta
# Globalframework packages
from globalframework.data.setting import DatabaseSetting


class BaseConnection(metaclass=ABCMeta):

    def __init__(self, connection_param: str, connection_timeout: int):
        self.connection_param = connection_param
        self.conn = None
        self.driver = None
        self.connection_timeout = connection_timeout

    def create_connection(self):
        pass

    def execute_query(self, query: str, rds_object):
        pass

    def close_connection(self):
        """Close db driver connection"""
        self.conn.close()


class BaseQuery(metaclass=ABCMeta):
    def __init__(self):
        pass

    def process(self, query: str):
        pass
