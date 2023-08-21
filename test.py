import time

from seleniumwire import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--ignore-certificate-errors')
driver = uc.Chrome(options=options)
driver.get('https://google.com')
time.sleep(100)