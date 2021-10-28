from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


def setup_driver():
    driver_options = webdriver.FirefoxOptions()
    driver_options.headless = False

    return webdriver.Firefox(
        options=driver_options
        )

def login(driver):
    

if __name__ == '__main__':
    setup_driver()

    try:
    
    except Exception as e:
        print(e)

