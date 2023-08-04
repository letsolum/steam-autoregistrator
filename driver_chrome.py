import os
import subprocess
import undetected_chromedriver as uc
from random import choice
from selenium.webdriver.chrome.options import Options


class ChromeBrowser:

    def __set_up(self):
        options = Options()
        _ua = choice(list(map(str.rstrip, open("user_agent_pc.txt").readlines())))
        options.add_argument(f'--user-agent={_ua}')
        # options.add_argument('--headless') # безголовый режим
        self.driver = uc.Chrome(version_main=self.__get_chrome_version, options=options)

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
            output = subprocess.check_output(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'])
            try:
                version = output.decode('utf-8').split()[-1]
                version = version.split(".")[0]
                return version
            except Exception as error:
                raise Exception(f"Chrome Exception: {error}")

    def get_driver(self):
        self.__set_up()
        return self.driver