import time
from seleniumwire import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def waiting_for_loading(driver: uc, xpath: str):
    for _ in range(20):
        try:
            driver.find_element(By.XPATH, xpath)
        except:
            time.sleep(1)
        else:
            return driver.find_element(By.XPATH, xpath)
    return driver.find_element(By.XPATH, xpath)


class SafetyConfigure:
    def __init__(self, login, password, proxy):
        self.login = login
        self.password = password
        self.proxy = proxy

    def configure(self):
        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--headless')
        wire_options = {
            'proxy': {
                'https': 'http://' + self.proxy
            }
        }
        driver = uc.Chrome(version_main=114, options=chrome_options, seleniumwire_options=wire_options)
        driver.get("https://store.steampowered.com/login/")

        waiting_for_loading(driver,
                            '//*[@id="responsive_page_template_content"]/div[3]/div[1]/div/div/div/div[2]/div/form/div[1]/input').send_keys(
            self.login)
        waiting_for_loading(driver,
                            '//*[@id="responsive_page_template_content"]/div[3]/div[1]/div/div/div/div[2]/div/form/div[2]/input').send_keys(
            self.password)
        waiting_for_loading(driver,
                            '//*[@id="responsive_page_template_content"]/div[3]/div[1]/div/div/div/div[2]/div/form/div[4]/button').click()
        waiting_for_loading(driver, '//*[@id="global_actions"]/a/img').click()
        waiting_for_loading(driver, '//*[@id="btn"]/a').click()
        waiting_for_loading(driver, '//*[@id="react_root"]/div[3]/div[2]/form/div[7]/button[1]').click()

        driver.get('https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/')
        waiting_for_loading(driver, '//*[@id="game_area_purchase"]/div[1]/div[2]/div/div[3]/span').click()

        driver.get('https://store.steampowered.com/app/1172470/Apex_Legends/')
        waiting_for_loading(driver, '//*[@id="game_area_purchase"]/div[1]/div[2]/div/div[3]/span').click()

        driver.get('https://store.steampowered.com/app/578080/PUBG_BATTLEGROUNDS/')
        waiting_for_loading(driver, '//*[@id="game_area_purchase"]/div[1]/div[2]/div/div[3]/span').click()

        time.sleep(2)

        print('DONE.')
