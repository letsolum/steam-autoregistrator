import os
import subprocess
from seleniumwire import undetected_chromedriver as uc
from random import choice
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth


class ChromeBrowser:
    def __init__(self, headless=True):
        self.__headless_mode = headless

    def __set_up(self):
        self.options = Options()
        _ua = choice(list(map(str.rstrip, open("../data/user_agent_pc.txt").readlines())))
        self.options.add_argument(f'--user-agent={_ua}')
        self.options.add_argument('--start-maximized')
        # self.options.add_experimental_option('excludeSwitches', ["enable-automation"])
        # self.options.add_argument('--headless=false')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument("--disable-blink-features")
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        # self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # self.options.add_experimental_option('useAutomationExtension', False)
        # options.add_argument("--remote-allow-origins=*")
        if self.__headless_mode:
            self.options.add_argument('--headless')  # безголовый режим
        proxy_index = 0
        with open('../data/last_proxy.txt') as f:
            proxy_index = int(f.read())
        with open('../data/last_proxy.txt', 'w') as f:
            f.write(str(proxy_index + 1))
        proxy_list = []
        with open('../data/proxy.txt') as f:
            proxy_list = f.read().splitlines()
        proxy_index %= len(proxy_list)
        self.curr_proxy = proxy_list[proxy_index]
        self.wire_options = {
            'proxy': {
                'https': 'http://' + self.curr_proxy
            }
        }
        #
        self.driver = uc.Chrome(seleniumwire_options=self.wire_options, options=self.options, version_main=117)
        self.driver.execute_script("""
           Object.defineProperty(navigator, 'deviceMemory', {
                 get: () => 8
           });
           Object.defineProperty(navigator, 'hardwareConcurrency', {
	             get: () => 8
           });
    """)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

    def get_proxy(self):
        return self.curr_proxy

    def get_driver(self):
        self.__set_up()
        return self.driver
