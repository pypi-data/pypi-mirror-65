
'''
With assumption that a set of dictionaries will be cached into memory

Sample data
mydict = {
    "Messages" : {
        1 : "test",
        2 : "test2"
    },
    "Configs" : {
        "Config_1_On" : True,
        "Config_2_On" : False
    }
}
'''
__all__ = []
__version__ = '0.0.1'
__author__ = 'Anand'

# Third party libraries
from pymemcache.client.base import Client
from pymemcache import serde

# globalframework Libraries
from globalframework.data.setting import CacheSetting
from globalframework.logger.log import Logger

class CacheManager:
    def __init__(self, cache_conn_setting=''):
        self.cache_conn_setting = cache_conn_setting

    def __get_cache_instance(self):
        cacheprovider = CacheProvider(self.cache_conn_setting)
        cpc = cacheprovider.get_connection()
        return Client((cpc.ipaddress, int(cpc.ports)),
                      serializer=serde.python_memcache_serializer,
                      deserializer=serde.python_memcache_deserializer,
                      connect_timeout=cpc.connection_timeout,
                      timeout=cpc.timeout)

    def read(self, cachekey):
        mc = self.__get_cache_instance()
        return mc.get(cachekey)

    def store(self, cachekey, value):
        mc = self.__get_cache_instance()
        mc.set(cachekey, value)


class CacheProvider:
    def __init__(self, cache_conn_setting=''):
        self.cache_conn_setting = cache_conn_setting

    def get_connection(self):
        cachesetting = CacheSetting(self.cache_conn_setting)
        return cachesetting.get_cache_connection()
