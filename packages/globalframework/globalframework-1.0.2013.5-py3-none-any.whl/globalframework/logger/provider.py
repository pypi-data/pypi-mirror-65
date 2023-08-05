from globalframework.data.baseprovider import BaseProvider
from globalframework.caching.cache_manager import CacheManager
from globalframework.enumeration import QueryType

import functools


def check_cache(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cache_value = getattr(CacheManager(), 'read', None)(
            'gf_logging_' + func.__name__)
        if cache_value is None:
            return func(*args, **kwargs)
        return cache_value
    return wrapper


def cachemethods(cls):
    for key, value in list(vars(cls).items()):
        if '_' not in key and callable(value):
            setattr(cls, key, check_cache(value))
    return cls


@cachemethods
class LoggingProvider(BaseProvider):

    def _get_adapter_instance(self):
        self.caching = CacheManager()
        super()._get_adapter_instance()

    def get_loggername(self):
        self._get_adapter_instance()
        rows = self.dbadapter.execute_query(
            "call dbcache.p_lookuplogger_sel_loggername();", "", QueryType.SELECT)
        result = {row[0]: row[0] for row in rows}
        self.caching.store('gf_logging_get_loggername', result)
        return result

    def get_loggerattributes(self, logger_name, platform):
        self._get_adapter_instance()
        rows = self.dbadapter.execute_query(
            f"call dbcache.p_loggerattributes_sel_by_loggername_operatingsystemid('{logger_name}', {platform});", "", QueryType.SELECT)
        keys = ('FileName', 'FileLocation', 'FileNameFormat', 'FileExtension')
        values = (row[0] for row in rows)
        result = dict(zip(keys, values))
        self.caching.store('gf_logging_get_loggerattributes', result)
        return result

    def get_frequency(self, logger_name):
        self._get_adapter_instance()
        rows = self.dbadapter.execute_query(
            f"call dbcache.p_lookupfrequencies_sel_by_loggername('{logger_name}');", "", QueryType.SELECT)
        keys = ('FrequencyTypeName', 'FrequencyValue')
        result = dict(zip(keys, *rows))
        self.caching.store('gf_logging_get_frequency', result)
        return result
