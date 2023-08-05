# default in libraries
from typing import List, Tuple

# Globalframework packages
from globalframework.internationalisation.provider import (
    ChannelProvider, ConfigProvider, CountryProvider, LanguageProvider, MessageProvider
)
from globalframework.caching.cache_manager import CacheManager
from globalframework.constants import CACHE_KEY_CHANNEL, CACHE_KEY_CHANNEL_PATH_ID,\
    CACHE_KEY_MESSAGE_CHANNEL, CACHE_KEY_CONFIG_HIERARCHY_ALIAS, CACHE_KEY_CONFIG_HIERARCHY_CLIENT,\
    CACHE_KEY_CONFIG_HIERARCHY_APPLICATION, CACHE_KEY_CONFIG_MIME_TYPES


class ChannelManager:
    def __init__(self):
        self.cache_manager = CacheManager()
        self.channel_provider = ChannelProvider()

    def get_channels(self):
        db_records = self.channel_provider.get_channels()
        return db_records

    def get_channels_by_id(self, channel_id: int):
        records = self.cache_manager.read(CACHE_KEY_CHANNEL.format(channel_id))
        if records:
            return records
        return None

    def get_channel_path(self, channel_id: int):
        records = self.cache_manager.read(
            CACHE_KEY_CHANNEL_PATH_ID.format(channel_id))
        if records:
            return records
        else:
            db_records = self.channel_provider.get_channel_path(channel_id)

            if db_records:
                self.cache_manager.store(
                    CACHE_KEY_CHANNEL_PATH_ID.format(channel_id), db_records)
                return db_records

    def get_channels_by_name(self, channel_name: str):
        db_records = self.channel_provider.get_channels_by_name(channel_name)
        return db_records

    def get_channels_by_alias(self, channel_alias: str):
        db_records = self.channel_provider.get_channels_by_alias(channel_alias)
        return db_records

           #Get channels by parentchannelId:
           #\nArgs:parent_channel_id(int)
           #\nReturns: List of child channels


    def get_channels_by_parentchannelId(self, parent_channel_id: int):
        db_records = self.channel_provider.get_channels_by_parentchannelId(
            parent_channel_id)
        return db_records

    def get_channels_by_languageid_countryid(self, languageid: int, countryid: int):
        db_records = self.channel_provider.get_channels_by_languageid_countryid(
            languageid, countryid)
        return db_records

    def create_channel(self, param):
        status_code = 404
        status = self.channel_provider.create_channel(param)
        if status:
            status_code = 201
        return status_code

    def update_channel(self, param):
        status_code = 404
        status = self.channel_provider.update_channel_by_channelid(param)
        if status:
            status_code = 204
        return status_code

    def delete_channel(self, param):
        status_code = 404
        status = self.channel_provider.delete_channel_by_channelid(param)
        if status:
            status_code = 204
        return status_code


class ConfigManager:
    """ConfigManager class
    """

    def __init__(self):
        self.cachemanager = CacheManager()
        self.configprovider = ConfigProvider()

    def get_config(self, applicationid: int, clientid: int, configalias: str):
        """get config value

        Args:\n
            applicationid (int): application id
            clientid (int): client id
            configalias (string): config alias name

        Returns:
            Config value
        """
        configs = self.cachemanager.read("Configs")

        if configs:
            return configs[configalias]
        else:
            configs = self.configprovider.get_configs(applicationid, clientid)

            if configs:
                return configs[configalias]

    def get_configuration_hierarchy(self, config_alias, client_id=None, application_id=None):
        if config_alias and client_id and application_id:
            cache_key = CACHE_KEY_CONFIG_HIERARCHY_APPLICATION.format(
                application_id)
        elif config_alias and client_id:
            cache_key = CACHE_KEY_CONFIG_HIERARCHY_CLIENT.format(client_id)
        else:
            cache_key = CACHE_KEY_CONFIG_HIERARCHY_ALIAS.format(config_alias)

        try:
            config = self.cachemanager.read(cache_key)
            if config:
                return config
            config = self.configprovider.get_configuration_hierarchy(
                config_alias, client_id, application_id)

            if config:
                self.cachemanager.store(cache_key, config)
                return config
            raise ValueError("Data not found!")
        except KeyError:
            raise KeyError
        except Exception as e:
            raise e

    def get_mime_types(self):
        try:
            cache_key = CACHE_KEY_CONFIG_MIME_TYPES
            config = self.cachemanager.read(cache_key)
            if config:
                return config
            config = self.configprovider.get_mime_types()
            if config:
                self.cachemanager.store(cache_key, config)
                return config
            raise ValueError("Data not found")
        except KeyError:
            raise KeyError
        except Exception as e:
            raise e

    def get_clientconfigs_by_clientid_configalias(self, client_id: int, config_alias: str):
        cache_key = f'get_clientconfigs_by_clientid_{client_id}_{config_alias}'
        records = self.cachemanager.read(cache_key)
        if records:
            return records
        else:
            dbrecords = self.configprovider.get_clientconfigs_by_clientid_configalias(client_id, config_alias)
        if dbrecords:
            self.cachemanager.store(cache_key, dbrecords)
            return dbrecords
        else:
            return None

    def get_default_clientconfigs_by_configalias(self, config_alias: str):
        cache_key = f'get_default_clientconfigs_by_configalias_{config_alias}'
        records = self.cachemanager.read(cache_key)
        if records:
            return records
        else:
            dbrecords = self.configprovider.get_default_clientconfigs_by_configalias(config_alias)
        if dbrecords:
            self.cachemanager.store(cache_key, dbrecords)
            return dbrecords
        else:
            return None

class CountryManager:
    def __init__(self):
        self.country_provider = CountryProvider()

    def get_countries(self):
        db_records = self.country_provider.get_countries()
        return db_records


class LanguageManager:
    def __init__(self):
        self.language_provider = LanguageProvider()

    def get_languages(self):
        db_records = self.language_provider.get_languages()
        return db_records


class MessageManager:
    """MessageManager class
    """

    def __init__(self):
        self.cachemanager = CacheManager()
        self.messageprovider = MessageProvider()

    def get_message(self, channelid: int, clientid: int, messageid):
        """Get translated message

        Args:\n
            channelid (int): Channel Id
            clientid (int): Client Id
            messageid (int): Message Id

        Returns:
            Translated message
        """
        records = self.cachemanager.read(
            CACHE_KEY_MESSAGE_CHANNEL.format(channelid))

        if records:
            return records[messageid]
        else:
            dbrecords = self.messageprovider.get_messages(channelid, clientid)

            if dbrecords:
                self.cachemanager.store(
                    CACHE_KEY_MESSAGE_CHANNEL.format(channelid), dbrecords)

                return dbrecords[messageid]

    def get_messages_by_channelid(self, channelid: int, messageid):
        """Get translated message

        Args:\n
            channelid (int): Channel Id
            clientid (int): Client Id
            messageid (int): Message Id

        Returns:
            Translated message
        """
        records = self.cachemanager.read(
            CACHE_KEY_MESSAGE_CHANNEL.format(channelid))

        msg = None
        if records is not None:
            msg = records[messageid]

        if msg is None:
            dbrecords = self.messageprovider.get_messages_by_channelid(
                channelid)

            if dbrecords:
                self.cachemanager.store(
                    CACHE_KEY_MESSAGE_CHANNEL.format(channelid), dbrecords)

                return dbrecords[messageid]

        return msg

    def get_messages_by_channelid_messageids(self, channelid: int, messageids: List[int]):
        records = self.cachemanager.read(
            CACHE_KEY_MESSAGE_CHANNEL.format(channelid))

        # If not cached, get from db
        if not records:
            records = self.messageprovider.get_messages_by_channelid_messageids(
                channelid, messageids)
            records = self._process_messages_from_provider(records)
            self.cachemanager.store(
                CACHE_KEY_MESSAGE_CHANNEL.format(channelid), records)
        else:
            # Query ids that are not in the cache and update the cache
            missing_messageids = self._get_list_dff(
                list(records.keys()), messageids)

            if missing_messageids:
                new_records = self.messageprovider.get_messages_by_channelid_messageids(
                    channelid, missing_messageids)
                new_records = self._process_messages_from_provider(new_records)
                records = {**records, **new_records}
            self.cachemanager.store(
                CACHE_KEY_MESSAGE_CHANNEL.format(channelid), records)

        return records

    def get_messages_by_channelid_clientid_messageids(self, channelid: int, clientid: int, messageids: List[int]):
        records = self.cachemanager.read(
            CACHE_KEY_MESSAGE_CHANNEL.format(channelid))

        # If not cached, get from db
        if not records:
            records = self.messageprovider.get_messages_by_channelid_clientid_messageids(
                channelid, clientid, messageids)
            records = self._process_messages_from_provider(records)
            self.cachemanager.store(
                CACHE_KEY_MESSAGE_CHANNEL.format(channelid), records)
        else:
            # Query ids that are not in the cache and update the cache
            missing_messageids = self._get_list_dff(
                list(records.keys()), messageids)

            if missing_messageids:
                new_records = self.messageprovider.get_messages_by_channelid_clientid_messageids(
                    channelid, clientid, missing_messageids)
                new_records = self._process_messages_from_provider(new_records)
                records = {**records, **new_records}
            self.cachemanager.store(
                CACHE_KEY_MESSAGE_CHANNEL.format(channelid), records)

        return records

    def get_messages_by_clientid(self, clientid: int):
        records = self.messageprovider.get_messages_by_clientid(clientid)
        return records

    def insert_messages(self, message_category_id, user_id):
        records = self.messageprovider.insert_messages(
            message_category_id, user_id)
        return records

    def insert_messagecategories(self, message_category_name, message_category_description, user_id):
        records = self.messageprovider.insert_messagecategories(
            message_category_name, message_category_description, user_id)
        return records

    def insert_messagetranslations_with_clientid(self, message_id, message_copy, channel_id, client_id, user_id):
        records = self.messageprovider.insert_messagetranslations_with_clientid(
            message_id, message_copy, channel_id, client_id, user_id)
        return records

    def update_messagetranslations_all_by_messagetranslationid(self, channel_id, message_copy, client_id, message_translation_id, user_id):
        records = self.messageprovider.update_messagetranslations_all_by_messagetranslationid(
            channel_id, message_copy, client_id, message_translation_id, user_id)
        return records

    def update_messagetranslations_min_by_messagetranslationid(self, channel_id, message_copy, message_translation_id, user_id):
        records = self.messageprovider.update_messagetranslations_min_by_messagetranslationid(
            channel_id, message_copy, message_translation_id, user_id)
        return records

    def update_messages_messagecategoryid_by_messageid(self, message_category_id, message_id, user_id):
        records = self.messageprovider.update_messages_messagecategoryid_by_messageid(
            self, message_category_id, message_id, user_id)
        return records

    def _process_messages_from_provider(self, messages: List[Tuple]):
        messages = sorted(messages, key=lambda x: x[2])
        messages = self._messages_tuples_to_dict(messages)
        return messages

    def _messages_tuples_to_dict(self, messages):
        records = {}

        for i in messages:
            records[i[0]] = i[1]

        return records

    def _get_list_dff(self, original: List, target: List) -> List:
        return list(set(target) - set(original))
