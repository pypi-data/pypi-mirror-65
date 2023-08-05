# default libraries
import ast

# Third party libraries
import psycopg2

# Globalframework packages
from globalframework.errors import InterfaceError, DatabaseError, GFDatabaseError, exception_raiser
from globalframework.data.base import BaseConnection
from globalframework.enumeration import QueryType


class PsycopgConnection(BaseConnection):

    def __init__(self, connection_param: str, connection_timeout=120):
        BaseConnection.__init__(self, connection_param, connection_timeout)

    def create_connection(self):
        """Create connection with psycopy2 driver"""
        args = ast.literal_eval(self.connection_param)

        auser = args['user']
        apassword = args['password']
        ahost = args['host']
        aport = args['port']
        adatabase = args['database']
        atimeout = self.connection_timeout

        try:
            self.conn = psycopg2.connect(host=ahost, port=aport, database=adatabase, user=auser, password=apassword, connect_timeout=atimeout)

        except psycopg2.DatabaseError as de:
            exception_raiser(de.args, DatabaseError, "Database General Error")

        except psycopg2.InterfaceError as ie:
            exception_raiser(ie.args, InterfaceError,
                             "Database Interface Error")

        except psycopg2.Error as e:
        # last in the list, catches everything above
            exception_raiser(e.args, GFDatabaseError, "Database General Error")

        except Exception as e:
        # Catches everything
            exception_raiser(e.args, GFDatabaseError, "Database General Error")

        self.driver = psycopg2
        return self.conn

    def execute_query(self, query: str, params: str, query_type: QueryType):
        cursor = self.conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if (query_type == QueryType.INSERT or  query_type == QueryType.UPDATE or query_type == QueryType.DELETE):
                self.conn.commit()

        except psycopg2.DatabaseError as de:
            exception_raiser(de.args, "Database Error")

        except psycopg2.OperationalError as oe:
            exception_raiser(oe.args, "Database Operational Error")

        except psycopg2.InternalError as ie:
            exception_raiser(ie.args, "Database Internal or Programming Error")

        except psycopg2.NotSupportedError as nse:
            exception_raiser(nse.args, "Database Not Supported Error")

        except psycopg2.DataError as dbe:
            exception_raiser(dbe.args, "General Database Error")

        return cursor
