from globalframework.data.database_factory import DatabaseFactory

class BaseProvider:
    def __init__(self):
        self.dbadapter = None

    def _get_adapter_instance(self, **kwargs):
        self.dbadapter = DatabaseFactory(**kwargs)
        self.dbadapter.create_connection()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.dbadapter.close_connection()
