from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from config_chrome_undetectedChromedriver import *
from user_gmail import *
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as ec 
from selenium.webdriver.common.keys import Keys 

if __name__ == '__main__':
    driver = iniciar_webdriver(pos="derecha")
    wait = WebDriverWait(driver, 30)

    driver.get('https://accounts.google.com/')
    #ingresar el correo
    gmail_clic = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[type='email']")))
    gmail_clic.send_keys(GMAIL)
    gmail_clic.send_keys(Keys.ENTER)

    #ingresar la contraseña
    password_clic = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']")))
    password_clic.send_keys(PASSWORD)
    password_clic.send_keys(Keys.ENTER)
    input()
    