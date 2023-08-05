## default libraries
from dataclasses import dataclass
import datetime

@dataclass
class UserDetailDTO:
    user_detail_id: int
    user_id: int
    login_retry: int
    last_successful_login: datetime
    is_ldap: int
    created_date: datetime
    modified_date: datetime


@dataclass
class UserDTO:
    user_id: int
    user_name: str
    email: str
    first_name: str
    last_name: str
    channel_id: int
    password: str
    is_active: int
    user_status_id: int
    created_date: datetime
    created_user_id: int
    modified_date: datetime
    modified_user_id: int


@dataclass
class SecurityPolicyDTO:
    security_policy_id: int
    security_policy_name: str
    security_policy_desc: str
    security_policy_category_id: int
    value: str
    created_date: datetime
    modified_date: datetime


class UserTokenBearerDTO:
    def __init__(self, user_id=0, user_token='', expiry=0):
        self.user_id = user_id
        self.user_token = user_token
        self.expiry = expiry



class AuthHeader:
    def __init__(self, is_authenticated=False, user_token='', user_secret='', expiry=0):
        """ is_authenticated :- is user authenticated
            \n expiry :- auth expires in  N (mins)
            \n messagelist :- information or errors related to user auth
        """
        self.is_authenticated = is_authenticated
        self.user_token = user_token
        self.user_secret = user_secret
        self.expiry = expiry
        self.messagelist = []


class PasswordResetCheck():
    def __init__(self, is_verified=False, user_token=''):
        self.is_verified = is_verified
        self.user_token = user_token
        self.messagelist = []

