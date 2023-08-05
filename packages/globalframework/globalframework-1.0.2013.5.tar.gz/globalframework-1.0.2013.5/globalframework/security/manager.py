import binascii
import copy
import math
from globalframework.internationalisation.manager import ConfigManager
from globalframework.security.encrypto import Crypto
from globalframework.security.provider import SecurityProvider, ServiceProvider
from globalframework.security.password_policy import PolicyStrength
from globalframework.caching.cache_manager import CacheManager
from globalframework.enumeration import SystemTokens
from globalframework.data.setting import HashSetting



class SecurityManager:
    def __init__(self):
        self.security_provider = SecurityProvider()
        self.cachemanager = CacheManager()
        self.cryptolib = Crypto()
        self.hash_setting = HashSetting()
        self.hasher = PasswordHash()
        self.config_manager = ConfigManager()

    def _encrypt_plaintext(self, plaintext: str, key):
        cipertext = self.cryptolib.encrypt(plaintext, key)
        return cipertext.decode("utf-8")

    def _decrypt_plaintext(self, cipertext: str, key):
        plaintext = self.cryptolib.decrypt(cipertext.encode(), key)
        return plaintext

    def _get_user_id_based_on_token(self, user_token: str):
        """Get user id based on user token"""
        session_token = self.security_provider.get_systemtoken_by_tokenname(SystemTokens.SESSION_TOKEN.value)
        user_id = self.cryptolib.decrypt( user_token.encode(), session_token['Token'])
        return user_id

    def encrypt_plaintext_with_security_token(self, plaintext: str):
        """"""
        security_token = self.security_provider.get_systemtoken_by_tokenname(
            SystemTokens.SECURITY_TOKEN.value)
        return self._encrypt_plaintext(plaintext, security_token['Token'])

    def encrypt_plaintext_with_session_token(self, plaintext: str):
        """"""
        session_token = self.security_provider.get_systemtoken_by_tokenname(
            SystemTokens.SESSION_TOKEN.value)
        return self._encrypt_plaintext(plaintext, session_token['Token'])

    def decrypt_plaintext_with_security_token(self, cipertext: str):
        """"""
        security_token = self.security_provider.get_systemtoken_by_tokenname(
            SystemTokens.SECURITY_TOKEN.value)
        return self._decrypt_plaintext(cipertext, security_token['Token'])

    def decrypt_plaintext_with_session_token(self, cipertext: str):
        """"""
        security_token = self.security_provider.get_systemtoken_by_tokenname(
            SystemTokens.SESSION_TOKEN.value)
        return self._decrypt_plaintext(cipertext, security_token['Token'])

    # region GET
    def get_userpermissions_by_userid(self, user_id: int):
        dbrecords = self.security_provider.get_userpermissions_by_userid(
            user_id)
        return dbrecords

    def get_userpermissions_by_serviceid(self, service_id: int):
        dbrecords = self.security_provider.get_userpermissions_by_serviceid(
            service_id)
        return dbrecords

    def get_userpermissions_by_userid_serviceid(self, user_id: int, service_id: int):
        dbrecords = self.security_provider.get_userpermissions_by_userid_serviceid(
            user_id, service_id)
        return dbrecords

    def get_userpermissions(self):
        dbrecords = self.security_provider.get_userpermissions()
        return dbrecords

    def get_rolepermissions_by_roleid(self, role_id: int):
        dbrecords = self.security_provider.get_rolepermissions_by_roleid(
            role_id)
        return dbrecords

    def get_rolepermissions_by_serviceid(self, service_id: int):
        dbrecords = self.security_provider.get_rolepermissions_by_serviceid(
            service_id)
        return dbrecords

    def get_rolepermissions_by_roleid_serviceid(self, role_id: int, service_id: int):
        dbrecords = self.security_provider.get_rolepermissions_by_roleid_serviceid(
            role_id, service_id)
        return dbrecords

    def get_rolepermissions(self):
        dbrecords = self.security_provider.get_rolepermissions()
        return dbrecords

    def get_user_roles(self):
        return self.security_provider.get_user_roles()

    def get_userroles_by_roleid(self, role_id: int):
        return self.security_provider.get_userroles_by_roleid(role_id)

    def get_userroles_by_userid(self, user_id: int):
        return self.security_provider.get_userroles_by_userid(user_id)

    def get_userroles_by_userid_roleid(self, user_id: int, role_id: int):
        return self.security_provider.get_userroles_by_userid_roleid(user_id, role_id)

    def get_roles_by_roleid(self, role_id: int):
        """Select roles by role ID."""
        return self.security_provider.get_roles_by_roleid(role_id)

    def get_roles_by_rolename(self, role_name: str):
        """Select roles by rolename."""
        return self.security_provider.get_roles_by_rolename(role_name)

    def get_roles_by_all(self):
        """Select roles all."""
        return self.security_provider.get_roles_by_all()

    def get_file_attributes_by_id_and_attribute_id(self, id, attribute_id):
        return self.security_provider.get_file_attributes_by_id_and_attribute_id(id, attribute_id)

    def get_audithistoryattributes_sel_by_audithistoryattributeid(self, audit_history_attribute_id: int):
        """select audithistoryattribute by audithistoryattributeid"""
        return self.security_provider.get_audithistoryattributes_sel_by_audithistoryattributeid(audit_history_attribute_id)

    def get_timezone(self):
        return self.security_provider.get_timezone()

    def get_userroles_permissions(self, userid):
        permissions = self.security_provider.get_userroles_permissions(userid)
        perm = ['view', 'create', 'update', 'delete']
        return [
            {'ServiceId': k,
             'ServiceAlias': v[0],
             'Permissions': dict(zip(perm, list(bin(v[1]).replace("0b", "").zfill(4)[::-1])))
             } for k, v in permissions.items()
        ]

    # Handle Permissions via encrypted User Token.
    def get_userroles_permissions_by_token(self, usertoken, servicealias):
        userid = self.decrypt_plaintext_with_session_token(usertoken)
        permissions = self.security_provider.get_userroles_permissions(userid)
        result = {}
        perm = ['view', 'create', 'update', 'delete']
        permission_list = [
            {'serviceid': k,
             'servicealias': v[0],
             'permissions': dict(zip(perm, list(bin(v[1]).replace("0b", "").zfill(4)[::-1])))
             } for k, v in permissions.items()
        ]
        for each in permission_list:
            if each['servicealias'] == servicealias:
                result = each
                break
        return result

    def get_user_by_email(self, email_id):
        return self.security_provider.get_user_by_email(email_id)

    def get_user_by_username(self, user_name):
        return self.security_provider.get_user_by_username(user_name)

    def get_user_by_userid(self, id):
        return self.security_provider.get_user_by_userid(id)

    def get_securitypolicy_sel_by_userid(self, userid):
        result = self.security_provider.get_securitypolicy_sel_by_userid(userid)
        return [{'policyid': k, 'policyname': v[0], 'policyvalue': v[1]} for k, v in result.items()]

    def get_users_by_rowlimit(self, client_id: str, display_rows: str):
        """Obtain Users based on ClientID and display based on Client Configuration for number
           of rows to be displayed at a time. display_rows is a multiplier used with the Client
           Configuration for number of rows to get the list total of users to be returned.
           ClientID and Displayrows value to be coerced into integer from dictionary source.
        """
        default_config = self.config_manager.get_default_clientconfigs_by_configalias('GlobalRowsToDisplay')
        try:
            if type(int(client_id)) == int:
                config_overwrite = self.config_manager.get_clientconfigs_by_clientid_configalias(int(client_id), 'GlobalRowsToDisplay')
            if config_overwrite is None:
                config_overwrite = default_config
        except:
            config_overwrite = default_config
        try:
            config = int(config_overwrite['ConfigValue'])
            total_rows = config * int(display_rows)
        except ValueError as value_error:
            return "ValueError"
        except TypeError as type_error:
            return "TypeError"
        result = self.security_provider.get_users_by_rowlimit(client_id, total_rows)
        return result[0: total_rows]

    # endregion GET

    # region INSERT
    def insert_userpermissions(self, user_id: int, service_id: int, permission_set: int, valid_from: str, valid_to: str, admin_user_id: int):
        """Inserting permissionsets for services tied to a user."""
        records = self.security_provider.insert_userpermissions(
            user_id, service_id, permission_set, valid_from, valid_to, admin_user_id)
        return records

    def insert_rolepermissions(self, role_id: int, service_id: int, permission_set: int, valid_from: str, valid_to: str, admin_user_id: int):
        """Inserting permissionsets for services tied to a role."""
        records = self.security_provider.insert_rolepermissions(
            role_id, service_id, permission_set, valid_from, valid_to, admin_user_id)
        return records

    def insert_roles(self, role_id: int, role_name: str, role_desc: str, user_id: int):
        """Inserting roles in dbsecurity.roles ."""
        records = self.security_provider.insert_roles(
            role_name, role_desc, user_id)
        return records

    def insert_or_update_timezone(self, params):
        return self.security_provider.insert_or_update_timezone(params)

    def insert_file(self, params):
        """
            Sample params should be like this:
            params = {
                "category_id": 1,
                "identity_id": 1,
                "mime_type_id": 1,
                "size": 1024,
                "attribute_id": 1,
                "attribute_value": "32x32",
                "is_active": True,
                "user_id": 1
            }
        """

        if "attribute_id" not in params and "attribute_value" not in params:
            file_id = self.security_provider.insert_file(params)
            return bool(file_id)

        file_params = copy.deepcopy(params)
        file_params.pop("attribute_id", None)
        file_params.pop("attribute_value", None)
        file_id = self.security_provider.insert_file(file_params)
        attribute_params = {
            "attribute_id": params["attribute_id"],
            "file_id": file_id,
            "attribute_value": params["attribute_value"],
            "user_d": params["user_id"]
        }
        return self.security_provider.insert_file_attributes(attribute_params)

    def create_roles_process(self, param):
        status_code = 404
        values = tuple(param.values())
        status = self.insert_roles(*values)
        if status:
            status_code = 201
        return status_code

    def insert_audithistory(self, audit_history_id: int, audit_category_id: int, audit_action_id: int, origin_value: str, new_value: str, ip_address: str, createdby_user_id: int, created_date: str):
        """Insert audithistory in dblog.audithistory"""
        records = self.security_provider.insert_audithistory(
            audit_history_id, audit_category_id, audit_action_id, origin_value, new_value, ip_address, createdby_user_id, created_date)
        return records

    def insert_lookupauditactions(self, audit_action_id: int, audit_action_name: str, name_message_id: int, createdby_user_id: int, created_date: str, modifiedby_user_id: int, modified_date: str):
        """Insert lookupauditactions in dblog.lookupauditactions"""
        records = self.security_provider.insert_lookupauditactions(
            audit_action_id, audit_action_name, name_message_id, createdby_user_id, created_date, modifiedby_user_id, modified_date)
        return records

    def insert_lookupauditattributes(self, audit_attribute_id: int, audit_attribute_name: str, name_message_id: int, createdby_user_id: int, created_date: str, modifiedby_user_id: int, modified_date: str):
        """Insert lookupauditattributes in dblog.lookupauditattributes"""
        records = self.security_provider.insert_lookupauditattributes(
            audit_attribute_id, audit_attribute_name, name_message_id, createdby_user_id, created_date, modifiedby_user_id, modified_date)
        return records

    def insert_lookupauditcategories(self, audit_category_id: int, audit_category_name: str, name_message_id: int, createdby_user_id: int, created_date: str, modifiedby_user_id: int, modified_date: str):
        """Insert lookupauditcategories in dblog.lookupauditcategories"""
        records = self.security_provider.insert_lookupauditcategories(
            audit_category_id, audit_category_name, name_message_id, createdby_user_id, created_date, modifiedby_user_id, modified_date)
        return records

    def insert_user(self, user_name: str, email: str, first_name: str, last_name: str, channelid: int, password: str, is_active: int, userstatusid: int, created_by: str):
        userid = self.decrypt_plaintext_with_session_token(created_by)
        algorithmid = self.hash_setting.get_hash_connection()['DEFAULT_ALGORITHM']
        if not algorithmid:
            algorithmid = 1
        hashed_pw = self.hasher.hash_data(password)
        return self.security_provider.insert_user(user_name, email, first_name, last_name, channelid, hashed_pw, algorithmid, is_active, userstatusid, userid)

    def insert_clientuser(self, client_id: int, user_id: int, current_user_id: int):
        """Insert a clientuser in dbsecurity.clientusers"""
        records = self.security_provider.insert_clientuser(client_id, user_id, current_user_id)
        return records

    # endregion INSERT

    # region UPDATE
    def update_userpermissions(self, user_id: int, service_id: int, permission_set: int, valid_from: str, valid_to: str, admin_user_id: int):
        # TODO : NXG-381
        records = self.security_provider.update_userpermissions_by_userid(
            user_id, service_id, permission_set, valid_from, valid_to, admin_user_id)
        return records

    def update_rolepermissions(self, role_id: int, service_id: int, permission_set: int, valid_from: str, valid_to: str, admin_user_id: int):
        """"""
        # TODO : NXG-381
        records = self.security_provider.update_rolepermissions_by_roleid(
            role_id, service_id, permission_set, valid_from, valid_to, admin_user_id)
        return records

    def update_roles_by_roleid(self, role_id: int, role_name: str, role_desc: str, user_id: int):
        """When updating entries in roles table, a history log will be inserted into dblog.roleshistory table prior to update for audit purposes."""
        # TODO : NXG-381
        records = self.security_provider.update_roles_by_roleid(
            role_id, role_name, role_desc, user_id)
        return records

    def update_roles_process(self, param):
        status_code = 404
        values = tuple(param.values())
        status = self.update_roles_by_roleid(*values)
        if status:
            status_code = 201
        return status_code
    # endregion UPDATE

    def update_file(self, params):
        return self.security_provider.update_file(params)

    def update_user_pwd_by_userid(self, user_id: int, password: str, algorithm_id: int):
        return self.security_provider.update_user_pwd_by_userid(user_id, password, algorithm_id)

    def update_user_status_by_user_id(self, user_id: int, is_active: int, user_status_id: int):
        return self.security_provider.update_user_status_by_user_id(user_id, is_active, user_status_id)

    def update_user_by_user_id(self, user_id: int, user_name: int, email: str, first_name: str, last_name: str, is_active: int, created_by: int):
        return self.security_provider.update_user_by_user_id(user_id, user_name, email, first_name, last_name, is_active, created_by)

    def update_user_isactive_by_userid(self, userid):
        return self.security_provider.update_user_isactive_by_userid(userid)

    # endregion UPDATE

    # region DELETE

    # TODO : Naming og dbrecords doesnt makes sense
    # The services needs to be rewritten we shouldn't be returning error code here

    def delete_userpermissions(self, userpermissions_id: int):
        success = self.security_provider.delete_userpermissions_by_userpermissionsid(
            userpermissions_id)
        return success

    def delete_roles_by_roleid(self, role_id: int):
        """Deleting role entries by roleID ."""
        success = self.security_provider.delete_roles_by_roleid(role_id)
        return success

    def delete_roles_process(self, param):
        status_code = 404
        values = tuple(param.values())
        status = self.delete_roles_by_roleid(*values)
        if status:
            status_code = 204
        return status_code

    def delete_rolepermissions(self, rolepermissions_id: int):
        success = self.security_provider.delete_rolepermissions_by_rolepermissionsid(
            rolepermissions_id)
        return success
    # endregion DELETE

    def request_lookup(self, request_type: str, source, param=None):
        if param:
            return getattr(self, request_type + '_' + source)(*param)
        return getattr(self, request_type + '_' + source)()

    def create_roles_process(self, param):
        status_code = 404
        values = tuple(param.values())
        status = self.insert_roles(*values)
        if status:
            status_code = 201
        return status_code

    def update_roles_process(self, param):
        status_code = 404
        values = tuple(param.values())
        status = self.update_roles_by_roleid(*values)
        if status:
            status_code = 201
        return status_code

    def delete_roles_process(self, param):
        status_code = 404
        values = tuple(param.values())
        status = self.delete_roles_by_roleid(*values)
        if status:
            status_code = 204
        return status_code


class ServiceManager():

    def __init__(self):
        self.service_provider = ServiceProvider()
        self.cachemanager = CacheManager()

    def access_cache(self, key_name: str, provider_method, *args):
        """Abstract method to be called when requiring cache access.
           \nArgs:key_name (str), provider_result
           \nReturns: Result of provider method or None
        """
        cache_key = f'{key_name}'
        records = self.cachemanager.read(cache_key)
        if records:
            return records
        else:
            dbrecords = getattr(self.service_provider, provider_method)(*args)
        if dbrecords:
            self.cachemanager.store(cache_key, dbrecords)
            return dbrecords
        else:
            return None

    def get_services(self):
        """"""
        return self.access_cache(f'get_services_all', self.get_services.__name__)

    def get_services_by_serviceid(self, serviceid: int):
        """"""
        return self.access_cache(f'get_services_by_serviceid_{serviceid}', self.get_services_by_serviceid.__name__, serviceid)

    def get_services_by_lookuplicenseid(self, lookuplicenseid: int):
        """"""
        return self.access_cache(f'get_services_by_lookuplicenseid_{lookuplicenseid}', self.service_provider.get_services_by_lookuplicenseid.__name__, lookuplicenseid)

    def get_services_by_servicecategoryid(self, servicecategoryid: int):
        """"""
        return self.access_cache(f'get_services_by_servicecategoryid_{servicecategoryid}', self.service_provider.get_services_by_servicecategoryid.__name__, servicecategoryid)

    def get_services_by_parentserviceid(self, parentserviceid: int):
        """"""
        return self.access_cache(f'get_services_by_parentserviceid_{parentserviceid}', self.service_provider.get_services_by_parentserviceid.__name__, parentserviceid)

    def get_services_by_servicename(self, servicename: str):
        """"""
        return self.access_cache(f'get_services_by_servicename_{servicename}', self.service_provider.get_services_by_servicename.__name__, servicename)

    def get_services_by_servicecategoryid_lookuplicenseid(self, servicecategoryid: int, lookuplicenseid: int):
        """"""
        return self.access_cache(f'get_services_by_servicecategoryid_lookuplicenseid_{servicecategoryid}_{lookuplicenseid}', self.service_provider.get_services_by_servicecategoryid_lookuplicenseid.__name__, servicecategoryid, lookuplicenseid)

    def get_services_by_lookuplicenseid_parentserviceid(self, lookuplicenseid: int, parentserviceid: int):
        """"""
        return self.access_cache(f'get_services_by_lookuplicenseid_parentserviceid_{lookuplicenseid}_{parentserviceid}', self.service_provider.get_services_by_lookuplicenseid_parentserviceid.__name__, lookuplicenseid, parentserviceid)

    def get_services_by_servicecategoryid_parentserviceid(self, servicecategoryid: int, parentserviceid: int):
        """"""
        return self.access_cache(f'get_services_by_servicecategoryid_parentserviceid_{servicecategoryid}_{parentserviceid}', self.service_provider.get_services_by_servicecategoryid_parentserviceid.__name__, servicecategoryid, parentserviceid)

    def get_services_by_servicecategoryid_lookuplicenseid_parentserviceid(self, servicecategoryid: int, lookuplicenseid: int, parentserviceid: int):
        """"""
        return self.access_cache(f'get_services_by_servicecategoryid_lookuplicenseid_parentserviceid_{servicecategoryid}_{lookuplicenseid}_{parentserviceid}', self.service_provider.get_services_by_servicecategoryid_lookuplicenseid_parentserviceid.__name__, servicecategoryid, lookuplicenseid, parentserviceid)

class PasswordHash():

    def __init__(self):
        self.security_provider = SecurityProvider()
        self.hash_setting = HashSetting()
        self.cryptolib = Crypto()

    def hash_data(self, data: str):
        """Checks gfconfig.json for Hashing AlgorithmID which will indicate hashing algorithm to be used for input data.
           Returns data (str) in hashed form.
        """
        algorithm_id = self.hash_setting.get_hash_connection()['DEFAULT_ALGORITHM']
        if algorithm_id == None:
            algorithm_id = 1
        algorithm_object = self.security_provider.get_algorithm_by_algorithmid(
            algorithm_id)
        hashed = binascii.hexlify(self.cryptolib.hash_content(
            data + '1000', algorithm_object['AlgorithmName'])).decode()
        return hashed

class PasswordPolicyManager():

    def __init__(self):
        self.security_provider = SecurityProvider()
        self.security_manager = SecurityManager()
        self.policy_strength = PolicyStrength()
        self.overwrite_policies = []

    def validate_password(self, usertoken, password):
        if type(usertoken) == str:
            usertoken = int(self.security_manager.decrypt_plaintext_with_session_token(usertoken))
        userid = math.log(usertoken, 8)
        user_policy = self.get_user_policy(userid)
        user_specific_policy = PolicyStrength(user_policy)
        test_result = user_specific_policy.perform_test(password)
        if False in test_result.values():
            return False
        return True

    def get_clients(self, user):
        """Returns a list of Client objects based on User (userid = math.log(x, 8)) or otherwise None.
        """
        security_provider = SecurityProvider()
        client_details = []
        if user is not None:
            client_list = self.check_user_has_client(round(math.pow(8, float(user))))
            if client_list is not None:
                for client in client_list:
                    client_details.append(security_provider.get_client_by_clientid(client['ClientID']))
                return client_details
            else:
                return None

    def get_user_policy(self, user):
        """Takes in user id information in the form of math.log(x, 8) where x is user id and returns
           Dictionary object of Password Policies after checking for possible client specific
           Password Policies.
        """
        client = self.get_clients(user)
        if client is not None:
            security_policy = self.get_client_overwrite_policy(int(client[0]['ClientID']))
        else:
            security_policy = self.get_client_overwrite_policy(0)
        return security_policy

    def get_client_overwrite_policy(self, clientid: int):
        self.overwrite_policies = self.security_provider.get_clientoverwritesecuritypolicies_by_clientid(
            clientid)
        security_policy = self.policy_strength.get_policy()
        if self.overwrite_policies is None:
            return security_policy
        else:
            for policy in self.overwrite_policies:
                if policy['SecurityPolicyID'] == 9:
                    security_policy['SpecialCharacters'] = int(
                        policy['OverwriteValue'])
                if policy['SecurityPolicyID'] == 10:
                    security_policy['NonLetters'] = int(
                        policy['OverwriteValue'])
                if policy['SecurityPolicyID'] == 11:
                    security_policy['MinCharacters'] = int(
                        policy['OverwriteValue'])
                if policy['SecurityPolicyID'] == 12:
                    security_policy['MaxCharacters'] = int(
                        policy['OverwriteValue'])
                if policy['SecurityPolicyID'] == 13:
                    security_policy['UppercaseLetter'] = int(
                        policy['OverwriteValue'])
            return security_policy

    def check_user_has_client(self, userid: int):
        check_client = self.security_provider.get_client_by_userid(userid)
        if check_client is None:
            return None
        else:
            return check_client