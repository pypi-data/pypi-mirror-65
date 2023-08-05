"""
     DO NOT USE, use blacklistmessagemanager instead
    Retrives blacklist messages from database
"""

from globalframework.data.baseprovider import BaseProvider
from globalframework.enumeration import QueryType


class BlacklistMessageProvider(BaseProvider):
    def get_blacklistmessages_by_channelid(self, channel_id: int):
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_messageblacklist_sel_by_channelid({channel_id});", "", QueryType.SELECT)
        return self.dbadapter.map_data_rows(cursor)
