from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from config_instagram import *
from selenium.webdriver.support.ui import WebDriverWait #esperar por elementos en sentium
from selenium.webdriver.support import expected_conditions as ec #condiciones en sentium
from selenium.common.exceptions import TimeoutException #excepción de timeout en sentium
from selenium.webdriver.common.keys import Keys #para pulsar teclas especiales
import pickle #guardar/cargar las cookies
import os
import sys
import wget

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

def login_instagram():

    #LOGIN CON COOKIES
    #validar si existe el archivo
    if os.path.isfile("instagram.cookies"):
        #leer el archivo si existe
        with open("instagram.cookies", "rb") as file:
            cookies = pickle.load(file)
        #cargar robots.txt
        driver.get("https://www.instagram.com/robots.txt")
        #recorrer cookies para ir añadiendo al driver
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get("https://www.instagram.com/")
        #comprobar que el login fue exitoso
        try:
            articulo = wait.until(ec.visibility_of_element_located((By.TAG_NAME, "article")))
            print("Login por cookies completado!")
            return "OK"
        except TimeoutException:
            print("ERROR AL CARGAR EL FEED")
            return "ERRROR"
    #LOGIN DESDE CERO
    driver.get("https://www.instagram.com/")

    wait.until(ec.visibility_of_element_located((By.NAME, "username")))
    #encontrar el campo de username
    usuario = driver.find_element(By.NAME, "username")
    #escribir en el campo username
    usuario.send_keys(USER_IG)
    #encontrar el campo password
    wait.until(ec.visibility_of_element_located((By.NAME, "password")))
    contrasena = driver.find_element(By.NAME, "password")
    #esribir en el campo password
    contrasena.send_keys(PASS_IG)
    #darlle a inciiar sesión
    iniciarSesion = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    iniciarSesion.click()
    #darle a guardar información
    guardarInformacion = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[text() ='Guardar información']")))
    guardarInformacion.click()
    #comprobar que el login fue exitoso
    try:
        articulo = wait.until(ec.visibility_of_element_located((By.TAG_NAME, "article")))
        print("Login de cero completado!")
    except TimeoutException:
        print("ERROR AL CARGAR EL FEED")
        return "ERRROR"
    #guardar las cookies
    cookies = driver.get_cookies()  
    #guarda las cookies en el arcivo instagram.cookies de modo escritura binario
    pickle.dump(cookies, open("instagram.cookies", "wb"))
    print("cookies guardadas")
    return "OK"

def descargar_fotos_instagram(hashtag, minimo):
    print(f'buscando por el #{hashtag}')
    driver.get(f'https://www.instagram.com/explore/search/keyword/?q=%23{hashtag}')
    url_fotos = set() #conjunto donde se irán añadiendo los enlaces de las fotos
    while len(url_fotos) < minimo:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        elementos = driver.find_elements(By.CSS_SELECTOR, "div._aagu")
        for elemento in elementos:
            try:
                url = elemento.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
                url_fotos.add(url)
            except:
                pass 
        print(f'total de elementos: {len(url_fotos)}')
        
    if not os.path.exists(hashtag):
        os.mkdir(hashtag)
        n = 0
    for url_foto in url_fotos:
        n += 1
        print(f'descargando {n} de {len(url_fotos)}')
        nombre_archivo = wget.download(url_foto, hashtag)
    return len(url_fotos)


if __name__ == '__main__':

    #definir modo de uso
    modo_de_uso = f'modo de uso:\n'
    modo_de_uso += f'{os.path.basename(sys.executable)} {sys.argv[0]} hashtag [minimo]\n\n'
    modo_de_uso += f'Ejemplos:\n'
    modo_de_uso += f'{os.path.basename(sys.executable)} {sys.argv[0]} cats\n'
    modo_de_uso += f'{os.path.basename(sys.executable)} {sys.argv[0]} superman 100\n'
    #controlar parámetros
    if(len(sys.argv) == 1  or len(sys.argv) > 3):
        print(modo_de_uso)
        sys.exit(1)
    elif len(sys.argv) == 3:
        if sys.argv[2].isdigit():
            MINIMO = int(sys.argv[2])
        else:
            print(f'{sys.argv[2]} no es un número')
            sys.exit(1)
    else:
        MINIMO = 300
    HASHTAG = sys.argv[1].strip('#')

    #iniciar selenium
    driver = iniciar_chrome()
    wait = WebDriverWait(driver, 10)
    #loguear en ig
    res = login_instagram()
    if res == "ERROR":
        driver.quit()     
    res_descargas = descargar_fotos_instagram(HASHTAG, MINIMO)  
    print(f'han sido descargadas {res_descargas} fotos')
    input("Pulse enter para salir")
    driver.quit()
