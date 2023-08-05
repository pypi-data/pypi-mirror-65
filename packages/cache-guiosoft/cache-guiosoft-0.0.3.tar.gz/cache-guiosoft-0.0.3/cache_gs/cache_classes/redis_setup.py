import re

from cache_gs.utils.logging import get_logger


class RedisSetup:
    """ Redis connection string setup     """

    opt_str = {
        'username': None,
        'password': None,
        'client_name': None,
        'encoding': 'utf-8',
        'encoding_errors': 'strict',
        'charset': None,
    }
    opt_int = {
        'db': 0,
        'health_check_interval': 0,
    }
    arguments = {
        'host': 'localhost',
        'port': 6379,
        'socket_timeout': None,
        'socket_connect_timeout': None,
        'socket_keepalive': None,
        'socket_keepalive_options': None,
        'connection_pool': None,
        'unix_socket_path': None,
        'errors': None,
        'decode_responses': False,
        'retry_on_timeout': False,
        'ssl': False,
        'ssl_keyfile': None,
        'ssl_certfile': None,
        'ssl_cert_reqs': 'required',
        'ssl_ca_certs': None,
        'ssl_check_hostname': False,
        'max_connections': None,
        'single_connection_client': False,
        'health_check_interval': 0,
    }

    def __init__(self, connection_string: str):
        connection_string = str(connection_string)

        regex = r"redis:\/\/(.*)?:(\d{4,5})\??(.*)"
        matches = re.match(regex, connection_string)
        if not matches or len(matches.groups()) != 3:
            raise RedisSetupException('Malformed redis connection string')

        self._options = {}
        for opt_set in [self.opt_str, self.opt_int]:
            self._options.update(opt_set)

        host, port, options = matches.groups()
        self.host = host
        self.port = int(port)
        if not (0 < self.port < 65535):
            raise RedisSetupException('Invalid port number ({0})'.format(port))

        self.parse_options(options)

    def parse_options(self, options: str):
        """ Options: username=user&password=1234 """

        for pair in options.split('&'):
            key, value = (pair + '=').split('=')[0:2]
            if key in self.opt_str:
                self.options[key] = None if not value else value

            elif key in self.opt_int:
                try:
                    self.options[key] = int(value)
                except:
                    raise RedisSetupException(
                        "Malformed redis connection string: {0} must have int value".format(key))
            else:
                get_logger().warning(
                    'Redis setup connection string setup key not recognized: {0}'.format(key))

    @property
    def options(self):
        return self._options

    @property
    def encoding(self):
        return self.options.get('encoding', 'utf-8')


class RedisSetupException(Exception):
    pass
