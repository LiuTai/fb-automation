import os
import random
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys


def randmized_sleep(average=1):
    _min, _max = average * 1 / 2, average * 3 / 2
    sleep(random.uniform(_min, _max))


class Browser:
    def __init__(self, has_screen):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        service_args = ["--ignore-ssl-errors=true"]
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--no-sandbox")
        if not has_screen:
            chrome_options.add_argument("--headless")
        print("%s/bin/chromedriver" % dir_path)
        self.driver = webdriver.Chrome(
            executable_path="%s/bin/chromedriver" % dir_path,
            service_args=service_args,
            chrome_options=chrome_options,
        )

    def get(self, url):
        self.driver.get(url)

    def current_url(self):
        return self.driver.current_url
    
    def find_one(self, css_selector, elem=None, waittime=0):
        obj = elem or self.driver

        if waittime:
          randmized_sleep(waittime)

        try:
            return obj.find_element(By.CSS_SELECTOR, css_selector)
        except NoSuchElementException:
            return None

    def find_by_id(self, id_selector, elem=None, waittime=0):
        obj = elem or self.driver

        if waittime:
          randmized_sleep(waittime)

        try:
            return obj.find_element(By.ID, id_selector)
        except NoSuchElementException:
            return None

    def find_by_tag(self, tag_selector, elem=None, waittime=0):
        obj = elem or self.driver

        if waittime:
          randmized_sleep(waittime)

        try:
            return obj.find_elements(By.TAG_NAME, tag_selector)
        except NoSuchElementException:
            return None

    def find_all(self, css_selector, elem=None, waittime=0):
        obj = elem or self.driver

        if waittime:
          randmized_sleep(waittime)

        try:
            return obj.find_elements(By.CSS_SELECTOR, css_selector)
        except NoSuchElementException:
            return None


    def js_click(self, elem):
        self.driver.execute_script("arguments[0].click();", elem)


    def click(self, elem=None, waittime=0):
        obj = elem or self.driver
        try:
            res = obj.click()
            if waittime:
                randmized_sleep(waittime)
            return res
        except NoSuchElementException:
            return None

    def open_new_tab(self, url):
        self.driver.execute_script("window.open('%s');" %url)
        self.driver.switch_to.window(self.driver.window_handles[1])

    def close_current_tab(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def __del__(self):
        try:
          self.driver.quit()
        except Exception:
          pass