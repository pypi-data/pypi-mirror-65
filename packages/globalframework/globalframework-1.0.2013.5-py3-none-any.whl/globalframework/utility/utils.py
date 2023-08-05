import random
import string
# import json
# from globalframework import constants
from globalframework.error_dict import ErrorDictionary
from globalframework.utility import bitwise_logic as bit


def random_string(string_length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def bitwise_function(db_num):
    db_input = bit.database_input(db_num)
    combination = bit.permission_logic(db_input)
    dict_output = bit.permission_output(combination)
    return dict_output


def get_error_response(error_type: str, errorcode):
    """Returns a dictionary of errorcodes and error messages to be utilized for API endpoint responses. error_type refers to the error dictionary lookup name, errorcode refers to any form of error codes whether in string, integer or list."""
    status = errorcode
    error_dict = {}
    if type(status) != list:
        status = []
        status.append(errorcode)
    for code in status:
        code = str(code).replace("'", "'")
        error_msg = ErrorDictionary().get_error_message(error_type, code)
        if not error_msg:
            error_dict[code] = "invalid error code"
        else:
            error_dict[code] = error_msg
    return error_dict
