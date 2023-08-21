from selenium.webdriver.support import expected_conditions as EC
from driver_chrome import ChromeBrowser
from selenium_recaptcha_solver import RecaptchaSolver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from typing import Optional
import random
import time
from email_confirm import EmailConf
from configure_account import SafetyConfigure


def waiting_for_element(driver, by_what, path):
    for _ in range(20):
        try:
            driver.find_element(by_what, path)
        except:
            time.sleep(1)
        else:
            return driver.find_element(by_what, path)
    return driver.find_element(by_what, path)

class CustomRecaptchaSolver(RecaptchaSolver):
    def click_recaptcha_v2(self, iframe: WebElement, by_selector: Optional[str] = None) -> None:
        if isinstance(iframe, str):
            WebDriverWait(self._driver, 150).until(
                ec.frame_to_be_available_and_switch_to_it((by_selector, iframe)))

        else:
            self._driver.switch_to.frame(iframe)

        checkbox = self._wait_for_element(
            by='id',
            locator='recaptcha-anchor',
            timeout=150,
        )

        self._js_click(checkbox)

        if checkbox.get_attribute('aria-checked') == 'true':
            return

        if self._delay_config:
            self._delay_config.delay_after_click_checkbox()

        self._driver.switch_to.parent_frame()

        captcha_challenge = self._wait_for_element(
            by=By.CSS_SELECTOR,
            locator='iframe[src*="ttps://google.com/recaptcha/enterprise"]',
            timeout=5,
        )
        time.sleep(4)
        self.solve_recaptcha_v2_challenge(iframe=captcha_challenge)

    def solve_recaptcha_v2_challenge(self, iframe: WebElement) -> None:
        iframe = \
            self._driver.find_elements(By.CSS_SELECTOR, 'iframe[src*="ttps://google.com/recaptcha/enterprise"]')[1]
        self._driver.switch_to.frame(iframe)

        time.sleep(1.5)
        try:
            self._wait_for_element(
                by=By.XPATH,
                locator='//*[@id="recaptcha-audio-button"]',
                timeout=1,
            ).click()

        except TimeoutException:
            print("Didn't find audio-button!")
            pass
        time.sleep(1.5)
        self._solve_audio_challenge('language')
        time.sleep(1.5)
        # Locate verify button and click it via JavaScript
        verify_button = self._wait_for_element(
            by=By.ID,
            locator='recaptcha-verify-button',
            timeout=5,
        )

        self._js_click(verify_button)

        if self._delay_config:
            self._delay_config.delay_after_click_verify_button()

        try:
            self._wait_for_element(
                by=By.XPATH,
                locator='//div[normalize-space()="Multiple correct solutions required - please solve more."]',
                timeout=1,
            )

            self._solve_audio_challenge()

            # Locate verify button again to avoid stale element reference and click it via JavaScript
            second_verify_button = self._wait_for_element(
                by=By.ID,
                locator='recaptcha-verify-button',
                timeout=5,
            )

            self._js_click(second_verify_button)

        except TimeoutException:
            pass

        self._driver.switch_to.parent_frame()


class RegisterSteam:
    def __init__(self, em, pswrd):
        brwsr = ChromeBrowser()
        self.driver = brwsr.get_driver()
        self.proxy = brwsr.get_proxy()
        self.mailconf = EmailConf()
        self.email = em
        self.password = pswrd

    def _get_url(self):
        self.driver.get("https://store.steampowered.com/join")

    def _solve_captcha(self):
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//iframe[@title="reCAPTCHA"]')))
        recaptcha_iframe = self.driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
        solver = CustomRecaptchaSolver(driver=self.driver)
        solver.click_recaptcha_v2(iframe=recaptcha_iframe)

    def __send_keys_as_human(self, where, what):
        for symb in what:
            waiting_for_element(self.driver, By.CSS_SELECTOR, where).send_keys(symb)
            time.sleep(1 / 10 + random.randint(0, 10) / 100 * (random.randint(1, 3) - 2))

    def _insert_data(self):
        waiting_for_element(self.driver, By.CSS_SELECTOR, "#i_agree_check").click()
        self.__send_keys_as_human("#email", self.email)
        self.__send_keys_as_human("#reenter_email", self.email)
        time.sleep(1.5)

    def _generate_data(self):
        with open('accounts.txt', 'a') as f:
            login = self.email[:self.email.find('@')]
            passw = ''
            for _ in range(10):
                symb = ''
                if random.randint(1, 2) == 1:
                    symb = str(random.randint(0, 9))
                else:
                    symb = chr(ord('a') + random.randint(0, 25))
                passw += symb
            passw += '_SD'
            f.write(self.email + ':' + self.password + ':' + login + ':' + passw + '\n')
        waiting_for_element(self.driver, By.CSS_SELECTOR, "#accountname").send_keys(login)
        waiting_for_element(self.driver, By.CSS_SELECTOR, "#password").send_keys(passw)
        waiting_for_element(self.driver, By.CSS_SELECTOR, "#reenter_password").send_keys(passw)
        waiting_for_element(self.driver, By.CSS_SELECTOR, "#createAccountButton").click()
        return login, passw

    def new_register(self):
        self._get_url()
        time.sleep(1)
        self._insert_data()
        #self._solve_captcha()
        time.sleep(20)
        waiting_for_element(self.driver, By.CSS_SELECTOR, "#createAccountButton").click()
        if not self.mailconf.confirm(self.email, self.password, self.proxy):
            return False
        time.sleep(5)
        data = self._generate_data()
        conf = SafetyConfigure(data[0], data[1], self.proxy)
        conf.configure()
        return True

    def clear(self):
        self.driver.quit()
