""" This is a Security provider module"""
__all__ = []
__version__ = '0.0.1'
__author__ = 'Anand'

# Default packages
from typing import List
import datetime

# Globalframework packages
from globalframework.data.baseprovider import BaseProvider
from globalframework.security.model import UserDetailDTO, UserTokenBearerDTO
from globalframework.enumeration import QueryType


class SecurityProvider(BaseProvider):
    """Security data provider"""

    #region GET

    def __init__(self):
        self._get_adapter_instance()

    def get_usersecuritydetails_by_userid(self, user_id: int):
        """Get userdetails:
           \nArgs:user_id(int)
           \nReturns: UserDetails object
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_usersecuritydetails_sel_by_userid('{user_id}');", "", QueryType.SELECT)
        return self.dbadapter.map_data(cursor)

    def get_user_by_email(self, user_email: str):
        """Get user by email:
           \nArgs:user_email(str)
           \nReturns: User object
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_users_sel_by_email('{user_email}');", "", QueryType.SELECT)
        return self.dbadapter.map_data(cursor)

    def get_user_by_username(self, user_name: str):
        """Get user by username:
           \nArgs:user_name(str)
           \nReturns: User object
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_users_sel_by_username('{user_name}');", "", QueryType.SELECT)
        return self.dbadapter.map_data(cursor)

    def get_user_by_userid(self, user_id: int):
        """Get user by userId:
           \nArgs:user_id(int)
           \nReturns: User object
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_users_sel_by_userid({user_id});", "", QueryType.SELECT)
        return self.dbadapter.map_data(cursor)

    def get_userid_by_clientid(self, client_id: int):
        """Get user by clientId:
           \nArgs:client_id(int)
           \nReturns: User ID
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_userid_by_clientid('{client_id}');", "", QueryType.SELECT)
        return self.dbadapter.map_data(cursor)

    def get_lookupsecuritypolicies_by_securitypolicycategoryid(self, security_policy_category_id: int):
        """Get security policy by securitypolicycategoryid:
           \nArgs:security_policy_category_id(int)
           \nReturns: list of security policy objects
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_lookupsecuritypolicies_sel_by_securitypolicycategoryid('{security_policy_category_id}');", "", QueryType.SELECT)
        return self.dbadapter.map_data_rows(cursor)

    def get_clientoverwritesecuritypolicies_by_clientid(self, client_id: int):
        """Get client overwrite security policy by clientid:
           \nArgs:client_id(int)
           \nReturns: list of client overwrite security policy objects
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_clientoverwritesecuritypolicies_sel_by_clientid('{client_id}');", "", QueryType.SELECT)
        return self.dbadapter.map_data_rows(cursor)

    def get_systemtoken_by_tokenname(self, token_name: str):
        """Get system token by token name:
           \nArgs:token_name(varchar(100))
           \nReturns: single token
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_systemtokens_sel_by_systemtokenname('{token_name}');", "", QueryType.SELECT)
        return self.dbadapter.map_data(cursor)

    def get_usertokenbearer_by_userid_usertoken(self, user_id: int, user_token: str):
        """Get user token details (Expiry):
           \nArgs:user_id, user_token
           \nReturns: single token
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_usertokenbearer_sel_by_userid_usertoken('{user_id}', '{user_token}');", "", QueryType.SELECT)
        return self.dbadapter.map_data(cursor)

    def get_client_by_userid(self, user_id: int):
        """Get client by userId:
           \nArgs:user_id(int)
           \nReturns: Client object
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_client_sel_by_userid('{user_id}');", "", QueryType.SELECT)
        return self.dbadapter.map_data_rows(cursor)

    def get_client_by_clientid(self, client_id: int):
        """Get client by clientId:
           \nArgs:client_id(int)
           \nReturns: Client object
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_client_sel_by_clientid('{client_id}');", "", QueryType.SELECT)
        return self.dbadapter.map_data(cursor)

    def get_algorithm_by_algorithmid(self, algorithm_id: int):
        """Get Hash Algorithm by AlgorithmID:
           \nArgs:algorithm_id(int)
           \nReturns: Hash Algorithm object
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_lookuphashingalgorithms_sel_by_algorithmid({algorithm_id});", "", QueryType.SELECT)
        return self.dbadapter.map_data(cursor)

    def get_user_roles(self):
        cursor_obj = self.dbadapter.execute_query(
            f"call dbsecurity.p_userroles_sel_all();", "", QueryType.SELECT)

        columns = [column[0] for column in cursor_obj.description]
        return [dict(zip(columns, row)) for row in cursor_obj]

    def get_userroles_by_userid(self, user_id: int):
        """Get User Role by RoleID:
           \nArgs:role_id(int)
           \nReturns: User Role objects
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_userroles_sel_by_userid({user_id});", "", QueryType.SELECT)
        return self.dbadapter.map_data_rows(cursor)

    def get_userroles_by_roleid(self, role_id: int):
        """Get User Role by RoleID:
           \nArgs:role_id(int)
           \nReturns: User Role objects
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_userroles_sel_by_roleid({role_id});", "", QueryType.SELECT)
        return self.dbadapter.map_data_rows(cursor)

    def get_userroles_by_userid_roleid(self, user_id: int, role_id: int):
        """Get User Role by UserID, RoleID:
           \nArgs:user_id (int), role_id(int)
           \nReturns: User Role object
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_userroles_sel_by_userid_roleid({user_id}, {role_id});", "", QueryType.SELECT)
        return self.dbadapter.map_data(cursor)

    def get_userpermissions_by_userid(self, user_id: int):
        """Get User Permissions by UserID:
           \nArgs:user_id (int)
           \nReturns: User Permissions object
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_userpermissions_sel_by_userid({user_id});", "", QueryType.SELECT)
        return self.dbadapter.map_data_rows(cursor)

    def get_userpermissions_by_serviceid(self, service_id: int):
        """Get User Permissions by ServiceID:
           \nArgs:service_id (int)
           \nReturns: User Permissions object
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_userpermissions_sel_by_serviceid({service_id});", "", QueryType.SELECT)
        return self.dbadapter.map_data_rows(cursor)

    def get_userpermissions_by_userid_serviceid(self, user_id: int, service_id: int):
        """Get User Permissions by UserID and ServiceID:
           \nArgs:user_id (int), service_id (int)
           \nReturns: User Permissions object
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_userpermissions_sel_by_userid_serviceid({user_id}, {service_id});", "", QueryType.SELECT)
        return self.dbadapter.map_data(cursor)

    def get_userpermissions(self):
        """Get all User Permissions:
           \nArgs: None
           \nReturns: User Permissions object
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_userpermissions_sel_all();", "", QueryType.SELECT)
        return self.dbadapter.map_data_rows(cursor)

    def get_rolepermissions_by_roleid(self, role_id: int):
        """Get rolepermissions by RoleID:
           \nArgs:role_id (int)
           \nReturns: Role Permissions object
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_rolepermissions_sel_by_roleid({role_id});", "", QueryType.SELECT)
        return self.dbadapter.map_data_rows(cursor)

    def get_rolepermissions_by_serviceid(self, service_id: int):
        """Get rolepermissions by ServiceID:
           \nArgs:service_id (int)
           \nReturns: Role Permissions object
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_rolepermissions_sel_by_serviceid({service_id});", "", QueryType.SELECT)
        return self.dbadapter.map_data_rows(cursor)

    def get_rolepermissions_by_roleid_serviceid(self, role_id: int, service_id: int):
        """Get rolepermissions by RoleID and ServiceID:
           \nArgs:role_id (int), service_id (int)
           \nReturns: Role Permissions object
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_rolepermissions_sel_by_roleid_serviceid({role_id}, {service_id});", "", QueryType.SELECT)
        return self.dbadapter.map_data(cursor)

    def get_rolepermissions(self):
        """Get all Role Permissions:
           \nArgs: None
           \nReturns: Role Permissions object
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_rolepermissions_sel_all();", "", QueryType.SELECT)
        return self.dbadapter.map_data_rows(cursor)

    def get_roles_by_roleid(self, role_id: int):
        """Get Role by RoleID:
           \nArgs:role_id(int)
           \nReturns:Role Object
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_roles_sel_by_roleid({role_id});", "", QueryType.SELECT)
        return self.dbadapter.map_data(cursor)

    def get_roles_by_rolename(self, role_name: str):
        """Get Role by Rolename:
           \nArgs:role_name(str)
           \nReturns:Role Object
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_roles_sel_by_rolename('{role_name}');", "", QueryType.SELECT)
        return self.dbadapter.map_data_rows(cursor)

    def get_roles_by_all(self):
        """Get Role by Rolename:
           \nArgs:role_name(str)
           \nReturns:Role Object
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_roles_sel_all();", "", QueryType.SELECT)
        return self.dbadapter.map_data_rows(cursor)

    def get_timezone(self):
        """"""
        cursor_obj = self.dbadapter.execute_query(
            f"call dbcache.p_lookuptimezones_sel();", None, QueryType.SELECT)

        columns = [column[0] for column in cursor_obj.description]
        return [dict(zip(columns, row)) for row in cursor_obj]

    def get_file_attributes_by_id_and_attribute_id(self, id, attribute_id):
        """"""
        cursor_obj = self.dbadapter.execute_query(
            f"p_fileattributes_sel_by_fileid_fileattributeid('{id}', '{attribute_id}');", None, QueryType.SELECT
        )
        columns = [column[0] for column in cursor_obj.description]
        return [dict(zip(columns, row)) for row in cursor_obj]

    def get_audithistoryattributes_sel_by_audithistoryattributeid(self, audit_history_attribute_id: int):

        cursor = self.dbadapter.execute_query(
            f"call dblog.p_audithistoryattributes_sel_by_audithistoryattributeid({audit_history_attribute_id});", None, QueryType.SELECT)
        return self.dbadapter.map_data_rows(cursor)

    def get_userroles_permissions(self, userid: int):
        """Get Permissions from User Roles:
           \nArgs: userid(int)
           \nReturns: List of permissions objects
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_userroles_getpermission({userid});", "", QueryType.SELECT)
        return {row[0]: row[1:] for row in cursor if row[3] < datetime.datetime.now() <= row[4]}

    def get_securitypolicy_sel_by_userid(self, userid: int):
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_user_sel_securitypolicy_by_userid({userid});", "", QueryType.SELECT)
        result = {}
        for row in cursor:
            if row[1]:
                result[row[0]] = list(row[1:])
            else:
                result[row[0]][1] = row[2]
        return result

    def get_securitypolicy_default(self):
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_user_sel_securitypolicy_by_userid({1});", "", QueryType.SELECT)
        result = {}
        for row in cursor:
            result[row[1]] = row[2]
        return result

    def get_users_by_rowlimit(self, client_id: int, total_rows: int):
        """Return Users and limit return results based on display_rows"""
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_users_sel_by_rowlimit({client_id}, {total_rows});", None, QueryType.SELECT)
        return self.dbadapter.map_data_rows(cursor)

    #endregion GET

    #region INSERT
    def insert_usersecuritydetails(self, user_details: UserDetailDTO):
        """Inserts new user details:
           \nArgs:UserDetails {user_id, login_retry, is_ldap, user_token}
           \nReturns: 1 if successfull or 0 if failed
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_usersecuritydetails_ins('{user_details.user_id}', '{user_details.login_retry}', '{user_details.is_ldap}');", "", QueryType.INSERT)
        return self.dbadapter.map_none_query(cursor)

    def insert_usertokenbearer(self, user_token_bearer: UserTokenBearerDTO):
        """Insert new token bearer:
            \nArgs: UserTokenBearerDTO {user_id, user_token, expiry(mins)}
            \nReturns: 1 if successful or 0 if failed
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_usertokenbearer_ins({user_token_bearer.user_id},'{user_token_bearer.user_token}',{user_token_bearer.expiry});", "", QueryType.INSERT)
        return self.dbadapter.map_none_query(cursor)

    def insert_userroles(self, user_id: int, role_id: int, current_user_id: int):
        """Insert new user role:
            \nArgs: user_id (int), role_id (int), current_user_id (int)
            \nReturns: 1 if successful or 0 if failed
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_userroles_ins({user_id}, {role_id}, {current_user_id});", "", QueryType.INSERT)
        return self.dbadapter.map_none_query(cursor)

    def insert_userpermissions(self, user_id: int, service_id: int, permission_set: int, valid_from: str, valid_to: str, admin_user_id: int):
        """Insert new user permissions:
            \nArgs: user_id (int), service_id (int), permission_set (int), valid_from (str), valid_to (str), admin_user_id (int)
            \nReturns: 1 if successful or 0 if failed
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_userpermissions_ins({user_id}, {service_id}, {permission_set}, '{valid_from}', '{valid_to}', {admin_user_id});", "", QueryType.INSERT)
        return self.dbadapter.map_none_query(cursor)

    def insert_rolepermissions(self, role_id: int, service_id: int, permission_set: int, valid_from: str, valid_to: str, admin_user_id: int):
        """Insert new user permissions:
            \nArgs: service_id (int), permission_set (int), valid_from (str), valid_to (str), admin_user_id (int)
            \nReturns: 1 if successful or 0 if failed
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_rolepermissions_ins({role_id}, {service_id}, {permission_set}, '{valid_from}', '{valid_to}', {admin_user_id});", "", QueryType.INSERT)
        return self.dbadapter.map_none_query(cursor)

    def insert_roles(self, role_name: str, role_desc: str, user_id: int):
        """Insert from roles whenever an update is performed:
           \nArgs: role_name (str), role_desc(str), user_id(int)
           \nReturns: 1 if successful or 0 if failed
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_roles_ins('{role_name}', '{role_desc}', {user_id});", "", QueryType.INSERT)
        return self.dbadapter.map_none_query(cursor)

    def insert_file_attributes(self, params):
        values = tuple(params.values())
        cursor_obj = self.dbadapter.execute_query(
            f"call dbsecurity.p_fileattributes_ins{values};", None, QueryType.INSERT)
        return bool(cursor_obj)

    def insert_file(self, params):
        values = tuple(params.values())
        curser_obj = self.dbadapter.execute_query(
            f"call dbsecurity.p_files_ins{values};", None, QueryType.SELECT)
        return curser_obj.fetchone()[0]

    def insert_audithistory(self, audit_history_id: int, audit_category_id: int, audit_action_id: int, origin_value: str, new_value: str, ip_address: str, createdby_user_id: int, created_date: str):
        """Insert from audithistory whenever an update is performed:
           \nArgs: audit_history_id (int), audit_category_id (int), audit_action_id (int), origin_value(str), new_value (str), ip_address (str), createdby_user_id (int), created_date (str)
           \nReturns: 1 if successful or 0 if failed
        """
        cursor = self.dbadapter.execute_query(
            f"call dblog.p_audithistory_ins({audit_history_id}, {audit_category_id}, {audit_action_id}, '{origin_value}', '{new_value}', '{ip_address}', {createdby_user_id}, '{created_date}');", "", QueryType.INSERT)
        return self.dbadapter.map_none_query(cursor)

    def insert_lookupauditactions(self, audit_action_id: int, audit_action_name: str, name_message_id: int, createdby_user_id: int, created_date: str, modifiedby_user_id: int, modified_date: str):
        """Insert from lookupauditactions whenever an update is performed:
           \nArgs: audit_action_id (int), audit_action_name (str), name_message_id (int), createdby_user_id (int), created_date (str), modifiedby_user_id (id), modified_date (str)
           \nReturns: 1 if successful or 0 if failed
        """
        cursor = self.dbadapter.execute_query(
            f"call dblog.p_lookupauditactions_ins({audit_action_id}, '{audit_action_name}', {name_message_id}, {createdby_user_id}, '{created_date}', {modifiedby_user_id}, '{modified_date}');", "", QueryType.INSERT)
        return self.dbadapter.map_none_query(cursor)

    def insert_lookupauditattributes(self, audit_attribute_id: int, audit_attribute_name: str, name_message_id: int, createdby_user_id: int, created_date: str, modifiedby_user_id: int, modified_date: str):
        """Insert from lookupauditattributes whenever an update is performed:
           \nArgs: audit_attribute_id (int), audit_attribute_name (str), name_message_id (int), createdby_user_id (int), created_date (str), modifiedby_user_id (id), modified_date (str)
           \nReturns: 1 if successful or 0 if failed
        """
        cursor = self.dbadapter.execute_query(
            f"call dblog.p_lookupauditattributes_ins({audit_attribute_id}, '{audit_attribute_name}', {name_message_id}, {createdby_user_id}, '{created_date}', {modifiedby_user_id}, '{modified_date}');", "", QueryType.INSERT)
        return self.dbadapter.map_none_query(cursor)

    def insert_lookupauditcategories(self, audit_category_id: int, audit_category_name: str, name_message_id: int, createdby_user_id: int, created_date: str, modifiedby_user_id: int, modified_date: str):
        """Insert from lookupauditcategories whenever an update is performed:
           \nArgs: audit_category_id (int), audit_category_name (str), name_message_id (int), createdby_user_id (int), created_date (str), modifiedby_user_id (id), modified_date (str)
           \nReturns: 1 if successful or 0 if failed
        """
        cursor = self.dbadapter.execute_query(
            f"call dblog.p_lookupauditcategories_ins({audit_category_id}, '{audit_category_name}', {name_message_id}, {createdby_user_id}, '{created_date}', {modifiedby_user_id}, '{modified_date}');", "", QueryType.INSERT)
        return self.dbadapter.map_none_query(cursor)

    def insert_user(self, user_name: str, email: str, first_name: str, last_name: str, channelid: int, password: str, algorithmid: int, is_active: int, userstatusid: int, created_by: int):
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_user_ins('{user_name}', '{email}', '{first_name}', '{last_name}', {channelid}, '{password}', {algorithmid}, {is_active}, {userstatusid}, {created_by});", "", QueryType.INSERT
        )
        return self.dbadapter.map_none_query(cursor)

    def insert_clientuser(self, client_id: int, user_id: int, current_user_id: int):
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_clientusers_ins({client_id}, {user_id}, {current_user_id});", "", QueryType.INSERT
        )
        return self.dbadapter.map_none_query(cursor)

    #endregion INSERT

    #region UPDATE
    def update_usersecuritydetails_by_user_id(self, user_details: UserDetailDTO):
        """Updates userdetails by userId:
           \nArgs:UserDetails
           \nReturns: 1 if successfull or 0 if failed
        """         
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_usersecuritydetails_upd_by_userid('{user_details.user_id}', '{user_details.login_retry}');", "", QueryType.UPDATE)
        return self.dbadapter.map_none_query(cursor)

    def update_usertokenbearer_by_usertoken(self, user_token: str, expiry: int):
        """Updates user token expiry:
           \nArgs:user_token,  expiry(mins)
           \nReturns: 1 if successfull or 0 if failed
        """         
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_usertokenbearer_upd_by_usertoken('{user_token}', '{expiry}');", "", QueryType.UPDATE)
        return self.dbadapter.map_none_query(cursor)

    def update_user_pwd_by_userid(self, user_id:str, password:str, algorithm_id:int):
        # TODO: Need to add new method to update password and call that method here with proper changes.
        # from .authentication import PasswordResetVerify
        # password_update = PasswordResetVerify()
        # password_update.update_password(password, user_id)
        values = (user_id, password, algorithm_id)
        curser_obj = self.dbadapter.execute_query(
            f"call dbsecurity.p_user_upd_pwd_by_userid{values};", None, QueryType.UPDATE)
        return bool(curser_obj)

    def update_user_status_by_user_id(self, user_id: int, is_active: int , user_status_id: int):
        """"""
        values = (user_id, is_active, user_status_id)
        curser_obj = self.dbadapter.execute_query(
            f"call dbsecurity.p_user_upd_status_by_userid{values};", None, QueryType.UPDATE)
        return bool(curser_obj)

    def update_user_by_user_id(self, user_id:int , user_name: str, email:None, first_name: str, last_name: str, is_active: int, created_by: int):
        """"""
        values = (user_id, user_name, email, first_name, last_name, is_active, created_by)
        curser_obj = self.dbadapter.execute_query(
            f"call dbsecurity.p_user_upd_by_userid{values};", None, QueryType.UPDATE)
        return bool(curser_obj)

    def update_userroles_by_userid(self, user_id: int, role_id: str, current_user_id: int):
        """Updates userroles:
           \nArgs:user_id (int), role_id (int), current_user_id (int)
           \nReturns: 1 if successfull or 0 if failed
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_userroles_upd_by_userid({user_id}, {role_id}, {current_user_id});", "", QueryType.UPDATE)
        return self.dbadapter.map_none_query(cursor)

    def update_userpermissions_by_userid(self, user_id: int, service_id: int, permission_set: int, valid_from: str, valid_to: str, admin_user_id: int):
        """Updates userpermissions:
           \nArgs:user_id (int), service_id (int), permission_set (int), valid_from (str), valid_to (str), admin_user_id (int)
           \nReturns: 1 if successfull or 0 if failed
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_userpermissions_upd_by_userid({user_id}, {service_id}, {permission_set}, '{valid_from}', '{valid_to}', {admin_user_id});", "", QueryType.UPDATE)
        return self.dbadapter.map_none_query(cursor)

    def update_rolepermissions_by_roleid(self, role_id: int, service_id: int, permission_set: int, valid_from: str, valid_to: str, admin_user_id: int):
        """Updates rolepermissions:
           \nArgs:role_id (int), service_id (int), permission_set (int), valid_from (str), valid_to (str), admin_user_id (int)
           \nReturns: 1 if successful or 0 if failed
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_rolepermissions_upd_by_roleid({role_id}, {service_id}, {permission_set}, '{valid_from}', '{valid_to}', {admin_user_id});", "", QueryType.UPDATE)
        return self.dbadapter.map_none_query(cursor)

    def update_roles_by_roleid(self, role_id: int, role_name: str, role_desc: str, user_id: int):
        """Insert from roles whenever an update is performed:
           \nArgs: role_name (str), role_desc(str), user_id(int)
           \nReturns: 1 if successful or 0 if failed
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_roles_upd_by_roleid({role_id}, '{role_name}', '{role_desc}', {user_id});", "", QueryType.UPDATE)
        return self.dbadapter.map_none_query(cursor)

    def insert_or_update_timezone(self, params):
        values = tuple(params.values())
        if "id" in params:
            cursor_obj = self.dbadapter.execute_query(
                f"call dbcache.p_lookuptimezones_upd{values};",
                None, QueryType.UPDATE)
        else:
            cursor_obj = self.dbadapter.execute_query(
                f"call dbcache.p_lookuptimezones_ins{values};",
                None, QueryType.INSERT)
        return bool(cursor_obj)

    def update_file(self, params):
        values = tuple(params.values())
        curser_obj = self.dbadapter.execute_query(
            f"call dbsecurity.p_files_upd{values};", None, QueryType.INSERT)
        return bool(curser_obj)

    def update_user_isactive_by_userid(self, userid):
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_user_upd_by_userid({userid});", "", QueryType.UPDATE
        )
        return cursor

    # endregion UPDATE

    # region DELETE
    def delete_usertokenbearer_by_userid_expiry(self, user_id: int):
        """ Deletes usertokenbearer by provided userID and expiry date < Now()
            \n Args: user_id
            \n Returns 1 if succesfull or 0 if failed
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_usertokenbearer_del_by_userid('{user_id}');", "", QueryType.DELETE)
        return self.dbadapter.map_none_query(cursor)

    def delete_userroles_by_userid(self, user_id: int):
        """ Deletes userroles by provided userID
            \n Args: user_id
            \n Returns 1 if succesfull or 0 if failed
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_userroles_del_by_userid({user_id});", "", QueryType.DELETE)
        return self.dbadapter.map_none_query(cursor)

    def delete_userpermissions_by_userid(self, user_id: int):
        """ Deletes userpermissions by provided userID
            \n Args: user_id
            \n Returns 1 if succesfull or 0 if failed
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_userpermissions_del_by_userid({user_id});", "", QueryType.DELETE)
        return self.dbadapter.map_none_query(cursor)

    def delete_userpermissions_by_userpermissionsid(self, userpermissions_id: int):
        """ Deletes userpermissions by UserPermissionsID
            \n Args: userpermissions_id
            \n Returns 1 if succesfull or 0 if failed
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_userpermissions_del_by_userpermissionsid({userpermissions_id});", "", QueryType.DELETE)
        return self.dbadapter.map_none_query(cursor)

    def delete_rolepermissions_by_roleid(self, role_id: int):
        """ Deletes rolepermissions by provided roleID
            \n Args: role_id
            \n Returns 1 if succesfull or 0 if failed
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_rolepermissions_del_by_roleid({role_id});", "", QueryType.DELETE)
        return self.dbadapter.map_none_query(cursor)

    def delete_rolepermissions_by_rolepermissionsid(self, rolepermissions_id: int):
        """ Deletes rolepermissions by RolePermissionsID
            \n Args: rolepermissions_id
            \n Returns 1 if succesfull or 0 if failed
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_rolepermissions_del_by_rolepermissionsid({rolepermissions_id});", "", QueryType.DELETE)
        return self.dbadapter.map_none_query(cursor)

    def delete_roles_by_roleid(self, role_id: int):
        """Deletes Role by RoleID:
           \nArgs:role_id
           \nReturns:Returns 1 if succesfull or 0 if failed
        """
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_roles_del_by_roleid({role_id});", "", QueryType.DELETE)
        return self.dbadapter.map_none_query(cursor)
    # endregion DELETE


class ServiceProvider(BaseProvider):

    def __init__(self):
        self._get_adapter_instance()

    def get_services(self):
        """"""
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_services_sel();", "", QueryType.SELECT)
        columns = [column.name for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor]

    def get_services_by_serviceid(self, serviceid: int):
        """"""
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_services_sel_by_serviceid({serviceid});", "", QueryType.SELECT)
        columns = (column.name for column in cursor.description)
        return dict(zip(columns, *cursor))

    def get_services_by_lookuplicenseid(self, lookuplicenseid: int):
        """"""
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_services_sel_by_lookuplicenseid({lookuplicenseid});", "", QueryType.SELECT)
        columns = [column.name for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor]

    def get_services_by_servicecategoryid(self, servicecategoryid: int):
        """"""
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_services_sel_by_servicecategoryid({servicecategoryid});", "", QueryType.SELECT)
        columns = [column.name for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor]

    def get_services_by_parentserviceid(self, parentserviceid: int):
        """"""
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_services_sel_by_parentserviceid({parentserviceid});", "", QueryType.SELECT)
        columns = [column.name for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor]

    def get_services_by_servicename(self, servicename: str):
        """"""
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_services_sel_by_servicename('{servicename}');", "", QueryType.SELECT)
        columns = [column.name for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor]

    def get_services_by_servicecategoryid_lookuplicenseid(self, servicecategoryid: int, lookuplicenseid: int):
        """"""
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_services_sel_by_servicecategoryid_lookuplicenseid({servicecategoryid}, {lookuplicenseid});", "", QueryType.SELECT)
        columns = [column.name for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor]

    def get_services_by_lookuplicenseid_parentserviceid(self, lookuplicenseid: int, parentserviceid: int):
        """"""
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_services_sel_by_lookuplicenseid_parentserviceid({lookuplicenseid}, {parentserviceid});", "", QueryType.SELECT)
        columns = [column.name for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor]

    def get_services_by_servicecategoryid_parentserviceid(self, servicecategoryid: int, parentserviceid: int):
        """"""
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_services_sel_by_servicecategoryid_parentserviceid({servicecategoryid}, {parentserviceid});", "", QueryType.SELECT)
        columns = [column.name for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor]

    def get_services_by_servicecategoryid_lookuplicenseid_parentserviceid(self, servicecategoryid: int, lookuplicenseid: int, parentserviceid: int):
        """"""
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_services_sel_by_scategoryid_llicenseid_pserviceid({servicecategoryid}, {lookuplicenseid}, {parentserviceid});", "", QueryType.SELECT)
        columns = [column.name for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor]

    def insert_service(self, servicecategoryid: int, servicename: str, servicedesc: str, userid: int):
        """"""
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_services_ins({servicecategoryid}, '{servicename}', '{servicedesc}', {userid});", "", QueryType.INSERT)
        return self.dbadapter.map_none_query(cursor)

    def update_service_by_serviceid(self, lookuplicenseid: int, applicationid: int, servicecategoryid: int, parentserviceid: int, servicename: str, servicedesc: str, userid: int, serviceid: int):
        """"""
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_services_upd_by_serviceid({lookuplicenseid}, {applicationid}, {servicecategoryid}, {parentserviceid}, '{servicename}', '{servicedesc}', {userid}, {serviceid});", "", QueryType.UPDATE)
        return self.dbadapter.map_none_query(cursor)

    def delete_service_by_serviceid(self, serviceid: int):
        """"""
        cursor = self.dbadapter.execute_query(
            f"call dbsecurity.p_services_del_by_serviceid({serviceid});", "", QueryType.DELETE)
        return self.dbadapter.map_none_query(cursor)
