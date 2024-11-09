from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from config_twt import *
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as ec 
from selenium.common.exceptions import TimeoutException 
import pickle 
import os

def iniciar_chrome():
    ruta = ChromeDriverManager().install()
    options = Options()

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    options.add_argument(f"user_agent={user_agent}") 
    options.add_argument("--disable-web-security") 
    options.add_argument("--disable-extensions") 
    options.add_argument("--disable-notifications") 
    options.add_argument("--ignore-certificate-errors") 
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3") 
    options.add_argument("--allow-running-insecure-content") 
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-first-run") 
    options.add_argument("--no-proxy-server") 
    options.add_argument("--disable-blink-features=AutomationControlled") 

    #PARÁMETROS A OMITIR EN EL INICIO DE CHROMEDRIVER
    exp_opt = [
        'enable-automation', 
        'ignore-certificate-errors' 
        'enable-logging' 
        ]
    options.add_experimental_option("excludeSwitches", exp_opt)
    
    #PARÁMETROS QUE DEFINEN PREFERENCIAS EN CHROMEDRIVER
    prefs = {
        "profile.default_content_setting_values.notifications" : 2, 
        "intl.accept_languages":["es-ES", "es"], 
        "credentials_enable_service": False
        }
    
    options.add_experimental_option("prefs", prefs)
    
    s = Service(ruta)
    driver = webdriver.Chrome(service=s, options=options)
    return driver

def login_twt():
    #LOGIN CON COOKIES
    if os.path.isfile("twt.cookies"):
        with open("twt.cookies", "rb") as file:
            cookies = pickle.load(file)
        driver.get("https://x.com/home")
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get("https://x.com/home")
        try:
            articulo = wait.until(ec.visibility_of_element_located((By.TAG_NAME, "article")))
            print("Login con cookies completado!")
        except TimeoutError:
            print("ERROR AL CARGAR EL FEED")
            return "ERRROR"
    #LOGIN DE CERO
    driver.get("https://x.com/i/flow/login")
    #ingresar usuario
    usuario = wait.until(ec.visibility_of_element_located((By.NAME, "text")))
    usuario.send_keys(USER_TWT)
    #darle clic a siguiente
    btnSiguiente = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Siguiente']]")))
    btnSiguiente.click()
    #ingresar contraseña
    contrasena = wait.until(ec.visibility_of_element_located((By.NAME, "password")))
    contrasena.send_keys(PASS_TWT)
    #darle clic a iniciar sesión 
    btnIniciarSesion = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Iniciar sesión']]")))
    btnIniciarSesion.click()
    #validar login exitoso
    try:
        articulo = wait.until(ec.visibility_of_element_located((By.TAG_NAME, "article")))
        print("Login de cero completado!")
    except TimeoutError:
        print("ERROR AL CARGAR EL FEED")
        return "ERRROR"
    
    #guardar cookies
    #cookies = driver.get_cookies
    #pickle.dump(cookies, open("twt.cookies", "wb"))
    #print("cookies guardadas")
    return "OK"


if __name__ == '__main__':
    #iniciar selenium
    driver = iniciar_chrome()
    wait = WebDriverWait(driver, 10)
    #loguear en ig
    res = login_twt()
    if res == "ERROR":
        driver.quit()       
    input("Pulse enter para salir")
    driver.quit()
