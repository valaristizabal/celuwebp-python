from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from config_chrome import *
from user_wattpad import *
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as ec 
from selenium.common.exceptions import TimeoutException 
from selenium.webdriver.common.keys import Keys 
import pickle 
import os
import wget
import time
from flask import Flask, request, render_template

app = Flask(__name__)

def login_wattpad(driver, wait):
    driver.get("https://www.wattpad.com/login")
    clic_iniciar_sesion = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, ".submit-btn-new"))).clic()
    


@app.route('/buscar', methods=['POST'])
def buscar():
    
    driver = iniciar_chrome()
    wait = WebDriverWait(driver, 10)

if __name__ == "__main__":

    app.run(debug=True)    
