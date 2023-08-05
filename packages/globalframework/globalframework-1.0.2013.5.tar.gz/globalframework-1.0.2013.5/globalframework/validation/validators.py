# default packages
import re
import math
import uuid
import string as string_
from decimal import Decimal
from fractions import Fraction


integer_types = (int,)
basestring = (str, bytes)
POSITIVE_INFINITY = math.inf
NEGATIVE_INFINITY = -math.inf
float_ = float
uuid_ = uuid
bool_ = bool
bool_types = ['true', 'false', '0', '1', 'on', 'off', 'yes', 'no']
numeric_types = (int, float, Decimal, Fraction)
IPV6_REGEX = re.compile(
    '^(?:(?:[0-9A-Fa-f]{1,4}:){6}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|::(?:[0-9A-Fa-f]{1,4}:){5}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){4}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){3}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,2}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){2}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,3}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}:(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,4}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,5}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}|(?:(?:[0-9A-Fa-f]{1,4}:){,6}[0-9A-Fa-f]{1,4})?::)(?:%25(?:[A-Za-z0-9\\-._~]|%[0-9A-Fa-f]{2})+)?$'
)
URL_PROTOCOLS = ('http://', 'https://', 'ftp://')
SPECIAL_USE_DOMAIN_NAMES = ('localhost', 'invalid', 'test', 'example')
URL_REGEX = re.compile(
    r"^"
    # protocol identifier
    r"(?:(?:https?|ftp)://)"
    # user:pass authentication
    r"(?:\S+(?::\S*)?@)?"
    r"(?:"
    # IP address exclusion
    # private & local networks
    r"(?!(?:10|127)(?:\.\d{1,3}){3})"
    r"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
    r"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
    # IP address dotted notation octets
    # excludes loopback network 0.0.0.0
    # excludes reserved space >= 224.0.0.0
    # excludes network & broadcast addresses
    # (first & last IP address of each class)
    r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
    r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
    r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
    r"|"
    r"(?:"
    r"(?:localhost|invalid|test|example)|("
    # host name
    r"(?:(?:[A-z\u00a1-\uffff0-9]-*_*)*[A-z\u00a1-\uffff0-9]+)"
    # domain name
    r"(?:\.(?:[A-z\u00a1-\uffff0-9]-*)*[A-z\u00a1-\uffff0-9]+)*"
    # TLD identifier
    r"(?:\.(?:[A-z\u00a1-\uffff]{2,}))"
    r")))"
    # port number
    r"(?::\d{2,5})?"
    # resource path
    r"(?:/\S*)?"
    r"$", re.UNICODE)
URL_SPECIAL_IP_REGEX = re.compile(
    r"^"
    # protocol identifier
    r"(?:(?:https?|ftp)://)"
    # user:pass authentication
    r"(?:\S+(?::\S*)?@)?"
    r"(?:"
    # IP address dotted notation octets
    # excludes loopback network 0.0.0.0
    # excludes reserved space >= 224.0.0.0
    # excludes network & broadcast addresses
    # (first & last IP address of each class)
    r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
    r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
    r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
    r"|"
    # host name
    r"(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)"
    # domain name
    r"(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*"
    # TLD identifier
    r"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
    r")"
    # port number
    r"(?::\d{2,5})?"
    # resource path
    r"(?:/\S*)?"
    r"$", re.UNICODE)


def is_numeric(value, allow_empty=False, minimum=None, maximum=None):
    if maximum is None:
        maximum = POSITIVE_INFINITY

    if minimum is None:
        minimum = NEGATIVE_INFINITY

    if value is None and not allow_empty:
        return False
    elif value is not None:
        if isinstance(value, str):
            try:
                value = float_(value)
            except (ValueError, TypeError):
                return False
        elif not isinstance(value, numeric_types):
            return False

    if value is not None and value > maximum:
        return False

    if value is not None and value < minimum:
        return False

    return True


def is_string(value, allow_empty=False,  minimum_length=None, maximum_length=None, whitespace_padding=False):
    if not value and allow_empty:
        return True

    elif not value:
        return False

    if minimum_length is None:
        minimum_length = 1

    if minimum_length == 1 and allow_empty:
        minimum_length = 0

    if maximum_length is None:
        maximum_length = POSITIVE_INFINITY

    value = str(value)

    if value and maximum_length and len(value) > maximum_length:
        return False

    if value and minimum_length and len(value) < minimum_length:
        if whitespace_padding:
            value = value.ljust(minimum_length, ' ')
        else:
            return False
    return True


def is_empty(value, allow_empty=False):
    if not value and allow_empty:
        return False
    elif not value:
        return True

    return False


def is_none(value, allow_empty=False):
    if value is not None and not value and allow_empty:
        pass
    elif (value is not None and not value) or value:
        return False

    return True


def validate_email_address(emailaddress, regexpr=None):
    """Validate email address with default regular expression if none provided.
        \nArgs: emailaddress (str), regexpr (str) [optional]
        \nReturns: [bool]: valid status
    """
    if not emailaddress:
        return False

    if not regexpr:
        regexpr = r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$"

    match = re.match(regexpr, emailaddress, re.IGNORECASE)
    return True if match else False


def validate_email_addresses(emailaddresses):
    """Validate email addresses and remove any duplicate entries
       \nArgs: emailaddresses (list): list of email address
       \nReturns: [dictionary]: email addresses with valid status
    """

    if not emailaddresses:
        return None

    # remove any duplicate entries
    result = dict.fromkeys(emailaddresses)

    for emailaddress in list(result):
        result[emailaddress] = validate_email_address(emailaddress)

    return result


def is_bool(value, allow_empty=False):
    if isinstance(value, bool_):
        return True     # Checks for actual True and False boolean types.
    try:
        # Checks value to see if it's an acceptable boolean value that is not natively a boolean type.
        if str(value).lower() not in bool_types:
            return False
    except ValueError:
        return False    # Cannot coerce into boolean Error
    return True


# Checking for type only or needing to coerce the value as well?
def is_float(value, allow_empty=False, minimum=None, maximum=None):
    try:
        result = is_numeric(value=value,
                            allow_empty=allow_empty,
                            minimum=minimum,
                            maximum=maximum)

        if result:
            try:
                value = float_(value)
            except (ValueError, TypeError, AttributeError, IndexError, SyntaxError):
                return False
        else:
            return False

    except (ValueError, TypeError):
        return False

    except Exception as error:
        return False

    return True


def is_url(value, allow_empty=False, allow_special_ips=False):
    """
    :param allow_special_ips: If ``True``, will succeed when validating special IP
      addresses, such as loopback IPs like ``127.0.0.1`` or ``0.0.0.0``. If ``False``,
      will raise a :class:`InvalidURLError` if ``value`` is a special IP address. Defaults
      to ``False``.
    :type allow_special_ips: :class:`bool <python:bool>`
    """
    if not value and not allow_empty:
        return False
        # Empty Value Check
    elif not value:
        return None

    if not isinstance(value, basestring):
        return False
        # Invalid String

    is_valid = False
    lowercase_value = value.lower()
    stripped_value = None
    lowercase_stripped_value = None
    for protocol in URL_PROTOCOLS:
        if protocol in value:
            stripped_value = value.replace(protocol, '')
            lowercase_stripped_value = stripped_value.lower()

    if lowercase_stripped_value is not None:
        for special_use_domain in SPECIAL_USE_DOMAIN_NAMES:
            if special_use_domain in lowercase_stripped_value:
                has_port = False
                port_index = lowercase_stripped_value.find(':')
                if port_index > -1:
                    has_port = True
                    lowercase_stripped_value = lowercase_stripped_value[:port_index]
                if not has_port:
                    path_index = lowercase_stripped_value.find('/')
                    if path_index > -1:
                        lowercase_stripped_value = lowercase_stripped_value[:path_index]

                    if lowercase_stripped_value:
                        if '/' in lowercase_stripped_value:
                            return False 
                            # Valid domain cannot contain '/'
                        if '\\' in lowercase_stripped_value:
                            return False
                            # Valid domain cannot contain '\\'
                        if '@' in lowercase_stripped_value:
                            return False
                            # Valid domain cannot contain '@'
                        if ':' in lowercase_stripped_value:
                            return False 
                            # Valid domain cannot contain ':'

                        lowercase_stripped_value = lowercase_stripped_value.strip().lower()

                        for item in string_.whitespace:
                            if item in lowercase_stripped_value:
                                return False
                                 # Valid domain cannot contain 'whitespace'
                        if lowercase_stripped_value in SPECIAL_USE_DOMAIN_NAMES:
                            is_valid = True

    if not is_valid and allow_special_ips:
        if is_ipaddress(stripped_value, allow_empty=False):
            is_valid = True

    if not is_valid:
        is_valid = URL_REGEX.match(value)
        print(f'REGEX RESULT = {is_valid}')

    if not is_valid and allow_special_ips:
        is_valid = URL_SPECIAL_IP_REGEX.match(value)

    if not is_valid:
        return False

    return True


def is_uuid(value, allow_empty=False):
    if not value and not allow_empty:
        return False
        # Empty Value Check
    elif not value:
        return None

    if isinstance(value, uuid_.UUID):
        return True

    try:
        value = uuid_.UUID(value)
    except ValueError:
        return False
        # Cannot coerce into uuid Error

    return True


def is_ip4(value, allow_empty=False):
    if not value and allow_empty is False:
        return False        # Empty String Check
    elif not value:
        return None

    try:
        components = value.split('.')
    except AttributeError:
        return False 
        # Invalid IP Address v4 Error

    if len(components) != 4 or not all(x.isdigit() for x in components):
        return False
        # Invalid IP Address v4 Error

    for x in components:
        try:
            result = is_numeric(x, allow_empty=allow_empty,
                                minimum=0, maximum=255)
            if not result and not isinstance(x, integer_types):
                return False
        except ValueError:
            return False 
            # Invalid IP Address v4 Error

    return True


def is_ip6(value, allow_empty=False):
    if not value and allow_empty is False:
        return False 
        # Empty String Check
    elif not value:
        return None

    if not isinstance(value, str):
        return False

    value = value.lower().strip()

    is_valid = IPV6_REGEX.match(value)

    if not is_valid:
        return False
        # Invalid IP Address

    return True


def is_ipaddress(value, allow_empty=False):
    if not value and not allow_empty:
        return False
        # Empty Value
    elif not value:
        return None

    if not is_ip6(value):
        if not is_ip4(value):
            return False

    return True
