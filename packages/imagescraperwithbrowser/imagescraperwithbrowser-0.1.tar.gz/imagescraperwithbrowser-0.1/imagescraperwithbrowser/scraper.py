from imagescraperwithbrowser.location import Location
from imagescraperwithbrowser.browser import Browser
from logdecorator import log_on_start
from logging import INFO
from time import sleep
from tqdm import tqdm


class Scraper:
    def __init__(self, location: Location, browser: Browser, config: dict = None):
        self._location = location
        self._browser = browser
        self.config = config or {}

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value: dict):
        supported_config = ['img_min_height', 'img_min_width', 'save_dir', 'max_img_count', 'sleep_time']

        if not isinstance(value, dict):
            raise SystemExit('Configuration should be in dict format.')

        for c in value.keys():
            if c not in supported_config:
                raise SystemExit('Unknown configuration defined: {}'.format(c))

            if c in ['img_min_height', 'img_min_width'] and not isinstance(value[c], int):
                raise SystemExit('"{}" must be integer.'.format(c))

            if c in ['save_dir'] and not isinstance(value[c], str):
                raise SystemExit('"{}" must be string.'.format(c))

            if c in ['sleep_time'] and not isinstance(value[c], (int, float)):
                raise SystemExit('"{}" must be numerical.'.format(c))

        if 'save_dir' not in value.keys():
            value['save_dir'] = 'images'
        else:
            value['save_dir'] = value['save_dir'].replace(' ', '_')

        self._config = value

    @log_on_start(INFO, 'Finding images')
    def find_images(self):
        images = self._browser.elements('img', 'tag')

        if 'img_min_height' in self._config:
            images = list(filter(lambda image: image.get_property('height') > self._config['img_min_height'], images))
        if 'img_min_width' in self._config:
            images = list(filter(lambda image: image.get_property('height') > self._config['img_min_width'], images))

        return images

    @log_on_start(INFO, 'Saving images')
    def save_images(self, images):
        from urllib.request import urlretrieve
        from os.path import isdir
        from os import makedirs

        if not isdir(self.config['save_dir']):
            makedirs(self.config['save_dir'])

        images = images[:self.config['max_img_count']]
        for index, image in enumerate(tqdm(images)):
            image_src = image.get_attribute('src') or image.get_attribute('data-src')
            image_name = '{save_dir}/{i}.png'.format(save_dir=self.config['save_dir'], i=index)

            try:
                urlretrieve(image_src, image_name)
                sleep(self.config['sleep_time'])
            except:
                continue

    def run(self):
        self._browser.go_to(location=self._location)

        images = []
        body_scroll_height = 0

        while len(images) < self.config['max_img_count']:
            images = self.find_images()

            body_scroll_height_new = self._browser.body_scroll_height
            if body_scroll_height_new > body_scroll_height:
                body_scroll_height = body_scroll_height_new
                self._browser.scroll_to(body_scroll_height)
            else:
                break

            sleep(self.config['sleep_time'])

        self.save_images(images)

        self._browser.close()
