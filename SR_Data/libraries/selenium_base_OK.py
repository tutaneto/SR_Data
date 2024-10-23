# import sys
import time
import random

# from datetime import datetime
# from typing import List

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys


# GLOBAL VARS
gvar = {}


# def ab_exit(message):
#     print(message)
#     sys.exit(-1)

# def ab_error(msg):
#     return -1,msg


def sel_rnd_sleep(base, extra):
    extra = random.uniform(0, extra)
    time.sleep(base + extra)


def sel_wait_for(xpath, timeout=None):
    if timeout == None:
       timeout =  20

    try:
        WebDriverWait(gvar['driver'], timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return 0
    except TimeoutException:
        print("Timeout for " + xpath)
    return -1


def sel_wait_click(xpath, timeout=None):
    sel_wait_for(xpath, timeout)
    sel_rnd_sleep(0.3, 0.2)
    elem = gvar['driver'].find_element(By.XPATH, xpath)
    elem.click()


def sel_wait_value(xpath, timeout=None):
    sel_wait_for(xpath, timeout)
    sel_rnd_sleep(0.3, 0.2)
    elem = gvar['driver'].find_element(By.XPATH, xpath)
    return elem.text


# https://pt.stackoverflow.com/questions/393846/como-acessar-um-iframe-usando-selenium-python
def sel_wait_switch(xpath, timeout=None):
    sel_wait_for(xpath, timeout)
    sel_rnd_sleep(0.3, 0.2)
    elem = gvar['driver'].find_element(By.XPATH, xpath)
    gvar['driver'].switch_to.frame(elem)

def sel_switch_to_default():
    # Retorna para a janela principal (fora do iframe)
    gvar['driver'].switch_to.default_content()


def sel_back(n_pages_back):
    gvar['driver'].execute_script(f"window.history.go({n_pages_back})")


def sel_close():
    # gvar['driver'].close()
    gvar['driver'].quit()


class selenium_connection:
    error=0
    errorMessage=""
    driver:webdriver.Chrome

    def set_error(self,msg):
        self.error=-1
        self.errorMessage=msg
        return self


def sel_conn(connURL):
    conn = selenium_connection()

    fp = open('chromedriver_path.txt', 'r')
    chromedriver_path = fp.readline().strip()
    fp.close()


    # https://stackoverflow.com/questions/31062789/how-to-load-default-profile-in-chrome-using-python-selenium-webdriver
    options = webdriver.ChromeOptions()
    # options.add_argument('user-data-dir=C:/Users/Rogerup/AppData/Local/Google/Chrome/User Data')
    options.add_argument('user-data-dir=C:/Users/Rogerup/AppData/Local/Google/Chrome/User Data Selenium')

    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
    driver.get(connURL)

    conn.driver = driver

    # Global var with conn
    gvar['conn'] = conn
    gvar['driver'] = conn.driver

    return conn
