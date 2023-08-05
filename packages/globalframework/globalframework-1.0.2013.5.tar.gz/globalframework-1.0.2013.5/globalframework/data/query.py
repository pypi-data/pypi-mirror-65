from globalframework.data.base import BaseQuery
from globalframework.enumeration import QueryType


class MysqlQuery(BaseQuery):
    def __init__(self):
        pass

    def process(self, query: str, query_type: QueryType):
        query = str(query).replace("{", "")
        query = str(query).replace("}", "")
        return query


class MssqlQuery(BaseQuery):
    def __init__(self):
        pass

    def process(self, query: str, query_type: QueryType):
        query = str(query).replace("{", "")
        query = str(query).replace("}", "")
        query = str(query).replace("call ".lower(), "exec ")
        query = str(query).replace("call ".upper(), "exec ")
        query = str(query).replace("call ".capitalize(), "exec ")
        query = str(query).replace("(", " ")
        query = str(query).replace(")", " ")
        return query


class PostgreQuery(BaseQuery):
    def __init__(self):
        pass

    def process(self, query: str, query_type: QueryType):
        if(query_type == QueryType.SELECT):
            query = str(query).replace("call ".lower(), "SELECT * FROM ")
            query = str(query).replace("call ".upper(), "SELECT * FROM ")
            query = str(query).replace("call ".capitalize(), "SELECT * FROM ")
        return query
