"""
    This is a blacklist message module,
    retrieve filter from cache, or database
"""
# Globalframework packages
import re
from globalframework.filter.provider import BlacklistMessageProvider
from globalframework.caching.cache_manager import CacheManager



class BlacklistMessageManager:
    """MessageManager class
    """

    def __init__(self):
        self.cachemanager = CacheManager()
        self.blacklistmessageprovider = BlacklistMessageProvider()


    def get_blacklistmessages(self, channelid: int):
        cache_key = 'get_blacklistmessages_{}'.format(channelid)
        records = self.cachemanager.read(cache_key)
        if records:
            return records
        else:
            dbrecords = self.blacklistmessageprovider.get_blacklistmessages_by_channelid(channelid)

            if dbrecords:
                self.cachemanager.store(cache_key, dbrecords)

                return dbrecords

    # take a string and a list of strings, filter out list of strings from string
    @staticmethod
    def filter(message, blacklistmessages):
        for i in blacklistmessages:
            i = i['Message']
            pattern = re.compile(i, re.IGNORECASE)
            message = pattern.sub(len(i) * '*', message)
        # If the entire message is censored, throw empty message back
        if message.replace(' ', '') == len(message.replace(' ', '')) * '*':
            message = ''

        return message
