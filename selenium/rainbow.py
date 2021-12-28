from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from random import shuffle
from time import sleep
import json


def setup_driver():
    """ Setup the firefox driver """
    driver_options = webdriver.FirefoxOptions()
    driver_options.headless = True

    return webdriver.Firefox(
        options=driver_options
        )

def setup_chrome_driver():
    """ Setup the chrome driver """
    driver_options = webdriver.ChromeOptions()
    driver_options.headless = True

    return webdriver.Chrome(
        options=driver_options
        )

def login(driver):
    """ Perform login """
    # My secret data
    secret_file = open('secret.json', 'r')
    data = json.load(secret_file)

    email = data['email']
    password = data['password']

    driver.get('https://discord.com/login')  
    
    # getting elements 
    email_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//input[@name='email']")
            )
        )
    password_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//input[@name='password']")
            )
        ) 
     
    email_element.send_keys(email)
    password_element.send_keys(password, Keys.ENTER)

def rainbow_chain(driver, color, time, previous=None):
    """ Perform a click on a given color """
    color_element = driver.find_element(
        By.CSS_SELECTOR,
        f'#message-reactions-884107859179208714 > div:nth-child({color})'\
         ' > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)'
        )
        
    color_element.click()
    if previous:
        previous.click()
    sleep(time)
    return color_element


if __name__ == '__main__':
    driver = setup_chrome_driver()

    discord_channel = 'https://discord.com/channels/864252583584464956/'\
                      '883813770118447224'

    try:
        login(driver)
        sleep(10)

        # url to server / change-color channel 
        driver.get(discord_channel) 
        sleep(10)
        
        previous = None
        while True:
            # color_list = [color for color in range(1, 13)]       
            # shuffle(color_list)
            
            color_list = [3, 12] 

            for color in color_list:
                element = rainbow_chain(driver, color, 3, previous)
                previous = element 

    except KeyboardInterrupt:
        pass

    except Exception as e:
        print(e)

    finally:
        driver.quit()

