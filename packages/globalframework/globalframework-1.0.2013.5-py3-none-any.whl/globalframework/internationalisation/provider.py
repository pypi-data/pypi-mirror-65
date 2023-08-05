# default in libraries
from typing import List

# Globalframework packages
from globalframework.data.baseprovider import BaseProvider
from globalframework.enumeration import PathCol, ConfiCol
from globalframework.enumeration import QueryType


class ChannelProvider(BaseProvider):

    def get_channels(self):
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_channels_sel();", "", QueryType.SELECT)
        return self.dbadapter.map_data_tuples(cursor)


    def get_channels_by_id(self, channel_id: int):
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_channels_sel_by_channelid('{channel_id}');", "", QueryType.SELECT)
        return self.dbadapter.map_data_tuples(cursor)


    def get_channel_path(self, channel_id: int):
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_channels_get_path_by_channelid('{channel_id}');", "", QueryType.SELECT)
        return self.dbadapter.map_data_tuples(cursor)


    def get_channels_by_name(self, channel_name: str):
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_channels_sel_by_channelname('{channel_name}');", "", QueryType.SELECT)
        return self.dbadapter.map_data_tuples(cursor)


    def get_channels_by_alias(self, channel_alias: str):
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_channels_sel_by_channelalias('{channel_alias}');", "", QueryType.SELECT)
        return self.dbadapter.map_data_tuples(cursor)


    def get_channels_by_parentchannelId(self, parent_channel_id: int):
        """Get channels by parentchannelId:
           \nArgs:parent_channel_id(int)
           \nReturns: List of child channels
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_channels_sel_by_parentchannelid('{parent_channel_id}');", "", QueryType.SELECT)
        return self.dbadapter.map_data_tuples(cursor)


    def get_channels_by_languageid_countryid(self, languageid: int, countryid: int):
        self._get_adapter_instance()
        if not countryid:
            countryid = 'NULL'
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_channels_sel_by_languageid_countryid({languageid},{countryid});", "", QueryType.SELECT)
        return self.dbadapter.map_data_tuples(cursor)

     # region INSERT
    def create_channel(self, param):
        self._get_adapter_instance()
        values = tuple(param.values())
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_channels_ins{values};", "", QueryType.INSERT)
        return self.dbadapter.map_none_query(cursor)

    # endregion INSERT

    # region UPDATE

    def update_channel_by_channelid(self, param):
        """Updates channel details using channel ID and logs operation in channelhistory:
           \nArgs: channel_id (int): Channel ID, channel_name (str): Channel Name, channel_desc (str): Channel Description, parent_channel_id (int): Parent Channel ID, language_id (int): Language ID, country_id (int): Country ID, channel_alias (str): Channel Alias, user_id (int): User ID
           \nReturns: 1 if successful or 0 if failed
        """
        # TODO : NXG-381
        self._get_adapter_instance()
        values = tuple(param.values())
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_channels_upd_by_channelid{values};", "", QueryType.UPDATE)
        return self.dbadapter.map_none_query(cursor)

    # endregion UPDATE

    # region DELETE

    def delete_channel_by_channelid(self, param):
        """Deletes channel using channel ID and logs operation into channelhistory table:
             \nArgs: channel_id (int): ChannelID, user_id (int): User ID, action_status (str): ActionStatus
             \nReturns: 1 if successful or 0 if failed
        """
        # TODO : NXG-381
        self._get_adapter_instance()
        values = tuple(param.values())
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_channels_del_by_channelid{values};", "", QueryType.DELETE)
        return self.dbadapter.map_none_query(cursor)

    # endregion DELETE

    def verify_channel_exist(self, id):
        return self.get_channels_by_id(id) != []


    def construct_channel_history(self, action, id, userid):
        history = (action, id, userid)
        return history


class ConfigProvider(BaseProvider):
    """ ChannelConfig class that handle config value retrieval
    """

    def __init__(self):
        self._get_adapter_instance()

    def get_configs(self, applicationid: int, clientid: int):
        """get_configs [function to retrieve config value]

        Args:\n
            applicationid (int): [application id - to make code more readable, can use AppTypes enum]
            clientid (int): [client id]

        Returns:
            Dictionary of configs
        """
        configs = {}

        # get client path
        client_path = self._get_client_organisation_path(clientid)

        # get default configs
        default_configs = self._get_default_configs()

        if default_configs:
            for config in default_configs:
                configs[config[ConfiCol.CONFIG_ALIAS.value]
                        ] = config[ConfiCol.CONFIG_VALUE.value]

        # get client configs
        for client in client_path:
            client_configs = self._get_client_configs(
                applicationid, client[PathCol.CLIENT_ID.value])

            for config in client_configs:
                configs[config[ConfiCol.CONFIG_ALIAS.value]
                        ] = config[ConfiCol.CONFIG_VALUE.value]

        return configs

    # region private methods
    def _get_client_organisation_path(self, clientid: int):
        """_get_client_organisation_path [function to get client organisation path]

        Args:
            clientid (int): [client id]

        Returns:
            client organisation path
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_organisationhierarchy_sel_path_by_clientid({clientid});", "", QueryType.SELECT)
        return cursor

    def _get_default_configs(self):
        """_get_default_configs [function to get default configs]

        Returns:
            default configs
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_clientconfigs_sel_default();", "", QueryType.SELECT)
        return self.dbadapter.map_data_rows(cursor)

    def _get_client_configs(self, applicationid: int, clientid: int):
        """_get_client_configs [function to get client configs by application id]

        Args:
            applicationid (int): [application id]
            clientid (int): [client id]

        Returns:
            client configs
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_clientconfigs_sel_by_applicationid_clientid(?,?);", (applicationid, clientid), QueryType.SELECT)
        return cursor
    # endregion

    def get_configuration_hierarchy(self, config_alias, client_id=None, application_id=None):
        if config_alias and client_id and application_id:
            cursor_obj = self.dbadapter.execute_query(
                f"call dbcache.p_lookuporganisationhierarchy_sel_by_configalias_client_app('{config_alias}', '{client_id}', '{application_id}');", None, QueryType.SELECT
            )
        elif config_alias and client_id:
            cursor_obj = self.dbadapter.execute_query(
                f"call dbcache.p_lookuporganisationhierarchy_sel_by_configalias_client('{config_alias}', '{client_id}');", None, QueryType.SELECT
            )
        elif config_alias:
            cursor_obj = self.dbadapter.execute_query(
                f"call dbcache.p_lookuporganisationhierarchy_sel_by_configalias('{config_alias}');", None, QueryType.SELECT
            )
        columns = [column[0] for column in cursor_obj.description]
        return [dict(zip(columns, row)) for row in cursor_obj]

    def get_mime_types(self):
        cursor_obj = self.dbadapter.execute_query(
            f"call dbcache.p_lookupmimetypes_sel();", None, QueryType.SELECT
        )
        columns = [column[0] for column in cursor_obj.description]
        return [dict(zip(columns, row)) for row in cursor_obj]

    def get_clientconfigs_by_clientid_configalias(self, client_id: int, config_alias: str):
        """Gets Client Overwrite Clientconfigs based on ClientID and config_alias"""
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_clientconfigs_sel_by_clientid_configalias({client_id}, '{config_alias}');", "", QueryType.SELECT)
        return self.dbadapter.map_data(cursor)

    def get_default_clientconfigs_by_configalias(self, config_alias: str):
        """Gets default client configs where ClientID is null."""
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_clientconfigs_sel_by_configalias('{config_alias}');", "", QueryType.SELECT)
        return self.dbadapter.map_data(cursor)

    # region INSERT
    def insert_clientconfigs(self, config_value: str, application_id: int, config_id: int, client_id: int, user_id: int):
        """Inserts new client configuration details:
           \nArgs: config_value (str), application_id (int), config_id (int), client_id (int), user_id (int)
           \nReturns: 1 if successful or 0 if failed
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_clientconfigs_ins('{config_value}', {application_id}, {config_id}, {client_id}, {user_id});", "", QueryType.INSERT)
        return self.dbadapter.map_none_query(cursor)

    def insert_lookupconfigurations(self, config_alias: str, config_desc: str, user_id: int):
        """Inserts new lookupconfiguration details:
           \nArgs: config_alias (str), config_desc (str), user_id (int)
           \nReturns: 1 if successful or 0 if failed
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_lookupconfigurations_ins('{config_alias}', '{config_desc}', {user_id});", "", QueryType.INSERT)
        return self.dbadapter.map_none_query(cursor)

    def insert_organisationhierarchy(self, client_id: int, parent_client_id: int, client_level: int, user_id: int):
        """Inserts new organisationhierarchy details:
           \nArgs: client_id (int), parent_client_id (int), client_level (int), user_id (int)
           \nReturns: 1 if successful or 0 if failed
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_organisationhierarchy_ins({client_id}, {parent_client_id}, {client_level}, {user_id});", "", QueryType.INSERT)
        return self.dbadapter.map_none_query(cursor)

    # endregion INSERT

    # region UPDATE
    def update_clientconfigs_configvalue_by_clientconfigid(self, clientconfig_id: int, configvalue: str, user_id: int):
        """Updates clientconfigs Config Value by clientconfigId:
           \nArgs: clientconfig_id (int), configvalue (str), user_id (int)
           \nReturns: 1 if successful or 0 if failed
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_clientconfigs_upd_configvalue_by_clientconfigid({clientconfig_id}, '{configvalue}', {user_id});", "", QueryType.UPDATE)
        return self.dbadapter.map_none_query(cursor)

    def update_clientconfigs_applicationid_by_clientconfigid(self, clientconfig_id: int, application_id: int, user_id: int):
        """Updates clientconfigs Application ID by clientconfigId:
           \nArgs: clientconfig_id (int), application_id (int), user_id (int)
           \nReturns: 1 if successful or 0 if failed
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_clientconfigs_upd_applicationid_by_clientconfigid({clientconfig_id}, {application_id}, {user_id});", "", QueryType.UPDATE)
        return self.dbadapter.map_none_query(cursor)

    def update_clientconfigs_clientid_by_clientconfigid(self, clientconfig_id: int, client_id: int, user_id: int):
        """Updates clientconfigs ClientID by clientconfigId:
           \nArgs: clientconfig_id (int), client_id (int), user_id (int)
           \nReturns: 1 if successful or 0 if failed
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_clientconfigs_upd_clientid_by_clientconfigid({clientconfig_id}, {client_id}, {user_id});", "", QueryType.UPDATE)
        return self.dbadapter.map_none_query(cursor)

    def update_clientconfigs_cv_appid_by_clientconfigid(self, clientconfig_id: int, configvalue: str, application_id: int, user_id: int):
        """Updates clientconfigs Config Value and Application ID by clientconfigId:
           \nArgs: clientconfig_id (int), configvalue (str), application_id (int), user_id (int)
           \nReturns: 1 if successful or 0 if failed
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_clientconfigs_upd_cv_appid_by_clientconfigid({clientconfig_id}, '{configvalue}', {application_id}, {user_id});", "", QueryType.UPDATE)
        return self.dbadapter.map_none_query(cursor)

    def update_clientconfigs_appid_cid_by_clientconfigid(self, clientconfig_id: int, application_id: int, client_id: int, user_id: int):
        """Updates clientconfigs Application ID and Client ID by clientconfigId:
           \nArgs: clientconfig_id (int), application_id (int), client_id (int), user_id (int)
           \nReturns: 1 if successful or 0 if failed
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_clientconfigs_upd_appid_cid_by_clientconfigid({clientconfig_id}, {application_id}, {client_id}, {user_id});", "", QueryType.UPDATE)
        return self.dbadapter.map_none_query(cursor)

    def update_clientconfigs_cv_cid_by_clientconfigid(self, clientconfig_id: int, configvalue: str, client_id: int, user_id: int):
        """Updates clientconfigs Config Value and Client ID by clientconfigId:
           \nArgs: clientconfig_id (int), configvalue (str), client_id (int), user_id (int)
           \nReturns: 1 if successful or 0 if failed
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_clientconfigs_upd_cv_cid_by_clientconfigid({clientconfig_id}, '{configvalue}', {client_id}, {user_id});", "", QueryType.UPDATE)
        return self.dbadapter.map_none_query(cursor)

    def update_clientconfigs_cv_appid_cid_by_clientconfigid(self, clientconfig_id: int, configvalue: str, application_id: int, client_id: int, user_id: int):
        """Updates clientconfigs Config Value, Application ID and Client ID by clientconfigId:
           \nArgs: clientconfig_id (int), configvalue (str), application_id (int), client_id (int), user_id (int)
           \nReturns: 1 if successful or 0 if failed
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_clientconfigs_upd_cv_appid_cid_by_clientconfigid({clientconfig_id}, '{configvalue}', {application_id}, {client_id}, {user_id});", "", QueryType.UPDATE)
        return self.dbadapter.map_none_query(cursor)

    def update_lookupconfigurations_by_configid(self, config_id: int, config_alias: str, config_desc: str, user_id: int):
        """Updates lookupconfigurations by configId:
           \nArgs: config_id (int), config_alias (str), config_desc (str), user_id (int)
           \nReturns: 1 if successful or 0 if failed
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_lookupconfigurations_upd_by_configid({config_id}, '{config_alias}', '{config_desc}', {user_id});", "", QueryType.UPDATE)
        return self.dbadapter.map_none_query(cursor)

    def update_organisationhierarchy_pid_by_hierarchyid(self, hierarchy_id: int, parentclient_id: int, user_id: int):
        """Updates organisationhierarchy Parent Client ID by hierarchyId:
           \nArgs: hierarchy_id (int), parentclient_id (int), user_id (int)
           \nReturns: 1 if successful or 0 if failed
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_organisationhierarchy_upd_pid_by_hierarchyid({hierarchy_id}, {parentclient_id}, {user_id});", "", QueryType.UPDATE)
        return self.dbadapter.map_none_query(cursor)

    def update_organisationhierarchy_cl_by_hierarchyid(self, hierarchy_id: int, client_level: int, user_id: int):
        """Updates organisationhierarchy Client Level by hierarchyId:
           \nArgs: hierarchy_id (int), client level (int), user_id (int)
           \nReturns: 1 if successful or 0 if failed
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_organisationhierarchy_upd_cl_by_hierarchyid({hierarchy_id}, {client_level}, {user_id});", "", QueryType.UPDATE)
        return self.dbadapter.map_none_query(cursor)

    def update_organisationhierarchy_by_hierarchyid(self, hierarchy_id: int, parentclient_id: int, client_level: int, user_id: int):
        """Updates organisationhierarchy by hierarchyId:
           \nArgs: hierarchy_id (int), parentclient_id (int), client level (int), user_id (int)
           \nReturns: 1 if successful or 0 if failed
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_organisationhierarchy_upd_pid_cl_by_hierarchyid({hierarchy_id}, {parentclient_id}, {client_level}, {user_id});", "", QueryType.UPDATE)
        return self.dbadapter.map_none_query(cursor)

    # endregion UPDATE


class CountryProvider(BaseProvider):
    def get_countries(self):
        """
            Get all countries from db
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_countries_sel();", "", QueryType.SELECT)
        return self.dbadapter.map_data_tuples(cursor)


class LanguageProvider(BaseProvider):
    def get_languages(self):
        """
            Get all languages from db
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_languages_sel();", "", QueryType.SELECT)
        return self.dbadapter.map_data_tuples(cursor)


class MessageProvider(BaseProvider):
    """MessageProvider [Provider class for messages]
    """

    def __init__(self):
        pass

    # region GET
    def get_messages(self, channelid: int, clientid: int):
        """Get translated messages

        Args:\n
            channelid (int): Channel Id
            clientid (int): Client Id

        Returns:
            Dictionary of messages
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_messagetranslations_sel_by_channelid_clientid({channelid},{clientid});", "", QueryType.SELECT)
        return self.dbadapter.map_data_tuples(cursor)

    def get_messages_by_channelid(self, channelid: int):
        """Get translated messages

        Args:\n
            channelid (int): Channel Id
            clientid (int): Client Id

        Returns:
            Dictionary of messages
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_messagetranslations_sel_by_channelid({channelid});", "", QueryType.SELECT)
        return self.dbadapter.map_data_tuples(cursor)

    def get_messages_by_channelid_messageids(self, channelid: int, messageids: List[int]):
        """
            Returns: Dictionary of messages
        """
        self._get_adapter_instance()
        messageids = self.dbadapter.format_list_to_strings(messageids)
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_messagetranslations_sel_by_channelid_messageids({channelid},{messageids});", "", QueryType.SELECT)
        return self.dbadapter.map_data_tuples(cursor)

    def get_messages_by_channelid_clientid_messageids(self, channelid: int, clientid: int, messageids: List[int]):
        """
            Returns: Dictionary of messages
        """
        self._get_adapter_instance()
        messageids = self.dbadapter.format_list_to_strings(messageids)
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_messagetranslations_sel_by_channelid_clientid_messageids({channelid},{clientid},{messageids});", "", QueryType.SELECT)
        return self.dbadapter.map_data_tuples(cursor)

    def get_messages_by_msgtranslationid(self, msgtranslationid: int):
        """Get translated messages

        Args:\n
            messageid (int): Translated Message Id

        Returns:
            Dictionary of messages
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_messagetranslations_sel_by_msgtranslationid({msgtranslationid});",
            "", QueryType.SELECT)
        return self.dbadapter.map_data_tuples(cursor)

    def get_message_details_by_channelid(self, channelid: int):
        """Get translated message details from table for GraphQL query

        Args:\n
            channelid (int): Channel Id

        Returns:
            Dictionary of messages
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_messagetranslations_sel_details_by_channelid({channelid});", "", QueryType.SELECT)
        return self.dbadapter.map_data_tuples(cursor)

    def insert_message(self, message_id, message_copy, channel_id, user_id):
        """Inserts a new message translation:
           \nArgs: message_id, message_copy, channel_id, client_id, user_id
           \nReturns: 1 if successful or 0 if failed
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_messagetranslations_ins({message_id},{message_copy},{channel_id},{user_id});", "", QueryType.SELECT)
        return self.dbadapter.map_none_query(cursor)

    def delete_message(self, msgtranslation_id):
        """ Deletes translated message by provided Message ID and expiry date < Now()
            \n Args: message_id
            \n Returns 1 if succesfull or 0 if failed
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_messagetranslations_del_by_msgtranslationid({msgtranslation_id});", "", QueryType.SELECT)
        return self.dbadapter.map_none_query(cursor)

    def get_messages_by_clientid(self, clientid: int):
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_messagetranslations_sel_by_clientid({clientid});", "", QueryType.SELECT)
        return {k: v for k, v in cursor}

    def get_messages_by_namemessageid_channel_id(self, channel_id: int):
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_messagetranslations_sel_by_namemessageid({channel_id});", "", QueryType.SELECT)
        return self.dbadapter.map_data_rows(cursor)

    def get_messages_by_descmessageid_channel_id(self, channel_id: int):
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_messagetranslations_sel_by_descmessageid({channel_id});", "", QueryType.SELECT)
        return self.dbadapter.map_data_rows(cursor)

    def get_messages_by_servicecategorynamemessageid_channel_id(self, channel_id: int):
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_messagetranslations_sel_by_servicecategorynamemessageid({channel_id});", "", QueryType.SELECT)
        return self.dbadapter.map_data_rows(cursor)
    # endregion GET

    def insert_messages(self, message_category_id, user_id):
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_messages_ins({message_category_id}, {user_id});", "", QueryType.SELECT)
        return cursor.fetchone()[0]

    def insert_messagecategories(self, message_category_name, message_category_description, user_id):
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_messagecategories_ins('{message_category_name}', '{message_category_description}', {user_id});", "", QueryType.SELECT)
        return cursor.fetchone()[0]

    def insert_messagetranslations_with_clientid(self, message_id, message_copy, channel_id, client_id, user_id):
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_messagetranslations_ins_clientid({message_id}, '{message_copy}', {channel_id}, {client_id}, {user_id});", "", QueryType.INSERT)
        return self.dbadapter.map_none_query(cursor)

    def update_messagetranslations_all_by_messagetranslationid(self, channel_id, message_copy, client_id, message_translation_id, user_id):
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_messagetranslations_upd_all_by_messagetranslationid({channel_id}, '{message_copy}', {client_id}, {message_translation_id}, {user_id});", "", QueryType.UPDATE)
        return self.dbadapter.map_none_query(cursor)

    def update_messagetranslations_min_by_messagetranslationid(self, channel_id, message_copy, message_translation_id, user_id):
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_messagetranslations_upd_min_by_messagetranslationid({channel_id}, '{message_copy}', {message_translation_id}, {user_id});", "", QueryType.UPDATE)
        return self.dbadapter.map_none_query(cursor)

    def update_messages_messagecategoryid_by_messageid(self, message_category_id, message_id, user_id):
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_messages_upd_messagecategoryid_by_messageid({message_category_id}, {message_id}, {user_id});", "", QueryType.UPDATE)
        return self.dbadapter.map_none_query(cursor)


class OperatingSystemProvider(BaseProvider):
    # TODO : Need to move this to Utils

    def __init__(self):
        pass

    def get_operatingsystems_by_operatingsystemname(self, os_name: str):
        """Get OperatingSystem details from table based on input for checking with Operating System Version

        Args:\n
            os_name (str): Operating System Name

        Returns:
            Dictionary of operatingsystems
        """
        self._get_adapter_instance()
        cursor = self.dbadapter.execute_query(
            f"call dbcache.p_lookupoperatingsystems_sel_by_operatingsystemname('{os_name}');", "", QueryType.SELECT)
        return self.dbadapter.map_data(cursor)
