# Third party libraries
import pyodbc

# Globalframework packages
from globalframework.errors import InterfaceError, DatabaseError, GFDatabaseError, exception_raiser
from globalframework.data.base import BaseConnection
from globalframework.enumeration import QueryType


class OdbcConnection(BaseConnection):

    def __init__(self, connection_param: str, connection_timeout=120):
        BaseConnection.__init__(self, connection_param, connection_timeout)

    def create_connection(self):
        """Create connection with pyodbc driver"""
        try:
            self.conn = pyodbc.connect(self.connection_param)
            # TODO : MYSQL and MSSQL work, Postgres doesn't need to figure this out @Anand
            self.conn.timeout = self.connection_timeout

        except pyodbc.DatabaseError as de:
            exception_raiser(de.args, DatabaseError, "Database General Error")

        except pyodbc.InterfaceError as ie:
            exception_raiser(ie.args, InterfaceError, "Database Interface Error")

        except pyodbc.Error as e:  
        # last in the list, catches everything above
            exception_raiser(e.args, GFDatabaseError, "Database General Error")

        except Exception as e: 
        # Catches everything
            exception_raiser(e.args, GFDatabaseError, "Database General Error")

        self.driver = pyodbc
        return self.conn

    def execute_query(self, query: str, params: str, query_type: QueryType):
        cursor = self.conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if (query_type == QueryType.INSERT or query_type == QueryType.UPDATE or query_type == QueryType.DELETE):
                self.conn.commit()

        except pyodbc.DatabaseError as de:
            exception_raiser(de.args, "Database Error")

        except pyodbc.OperationalError as oe:
            exception_raiser(oe.args, "Database Operational Error")

        except (pyodbc.InternalError, pyodbc.ProgrammingError) as ie:
            exception_raiser(ie.args, "Database Internal or Programming Error")

        except pyodbc.NotSupportedError as nse:
            exception_raiser(nse.args, "Database Not Supported Error")

        except pyodbc.DataError as dbe:
            exception_raiser(dbe.args, "General Database Error")

        return cursor
