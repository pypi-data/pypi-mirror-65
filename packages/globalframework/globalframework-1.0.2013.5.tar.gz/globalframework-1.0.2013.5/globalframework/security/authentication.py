# Default libraries
import math
import binascii

# Third party libraries
from cryptography.fernet import InvalidToken

# Globalframework libraries
from globalframework.security.encrypto import Crypto
from globalframework.security.provider import SecurityProvider
from globalframework.security.manager import SecurityManager, PasswordHash
from globalframework.security.model import AuthHeader, UserTokenBearerDTO, UserDetailDTO, PasswordResetCheck
from globalframework.security.password_policy import PolicyStrength, PasswordStats
from globalframework.error_dict import ErrorDictionary
from globalframework.enumeration import SystemTokens, LookupSecurityPolicyCategories
from globalframework.utility.utils import random_string
from globalframework.data.setting import HashSetting
from globalframework.validation.validators import validate_email_address, is_string




class VerifyUserAuth:

    def __init__(self, pusername_or_email: str, ppassword: str):
        self.pusername_or_email = pusername_or_email
        self.ppassword = ppassword
        self.auth_payload = AuthHeader()

    def perform_verification(self):
        tests = self._get_test_items()
        authentication_test = AuthenticationTest(self.auth_payload,
                                                 tests,
                                                 self.pusername_or_email,
                                                 self.ppassword)
        authentication_test.execute()

        if len(self.auth_payload.messagelist) == 0:
            actions = self._get_action_items()
            authentication_actions = AuthenticationActions(
                self.auth_payload, actions)
            authentication_actions.execute()
        return self.auth_payload

    def _get_test_items(self):
        return ['username_or_email', 'password', 'is_active', 'credentials']

    def _get_action_items(self):
        return ['generate_tokens', 'get_token_bearer_expiry', 'create_token_bearer', 'update_security_details']


class VerifyUserToken():
    def __init__(self, user_token: str, user_secret: str):
        self.auth_payload = AuthHeader()
        self.auth_payload.user_token = user_token
        self.auth_payload.user_secret = user_secret

    def perform_verification(self):

        tests = self._get_test_items()

        authentication_test = AuthenticationTest(self.auth_payload,
                                                 tests, '', '')
        authentication_test.execute()

        if len(self.auth_payload.messagelist) == 0:
            actions = self._get_action_items()
            authentication_actions = AuthenticationActions(
                self.auth_payload, actions)
            authentication_actions.execute()

        return self.auth_payload

    def _get_test_items(self):
        return ['user_token', 'user_secret']

    def _get_action_items(self):
        return ['get_token_bearer_expiry', 'get_token_bearer', 'update_token_bearer_expiry']


# region AuthenticationTest
class AuthenticationTest:

    def __init__(self, auth_payload: AuthHeader, test_items: [], pusername_or_email: str, ppassword: str):
        self.auth_payload = auth_payload
        self.test_items = test_items
        self.pusername_or_email = pusername_or_email
        self.ppassword = ppassword
        self.lookup_error_list = ErrorDictionary()
        self.user_object = None
        self.security_provider = SecurityProvider()
        self.password_hash = PasswordHash()

    def lookupMethod(self, command):
        return getattr(self, '_test_' + command, None)

    def execute(self):
        for item in self.test_items:
            method = self.lookupMethod(item)
            result = method()
            if len(self.auth_payload.messagelist) > 0:
                return result

    def _test_is_empty(self, value: str, value_length: int):
        return is_string(value, False,  value_length)

    def _test_username_or_email(self):
        if not self._test_is_empty(self.pusername_or_email, 5):
            msg = self.lookup_error_list.get_error_message('auth', 'A001')
            self.auth_payload.messagelist.append(msg)
            return False
        return True

    def _test_password(self):
        if not self._test_is_empty(self.ppassword, 5):
            msg = self.lookup_error_list.get_error_message('auth', 'A002')
            self.auth_payload.messagelist.append(msg)
            return False
        return True

    def _test_user_token(self):
        if not self._test_is_empty(self.auth_payload.user_token, 5):
            msg = self.lookup_error_list.get_error_message('auth', 'A002')
            self.auth_payload.messagelist.append(msg)
            return False
        return True

    def _test_user_secret(self):
        if not self._test_is_empty(self.auth_payload.user_secret, 5):
            msg = self.lookup_error_list.get_error_message('auth', 'A002')
            self.auth_payload.messagelist.append(msg)
            return False
        return True

    def _test_is_active(self):
        is_email = validate_email_address(self.pusername_or_email)
        if is_email:
            self.user_object = self.security_provider.get_user_by_email(
                self.pusername_or_email)
        else:
            self.user_object = self.security_provider.get_user_by_username(
                self.pusername_or_email)

        if(self.user_object is None):
            msg = self.lookup_error_list.get_error_message('auth', 'A003')
            self.auth_payload.messagelist.append(msg)
            return
        if(self.user_object['IsActive'] == 0):
            msg = self.lookup_error_list.get_error_message('auth', 'A004')
            self.auth_payload.messagelist.append(msg)
            return

    def _test_credentials(self):
        if(self.user_object):
            security_token = self.security_provider.get_systemtoken_by_tokenname(
                SystemTokens.SECURITY_TOKEN.value)
            cryptolib = Crypto()
            hash_given_pw = self.password_hash.hash_data(self.ppassword)
            if(self.user_object['Password'] == hash_given_pw):
                self.auth_payload.is_authenticated = True
                self.auth_payload.user_token = self.user_object['UserID']
            else:
                self.auth_payload.is_authenticated = False
                msg = self.lookup_error_list.get_error_message('auth', 'A003')
                self.auth_payload.messagelist.append(msg)
                return
# endregion AuthenticationTest

# region AuthentictionActions


class AuthenticationActions():
    def __init__(self, auth_payload: AuthHeader, action_items: []):
        self.auth_payload = auth_payload
        self.action_items = action_items
        self.user_id = 0
        self.lookup_error_list = ErrorDictionary()
        self.security_provider = SecurityProvider()
        self.security_manager = SecurityManager()

    def lookupMethod(self, command):
        return getattr(self, '_action_' + command, None)

    def execute(self):
        for item in self.action_items:
            method = self.lookupMethod(item)
            result = method()
            if(len(self.auth_payload.messagelist) > 0):
                return

    def _action_generate_tokens(self):
        '''Generate user and secret tokens'''
        session_token = self.security_provider.get_systemtoken_by_tokenname(
            SystemTokens.SESSION_TOKEN.value)
        security_token = self.security_provider.get_systemtoken_by_tokenname(
            SystemTokens.SECURITY_TOKEN.value)

        cryptolib = Crypto()
        self.user_id = str(self.auth_payload.user_token)
        self.auth_payload.user_token = cryptolib.encrypt(
            self.user_id, session_token['Token']).decode()
        random_characters = random_string(16)
        raw_security_token = random_characters + \
            str(10000000000 + int(self.user_id))
        self.auth_payload.user_secret = cryptolib.encrypt(
            raw_security_token, security_token['Token']).decode()

    def _action_get_token_bearer_expiry(self):
        ''' 1.Get session expiration based on security policy
            2. updates payload expiry window
        '''
        # TODO : Add a new proc to get by category and policy Id
        # TODO : Get security policy based on  user client to overwrite the default policies

        security_policies = self.security_provider.get_lookupsecuritypolicies_by_securitypolicycategoryid(
            LookupSecurityPolicyCategories.USER.value)

        session_expiry = 30

        for policy in security_policies:
            if(policy['SecurityPolicyName'] == 'SessionExpiryInMins'):
                session_expiry = int(policy['SecurityPolicyValue'])

        self.auth_payload.expiry = session_expiry

    def _action_create_token_bearer(self):
        ''' 1.Create new token bearer
            2.update expiry(mins) in AuthHeader
            3.Delete Expired token bearer
        '''
        token_bearer = UserTokenBearerDTO(user_id=int(
            self.user_id), user_token=self.auth_payload.user_secret, expiry=self.auth_payload.expiry)
        result = self.security_provider.insert_usertokenbearer(token_bearer)

        if(not result):
            msg = self.lookup_error_list.get_error_message('auth', 'A005')
            self.auth_payload.messagelist.append(msg)

        self.security_provider.delete_usertokenbearer_by_userid_expiry(
            self.user_id)

    def _action_get_token_bearer(self):
        user_token = self.auth_payload.user_token
        secret_token = self.auth_payload.user_secret

        self.user_id   = self.security_manager._get_user_id_based_on_token(user_token)

        result = self.security_provider.get_usertokenbearer_by_userid_usertoken(
            self.user_id, secret_token)

        if(not result):
            msg = self.lookup_error_list.get_error_message('auth', 'A006')
            self.auth_payload.messagelist.append(msg)
            return

        self.auth_payload.is_authenticated = True

    def _action_update_security_details(self):
        ''' 1.Search for Security Details
            2.Create one if does exist
            3.Update LastSuccessfulLogin and LoginRetry
         '''
        result = self.security_provider.get_usersecuritydetails_by_userid(
            self.user_id)
        user_security_details = UserDetailDTO(user_detail_id=0,
                                              user_id=self.user_id,
                                              login_retry=0,
                                              last_successful_login=None,
                                              is_ldap=0,
                                              created_date=None,
                                              modified_date=None)

        if not result:
            result = self.security_provider.insert_usersecuritydetails(
                user_security_details)
        else:
            result = self.security_provider.update_usersecuritydetails_by_user_id(
                user_security_details)

        if not result:
            msg = self.lookup_error_list.get_error_message('auth', 'A005')
            self.auth_payload.messagelist.append(msg)

    def _action_update_token_bearer_expiry(self):
        self.security_provider.update_usertokenbearer_by_usertoken(
            self.auth_payload.user_secret, self.auth_payload.expiry)

class PasswordResetVerify:
    def __init__(self, new_password: str, confirm_password: str):
        self.new_password = new_password
        self.confirm_password = confirm_password
        self.security_provider = SecurityProvider()
        self.hash_setting = HashSetting()
        self.password_hash = PasswordHash()
        self.password_check = PasswordResetCheck()

    def reset_verification(self, security_policy, user):
        reset_test = PasswordResetTest(self.password_check,
                                       self.new_password,
                                       self.confirm_password,
                                       security_policy)
        reset_test.execute()

        if len(self.password_check.messagelist) == 0:
            self.password_check.is_verified = True
            self.update_password(self.confirm_password, user)
            print('Password change accepted!')
        return self.password_check

    def update_password(self, confirm_password, user):
        algorithm_id = self.hash_setting.get_hash_connection()['DEFAULT_ALGORITHM']
        hashed_password = self.password_hash.hash_data(confirm_password)
        user_object = self.security_provider.get_user_by_userid(
            round(math.pow(8, float(user))))
        algorithm_object = self.security_provider.get_algorithm_by_algorithmid(
            algorithm_id)
        self.security_provider.update_user_pwd_by_userid(
            user_object['UserID'], hashed_password, algorithm_id)


class PasswordResetPolicies():

    def __init__(self):
        self.security_provider = SecurityProvider()
        self.password_policies = []
        self.overwrite_policies = []
        self.policy_strength = PolicyStrength()

    # Get the client overwrite policies
    def get_client_overwrite_policy(self, clientid: int):
        self.overwrite_policies = self.security_provider.get_clientoverwritesecuritypolicies_by_clientid(
            clientid)
        security_policy = self.policy_strength.get_policy()
        if self.overwrite_policies is None:
            return security_policy
        else:
            for policy in self.overwrite_policies:
                if policy['SecurityPolicyID'] == 9:
                    security_policy['special_characters'] = int(
                        policy['OverwriteValue'])
                if policy['SecurityPolicyID'] == 10:
                    security_policy['non_letters'] = int(
                        policy['OverwriteValue'])
                if policy['SecurityPolicyID'] == 11:
                    security_policy['min_length'] = int(
                        policy['OverwriteValue'])
                if policy['SecurityPolicyID'] == 12:
                    security_policy['max_length'] = int(
                        policy['OverwriteValue'])
                if policy['SecurityPolicyID'] == 13:
                    security_policy['letters_uppercase'] = int(
                        policy['OverwriteValue'])
            return security_policy

    # Obtains the client ID if client is assigned to User ID.
    def check_user_has_client(self, userid: int):
        check_client = self.security_provider.get_client_by_userid(userid)
        if check_client is None:
            return None
        else:
            return check_client


class PasswordResetTest():
    def __init__(self, password_check: PasswordResetCheck, new_password: str, confirm_password: str, security_policy: dict):
        self.password_check = password_check
        self.new_password = new_password
        self.confirm_password = confirm_password
        self.password_reset_policies = PasswordResetPolicies()
        self.security_provider = SecurityProvider()
        self.lookup_error_list = ErrorDictionary()
        self.security_policy = security_policy
        self.pw_stats = PasswordStats(new_password)
        self.policy_strength = PolicyStrength(security_policy)

    def execute(self):
        if self.test_is_empty() == False:
            result = self.policy_strength.perform_test(self.new_password)
            for item in result:
                if result[item] == False:
                    self.get_pw_error_message(item)
                if len(self.password_check.messagelist) > 0:
                    return
        else:
            if len(self.password_check.messagelist) > 0:
                return
        if self.test_matching_passwords() == False:
            if len(self.password_check.messagelist) > 0:
                return

    def get_pw_error_message(self, test_item):
        if test_item == 'min_length':
            msg = self.lookup_error_list.get_error_message('pwreset', 'P004')
            self.password_check.messagelist.append(msg)
        elif test_item == 'max_length':
            msg = self.lookup_error_list.get_error_message('pwreset', 'P005')
            self.password_check.messagelist.append(msg)
        elif test_item == 'letters_uppercase':
            msg = self.lookup_error_list.get_error_message('pwreset', 'P006')
            self.password_check.messagelist.append(msg)
        elif test_item == 'special_characters':
            msg = self.lookup_error_list.get_error_message('pwreset', 'P002')
            self.password_check.messagelist.append(msg)
        elif test_item == 'non_letters':
            msg = self.lookup_error_list.get_error_message('pwreset', 'P003')
            self.password_check.messagelist.append(msg)
        else:
            msg = self.lookup_error_list.get_error_message('pwreset', 'P007')
            self.password_check.messagelist.append(msg)

    # Checks if either password form fields are empty
    def test_is_empty(self):
        if len(self.new_password) != 0 and len(self.confirm_password) != 0:
            return False
        else:
            msg = self.lookup_error_list.get_error_message('pwreset', 'P001')
            self.password_check.messagelist.append(msg)
            return True

    # Test for matching password in fields
    def test_matching_passwords(self):
        if self.new_password == self.confirm_password:
            return True
        else:
            msg = self.lookup_error_list.get_error_message('pwreset', 'P007')
            self.password_check.messagelist.append(msg)
            return False


class PasswordRecoveryVerification:

    def __init__(self):
        self.crypto = Crypto()
        self.security_provider = SecurityProvider()
        self.token = self.security_provider.get_systemtoken_by_tokenname(
            SystemTokens.SECURITY_TOKEN.value)['Token'].encode()

    # Checks for the existence of username in database prior to generating a password recovery request. If logged in, skip this method.
    def verify_email(self, username: str):
        security = SecurityProvider()
        is_email = validate_email_address(username)
        if is_email:
            dbrecords = security.get_user_by_email(username)
        else:
            dbrecords = security.get_user_by_username(username)
        if dbrecords is not None and is_email == True:
            if dbrecords['Email'] == username:
                return math.log(dbrecords['UserID'], 8)
            else:
                return None
        elif dbrecords is not None and is_email == False:
            if dbrecords['UserName'] == username:
                return math.log(dbrecords['UserID'], 8)
            else:
                return None
        else:
            return None

    # Generates a token based on existing SECURITY Key.
    def request_email_token(self, user):
        self.encryption = self.crypto.encrypt(str(user), self.token)
        return self.encryption

    # Checks the token validity based on time from the password recovery email link.
    def verify_request_token(self, encryption):
        try:
            user = self.crypto.decrypt_with_sliding_window(
                encryption.encode(), self.token, 60)
            if self.security_provider.get_user_by_userid(round(math.pow(8, float(user)))) is not None:
                return user
            else:
                return None

        # If key was in str instead of bytes. Probably can remove this check once keys ensured to be stored correctly.
        except TypeError:
            return None

        # When users click on an expired link and no key was found in temp_storage for decryption.
        except UnboundLocalError:
            return None

        # When users click on an expired link with valid decryption key.
        except InvalidToken:
            return None
