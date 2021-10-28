from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import json
from time import sleep


def setup_driver():
    """ Setup the firefox webdriver """
    driver_options = webdriver.FirefoxOptions()
    driver_options.headless = True

    return webdriver.Firefox(
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

def rainbow_chain(driver, color, time):
    color_element = driver.find_element(
        By.CSS_SELECTOR,
        f'#message-reactions-884107859179208714 > div:nth-child({color})'\
         ' > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)'
        )

    color_element.click()
    sleep(time)
    color_element.click()


if __name__ == '__main__':
    
    driver = setup_driver()
    discord_channel = 'https://discord.com/channels/864252583584464956/'\
                      '883813770118447224'

    try:
        login(driver)
        sleep(5) # timeout to mark the dc logs as "read"

        # url to server / change-color channel 
        driver.get(discord_channel) 
        sleep(5) # timeout to the channel loading
        
        # run the rainbow chain
        color_list = [color for color in range(1, 13)]
        while True:
            for color in color_list:
                rainbow_chain(driver, color, 3)

    except KeyboardInterrupt:
        pass

    except Exception as e:
        print(e)

    finally:
        driver.quit()

