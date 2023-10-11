import os
import subprocess
from seleniumwire import undetected_chromedriver as uc
from random import choice
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth


class ChromeBrowser:
    def __set_up(self):
        self.options = Options()
        _ua = choice(list(map(str.rstrip, open("user_agent_pc.txt").readlines())))
        self.options.add_argument(f'--user-agent={_ua}')
        self.options.add_argument('--start-maximized')
        # self.options.add_experimental_option('excludeSwitches', ["enable-automation"])
        # self.options.add_argument('--headless=false')
        self.options.add_argument('--ignore-certificate-errors')

        # options.add_argument("--remote-allow-origins=*")
        self.options.add_argument('--headless') # безголовый режим
        proxy_index = 0
        with open('last_proxy.txt') as f:
            proxy_index = int(f.read())
        with open('last_proxy.txt', 'w') as f:
            f.write(str(proxy_index + 1))
        proxy_list = []
        with open('proxy.txt') as f:
            proxy_list = f.read().splitlines()
        proxy_index %= len(proxy_list)
        self.curr_proxy = proxy_list[proxy_index]
        self.wire_options = {
            'proxy': {
                'https': 'http://' + self.curr_proxy
            }
        }
        self.driver = uc.Chrome(seleniumwire_options=self.wire_options, options=self.options, version_main=117)

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

    @property
    def __get_chrome_version(self):
        """Определяет версию chrome в зависимости от платформы"""
        if os.name == 'nt':
            import winreg
            # открываем ключ реестра, содержащий информацию о Google Chrome
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
            # считываем значение ключа "version"
            version = winreg.QueryValueEx(reg_key, "version")[0]
            return version.split(".")[0]
        else:
            output = subprocess.check_output(
                ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'])
            try:
                version = output.decode('utf-8').split()[-1]
                version = version.split(".")[0]
                return version
            except Exception as error:
                raise Exception(f"Chrome Exception: {error}")

    def get_driver(self):
        self.__set_up()
        return self.driver

    def dele(self):
        self.driver.quit()
