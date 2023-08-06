from urllib.parse import urlencode
from urllib.robotparser import RobotFileParser


class Location:
    def __init__(self, hostname: str, pathname: str = '', params: dict = None, protocol: str = 'https'):
        self.hostname = hostname
        self.pathname = pathname
        self.protocol = protocol

        self.params = params or {}

    @property
    def hostname(self):
        return self._hostname

    @hostname.setter
    def hostname(self, value: str):
        if not isinstance(value, str):
            raise SystemExit('Hostname should be string.')

        self._hostname = value

    @property
    def pathname(self):
        return self._pathname

    @pathname.setter
    def pathname(self, value: str):
        if not isinstance(value, str):
            raise SystemExit('Pathname should be string.')

        self._pathname = value

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, value: dict):
        if not isinstance(value, dict):
            raise SystemExit('Parameters should be in dict format.')

        self._params = value

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, value: str):
        allowed_protocols = ['http', 'https']

        if value not in allowed_protocols:
            raise SystemExit('Protocol can be one of {}.'.format(', '.join(allowed_protocols)))

        self._protocol = value

    @property
    def url(self):
        return '{protocol}://{hostname}/{pathname}?{params}'.format(
            protocol=self.protocol,
            hostname=self.hostname,
            pathname=self.pathname,
            params=urlencode(self.params)
        )

    @property
    def url_robots(self):
        return '{protocol}://{hostname}/robots.txt'.format(
            protocol=self.protocol,
            hostname=self.hostname,
        )

    @property
    def is_secure(self):
        return self.protocol is 'https'

    def robot_rules(self, user_agent: str):
        robot_parser = RobotFileParser(url=self.url_robots)
        robot_parser.read()

        return {
            'can_fetch': robot_parser.can_fetch(user_agent, self.url),
            'crawl_delay': robot_parser.crawl_delay(user_agent),
            'request_rate': robot_parser.request_rate(user_agent),
        }
