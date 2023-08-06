from imagescraperwithbrowser.location import Location
from logdecorator import log_on_start
from selenium import webdriver
from warnings import warn
from logging import INFO


class Browser:
    def __init__(self, config: dict = None):
        self._driver = webdriver.Chrome()
        self.config = config if config is not None else {}

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value: dict):
        supported_config = ['disrespect_robot_rules', 'scroll_step']

        if not isinstance(value, dict):
            raise SystemExit('Configuration should be in dict format.')

        for c in value.keys():
            if c not in supported_config:
                raise SystemExit('Unknown configuration defined: {}'.format(c))

            if c in ['disrespect_robot_rules'] and not isinstance(value[c], bool):
                raise SystemExit('"{}" must be boolean.'.format(c))

        if 'disrespect_robot_rules' not in value.keys():
            value['disrespect_robot_rules'] = False

        if 'scroll_step' not in value.keys():
            value['scroll_step'] = 15

        self._config = value

    @property
    def body_scroll_height(self):
        return self._driver.execute_script('return document.body.scrollHeight')

    @property
    def body_scroll_top(self):
        return self._driver.execute_script('return window.scrollY')

    @property
    def user_agent(self):
        return self._driver.execute_script('return navigator.userAgent')

    @log_on_start(INFO, 'Closing browser')
    def close(self):
        self._driver.close()

    @log_on_start(INFO, 'Going to {location.url:s}')
    def go_to(self, location: Location):
        if not location.is_secure:
            warn('Your connection to "{}" may not be secure.'.format(location.hostname), stacklevel=2)

        robot_rules = location.robot_rules(self.user_agent)

        if not robot_rules['can_fetch'] and not self.config['disrespect_robot_rules']:
            self.close()
            raise SystemExit('"{}/{}" does not allow robots.'.format(location.hostname, location.pathname))

        self._driver.get(url=location.url)

    @log_on_start(INFO, 'Going to {data:s}')
    def go_to_data(self, data):
        self._driver.get(url=data)

    @log_on_start(INFO, 'Scrolling to {height:d}')
    def scroll_to(self, height: int):
        scroll_now = self.body_scroll_top
        scroll_to = height

        while scroll_now < scroll_to:
            self._driver.execute_script('window.scrollTo(0, {})'.format(scroll_now))
            scroll_now += self.config['scroll_step']

    def elements(self, value: str = None, identifier: str = None):
        supported_identifiers = ['tag', 'class']

        if identifier is 'tag':
            return self._driver.find_elements_by_tag_name(value)
        if identifier is 'class':
            return self._driver.find_elements_by_class_name(value)

        raise SystemExit('Identifier can be one of {}.'.format(', '.join(supported_identifiers)))
