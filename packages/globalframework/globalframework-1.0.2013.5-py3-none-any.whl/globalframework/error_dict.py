
class ErrorDictionary():
    def __init__(self):
        pass

    def get_error_message(self, error_type, error_code):
        dictlookup = DictionaryLookup()
        method = dictlookup.lookupError(error_type)
        return method(error_code)


class DictionaryLookup():
    def __init__(self):
        pass

    def lookupError(self, command):
        return getattr(self, 'lookup_' + command, None)

    def lookup_odbc(self, arg):
        result = dict_odbc.get(arg)
        if(not result):
            arg = arg[1:]
            result = dict_odbc.get(arg)

        return result

    def lookup_auth(self, arg):
        result = dict_auth.get(arg)
        if(not result):
            arg = arg[1:]
            result = dict_auth.get(arg)

        return result

    def lookup_pwreset(self, arg):
        result = dict_pwreset.get(arg)
        if(not result):
            arg = arg[1:]
            result = dict_pwreset.get(arg)

        return result

    def lookup_statuscode(self, arg):
        result = dict_statuscode.get(arg)
        if(not result):
            arg = arg[1:]
            result = dict_statuscode.get(arg)

        return result

    # Add more dictonaries below

# region ODBC errors


dict_odbc = {
    "1000"	: "General warning",
    "1001"	: "Cursor operation conflict",
    "1002"	: "Disconnect error",
    "1003"	: "NULL value eliminated in set function",
    "1004"	: "String data, right-truncated",
    "1006"	: "Privilege not revoked",
    "1007"	: "Privilege not granted",
    "01S00"	: "Invalid connection string attribute",
    "01S01"	: "Error in row",
    "01S02"	: "Option value changed",
    "01S06"	: "Attempt to fetch before the result set returned the first rowset",
    "01S07"	: "Fractional truncation",
    "01S08"	: "Error saving File DSN",
    "01S09"	: "Invalid keyword",
    "7001"	: "Wrong number of parameters",
    "7002"	: "COUNT field incorrect",
    "7005"	: "Prepared statement not a cursor-specification",
    "7006"	: "Restricted data type attribute violation",
    "7009"	: "Invalid descriptor index",
    "07S01"	: "Invalid use of default parameter",
    "8001"	: "Client unable to establish connection",
    "8002"	: "Connection name in use",
    "8003"	: "Connection not open",
    "8004"	: "Server rejected the connection",
    "8007"	: "Connection failure during transaction",
    "08S01"	: "Communication link failure",
    "21S01"	: "Insert value list does not match column list",
    "21S02"	: "Degree of derived table does not match column list",
    "22001"	: "String data, right-truncated",
    "22002"	: "Indicator variable required but not supplied",
    "22003"	: "Numeric value out of range",
    "22007"	: "Invalid datetime format",
    "22008"	: "Datetime field overflow",
    "22012"	: "Division by zero",
    "22015"	: "Interval field overflow",
    "22018"	: "Invalid character value for cast specification",
    "22019"	: "Invalid escape character",
    "22025"	: "Invalid escape sequence",
    "22026"	: "String data, length mismatch",
    "23000"	: "Integrity constraint violation",
    "24000"	: "Invalid cursor state",
    "25000"	: "Invalid transaction state",
    "25S01"	: "Transaction state",
    "25S02"	: "Transaction is still active",
    "25S03"	: "Transaction is rolled back",
    "28000"	: "Invalid authorization specification",
    "34000"	: "Invalid cursor name",
    "3C000"	: "Duplicate cursor name",
    "3D000"	: "Invalid catalog name",
    "3F000"	: "Invalid schema name",
    "40001"	: "Serialization failure",
    "40002"	: "Integrity constraint violation",
    "40003"	: "Statement completion unknown",
    "42000"	: "Syntax error or access violation",
    "42S01"	: "Base table or view already exists",
    "42S02"	: "Base table or view not found",
    "42S11"	: "Index already exists",
    "42S12"	: "Index not found",
    "42S21"	: "Column already exists",
    "42S22"	: "Column not found",
    "44000"	: "WITH CHECK OPTION violation",
    "HY000"	: "General error",
    "HY001"	: "Memory allocation error",
    "HY003"	: "Invalid application buffer type",
    "HY004"	: "Invalid SQL data type",
    "HY007"	: "Associated statement is not prepared",
    "HY008"	: "Operation canceled",
    "HY009"	: "Invalid use of null pointer",
    "HY010"	: "Function sequence error",
    "HY011"	: "Attribute cannot be set now",
    "HY012"	: "Invalid transaction operation code",
    "HY013"	: "Memory management error",
    "HY014"	: "Limit on the number of handles exceeded",
    "HY015"	: "No cursor name available",
    "HY016"	: "Cannot modify an implementation row descriptor",
    "HY017"	: "Invalid use of an automatically allocated descriptor handle",
    "HY018"	: "Server declined cancel request",
    "HY019"	: "Non-character and non-binary data sent in pieces",
    "HY020"	: "Attempt to concatenate a null value",
    "HY021"	: "Inconsistent descriptor information",
    "HY024"	: "Invalid attribute value",
    "HY090"	: "Invalid string or buffer length",
    "HY091"	: "Invalid descriptor field identifier",
    "HY092"	: "Invalid attribute/option identifier",
    "HY095"	: "Function type out of range",
    "HY096"	: "Invalid information type",
    "HY097"	: "Column type out of range",
    "HY098"	: "Scope type out of range",
    "HY099"	: "Nullable type out of range",
    "HY100"	: "Uniqueness option type out of range",
    "HY101"	: "Accuracy option type out of range",
    "HY103"	: "Invalid retrieval code",
    "HY104"	: "Invalid precision or scale value",
    "HY105"	: "Invalid parameter type",
    "HY106"	: "Fetch type out of range",
    "HY107"	: "Row value out of range",
    "HY109"	: "Invalid cursor position",
    "HY110"	: "Invalid driver completion",
    "HY111"	: "Invalid bookmark value",
    "HYC00"	: "Optional feature not implemented",
    "HYT00"	: "Timeout expired",
    "HYT01"	: "Connection timeout expired",
    "IM001"	: "Driver does not support this function",
    "IM002"	: "Data source name not found and no default driver specified",
    "IM003"	: "Specified driver could not be loaded",
    "IM004"	: "Driver's SQLAllocHandle on SQL_HANDLE_ENV failed",
    "IM005"	: "Driver's SQLAllocHandle on SQL_HANDLE_DBC failed",
    "IM006"	: "Driver's SQLSetConnectAttr failed",
    "IM007"	: "No data source or driver specified; dialog prohibited",
    "IM008"	: "Dialog failed",
    "IM009"	: "Unable to load translation DLL",
    "IM010"	: "Data source name too long",
    "IM011"	: "Driver name too long",
    "IM012"	: "DRIVER keyword syntax error",
    "IM013"	: "Trace file error",
    "IM014"	: "Invalid name of File DSN",
    "IM015"	: "Corrupt file data source"}

# endregion ODBC errors


# region auth errors

dict_auth = {
    "A001"	: "Username or Email doesn't meet the minimum requirement",
    "A002"	: "Password doesn't meet the minimum requirement",
    "A003"	: "Provided credentials failed authentication",
    "A004"	: "User inactive, please contact Administrator",
    "A005"	: "500 Internal Server Error",
    "A006": "Invalid Tokens"
}

# endregion auth errors

# region Password Reset errors

dict_pwreset = {
    "P001"	: "Password fields cannot be empty!",
    "P002"	: "Password does not meet minimum number of Special characters requirement",
    "P003"	: "Password does not meet minimum number of Non Letters requirement",
    "P004"	: "Password does not meet minimum number of characters requirement",
    "P005"	: "Password does not meet maximum number of characters requirement",
    "P006"	: "Password does not meet minimum number of Uppercase characters requirement",
    "P007": "Password fields must match!"
}

# endregion Password Reset errors


# region REST API HTTP response status code errors

dict_statuscode = {
    "200":   "ok",
    "201":   "created",
    "204":   "no content",
    "400":   "bad request",
    "401":   "unauthorized",
    "403":   "forbidden",
    "404":   "not found",
    "405":   "method not allowed",
    "406":   "not acceptable",
    "409":   "conflict",
    "500":   "internal server error",
    "501":   "not implemented"
}

# endregion REST API HTTP response status code errors
