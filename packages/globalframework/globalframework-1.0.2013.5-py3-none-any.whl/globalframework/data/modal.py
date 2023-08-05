#Default libraries
import platform

class DatabaseConfiguration:
    def __init__(self, connection: str, timeout: int, driver: str, rdmsprovider: str):
        self.connection = connection
        self.timeout = timeout
        self.driver = driver
        self.rdmsprovider = rdmsprovider


class CacheConfiguration:
    def __init__(self, provider: str, ipaddress: str, ports: str, connection_timeout: str, timeout: str):
        self.provider = provider
        self.ipaddress = ipaddress
        self.ports = ports
        self.connection_timeout = int(connection_timeout)
        self.timeout = int(timeout)


class EmailConfiguration:
    pass

class CloudConfiguration:
    def __init__(self, provider: str, token: str):
        self.provider = provider
        self.token = token


class EnvironmentConfiguration:
    def __init__(self):
        pass

    def get_operating_system(self):
        return platform.system().upper()
