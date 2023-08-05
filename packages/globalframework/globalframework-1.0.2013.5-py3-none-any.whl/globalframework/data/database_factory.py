# Default packages
from typing import List, Tuple

# Globalframework packages
from globalframework.enumeration import QueryType, DatabaseConnectionArgs, SettingKey
from globalframework.data.setting import DatabaseSetting
from globalframework.data.odbc_connection import OdbcConnection
from globalframework.data.psycopg_connection import PsycopgConnection
from globalframework.data.query import MysqlQuery, MssqlQuery, PostgreQuery
from globalframework.enumeration import DatabaseTypes


class DatabaseFactory():
    """DatabaseFactory [abstract layer to handle database connection]"""

    def __init__(self, **kwargs):
        self.connection_string = None
        self.driver_object = None
        self.rdms_object = None
        self.conn = None

        if DatabaseConnectionArgs.CONNECTION_STRING.value in kwargs:
            self.connection_string = kwargs.get(
                DatabaseConnectionArgs.CONNECTION_STRING.value)

        if DatabaseConnectionArgs.DRIVER.value in kwargs:
            self.driver = kwargs.get(
                DatabaseConnectionArgs.DRIVER.value).capitalize()

        if DatabaseConnectionArgs.PROVIDER.value in kwargs:
            self.provider = kwargs.get(
                DatabaseConnectionArgs.PROVIDER.value).capitalize()

        if self.connection_string == None:
            databaseSetting = None

            if SettingKey.NAMED_CONFIGURATION.value in kwargs:
                databaseSetting = DatabaseSetting("", DBConfiguration = kwargs.get(SettingKey.NAMED_CONFIGURATION.value))
            else:
                databaseSetting = DatabaseSetting()

            database_configuration = databaseSetting.get_database_connection()
            self.connection_string = database_configuration.connection
            self.driver = database_configuration.driver.capitalize()
            self.provider = database_configuration.rdmsprovider.capitalize()

    def create_connection(self):
        """To create connection"""
        self.driver_object = eval(
            self.driver + "Connection")(self.connection_string)
        self.conn = self.driver_object.create_connection()

    def execute_query(self, query: str, params: str, query_type: QueryType):
        # abstract factory method is require to the right approach the proc calls.
        self.rdms_object = eval(self.provider + "Query")()
        updated_query = self.rdms_object.process(query, query_type)

        # returns executed cursor
        return self.driver_object.execute_query(updated_query, params, query_type)

    def close_connection(self):
        """To close connection"""
        self.driver_object.close_connection()                     

# region data processing
    def map_data(self, cursor, columns=[]):
        if cursor:
            if not columns:
                columns = [column[0] for column in cursor.description]
            row = cursor.fetchone()
            data = []
            if row and len(row) > 0:
                data = dict(zip(columns, row))
                return data
        return None

    def map_data_rows(self, cursor, columns=[]):
        if cursor:
            if not columns:
                columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            data = []
            for row in rows:
                data.append(dict(zip(columns, row)))

            if data == []:
                return None
            return data
        return None

    def map_data_tuples(self, cursor) -> List[Tuple]:
        value = None
        if cursor:
            value = [tuple(row) for row in cursor]
            if value == []:
                return None
        return value

    def map_none_query(self, cursor):
        if cursor:
            return True
        return False
# endregion

    # Method to format list to string which can be parsed by mysql stored proc
    def format_list_to_strings(self, list_i):
        value = None

        if self.provider == DatabaseTypes.MYSQL.value:
            value = f"\'{','.join(map(str, list_i))}\'"
        elif self.provider == DatabaseTypes.POSTGRES.value:
            value = f'ARRAY{list_i}'

        return value
