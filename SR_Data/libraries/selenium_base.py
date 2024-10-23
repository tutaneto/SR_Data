# import sys
import time
import random
import platform

from .gvar import *

# from datetime import datetime
# from typing import List

# import undetected_chromedriver as uc
# driver = uc.Chrome()

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys


# def ab_exit(message):
#     print(message)
#     sys.exit(-1)

# def ab_error(msg):
#     return -1,msg


def sel_rnd_sleep(base, extra):
    extra = random.uniform(0, extra)
    time.sleep(base + extra)

g_sleep_base, g_sleep_extra = 0.3, 0.2
def sel_rnd_sleep_set(base=0.3, extra=0.2):
    global g_sleep_base, g_sleep_extra
    g_sleep_base, g_sleep_extra = base, extra

def sel_rnd_sleep_fixed():
    if g_sleep_base + g_sleep_extra > 0.01:
        sel_rnd_sleep(g_sleep_base, g_sleep_extra)


def sel_wait_for(xpath, by=By.XPATH, timeout=None, in_elem=None, retry=True):
    if timeout == None:
       timeout =  20

    while True:
        try:
            if in_elem == None: in_elem = gvar['driver']
            WebDriverWait(in_elem, timeout).until(EC.presence_of_element_located((by, xpath)))
            return 0
        except TimeoutException:
            if not retry:
                return -1
            print("\nTimeout for " + xpath)

        gvar['driver'].get(gvar['driver'].current_url)
        gvar['driver'].refresh()
        sel_rnd_sleep(2.0, 0.5)


def sel_wait_click(xpath, by=By.XPATH, timeout=None, in_elem=None, retry=True):
    if in_elem == None: in_elem = gvar['driver']
    ret = sel_wait_for(xpath, by, timeout, in_elem, retry)
    if ret == -1:  # element not found
        return ret
    sel_rnd_sleep_fixed()
    elem = in_elem.find_element(by, xpath)
    try:
        elem.click()
        return 0
    except:
        return -2  # element found, but not interactable

def sel_click(xpath, by=By.XPATH, in_elem=None):
    return sel_wait_click(xpath, by, 0.1, in_elem, False)


def sel_wait_value(xpath, by=By.XPATH, timeout=None, in_elem=None, retry=True):
    if in_elem == None: in_elem = gvar['driver']
    ret = sel_wait_for(xpath, by, timeout, in_elem, retry)
    if ret == -1:
        return ret
    elem = in_elem.find_element(by, xpath)
    return elem.text

def sel_get_value(xpath, by=By.XPATH, in_elem=None):
    return sel_wait_value(xpath, by, 0.1, in_elem, False)


def sel_wait_values(xpath, by=By.XPATH, timeout=None, in_elem=None, retry=True):
    if in_elem == None: in_elem = gvar['driver']
    ret = sel_wait_for(xpath, by, timeout, in_elem, retry)
    if ret == -1:
        return ret
    elems = in_elem.find_elements(by, xpath)
    return elems

def sel_get_values(xpath, by=By.XPATH, in_elem=None):
    return sel_wait_values(xpath, by, 0.1, in_elem, False)


# https://pt.stackoverflow.com/questions/393846/como-acessar-um-iframe-usando-selenium-python
def sel_wait_switch(xpath, timeout=None, retry=True):
    ret = sel_wait_for(xpath, timeout=timeout, retry=retry)
    if ret == -1:
        return ret
    elem = gvar['driver'].find_element(By.XPATH, xpath)
    gvar['driver'].switch_to.frame(elem)
    return 0

def sel_switch_to_default():
    # Retorna para a janela principal (fora do iframe)
    gvar['driver'].switch_to.default_content()


def sel_back(n_pages_back):
    gvar['driver'].execute_script(f"window.history.go({n_pages_back})")


def sel_reload_page():
    # gvar['driver'].get(gvar['driver'].current_url)
    gvar['driver'].refresh()


# https://stackoverflow.com/questions/10629815/how-to-switch-to-new-window-in-selenium-for-python
# https://stackoverflow.com/questions/9588827/how-to-switch-to-the-new-browser-window-which-opens-after-click-on-the-button
def sel_switch_window(window_num):
    gvar['driver'].switch_to.window(gvar['driver'].window_handles[window_num])

def sel_close_window():
    gvar['driver'].close()


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


def sel_conn(connURL, beta=False, headless=False):
    conn = selenium_connection()

    if platform.system() == 'Darwin':
        main_path = '/Users/SR_Prev/'
    else:
        main_path = 'C:/SR_Prev/'

    fp = open(main_path + 'chromedriver_path.txt', 'r')
    chrome_driver_path = fp.readline().strip()
    chrome_user_path = fp.readline().strip()
    if beta:
        chrome_driver_path = fp.readline().strip()
        chrome_user_path = fp.readline().strip()
    fp.close()

    # https://piprogramming.org/articles/How-to-make-Selenium-undetectable-and-stealth--7-Ways-to-hide-your-Bot-Automation-from-Detection-0000000017.html

    # https://stackoverflow.com/questions/31062789/how-to-load-default-profile-in-chrome-using-python-selenium-webdriver
    # https://stackoverflow.com/questions/50635087/how-to-open-a-chrome-profile-through-user-data-dir-argument-of-selenium
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-data-dir={chrome_user_path}')
    if chrome_user_path.endswith('Data'):
        # options.add_argument(f'profile-directory=Profile 2')
        options.add_argument(f'profile-directory=Profile 1')

    # Desliga mensagem de automação
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches",["enable-automation"])
    # options.add_argument("--disable-blink-features=AutomationControlled")

    if headless:
        options.add_argument("--headless")

    if beta:
        options.binary_location = "C:/Program Files/Google/Chrome Beta/Application/chrome.exe"

    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
    # driver = uc.Chrome()

    driver.get(connURL)

    conn.driver = driver

    # Global var with conn
    gvar['conn'  ] = conn
    gvar['driver'] = conn.driver

    return conn
