from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from config_chrome import *
from user_pinterest import *
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as ec 
from selenium.common.exceptions import TimeoutException 
from selenium.webdriver.common.keys import Keys 
import pickle 
import os
import sys
import wget

def login_pinterest():

    #LOGIN MEDIANTE COOKIES
    if os.path.isfile("pinterest.cookies"):
        with open("pinterest.cookies", "rb") as file:
            cookies = pickle.load(file)
        driver.get("https://es.pinterest.com/robots.txt")
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get("https://es.pinterest.com/")
        #comprobar que el login fue exitoso
        try:
            wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "div[data-test-id='pin']")))
            print("Login por cookies completado!")
            return "OK"
        except TimeoutException:
            print("ERROR AL CARGAR EL FEED")
            return "ERRROR"

    #LOGIN DE CERO
    driver.get("https://es.pinterest.com/")
    #clic a iniciar sesión
    clic_iniciar_sesion = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "div[data-test-id='simple-login-button']")))
    clic_iniciar_sesion.click()

    #escribir credenciales
    input_email = wait.until(ec.visibility_of_element_located((By.ID, "email")))
    input_password = wait.until(ec.visibility_of_element_located((By.ID, "password")))
    input_email.send_keys(EMAIL_PINT)
    input_password.send_keys(PASS_PRINT)

    #iniciar sesión con la cuenta
    clic_iniciar_sesion = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "div[data-test-id='registerFormSubmitButton']")))
    clic_iniciar_sesion.click()

    #clic en aceptar todas las cookies
    #clic_aceptar_cookies = wait.until(ec.element_to_be_clickable((By.XPATH, "//div[text() = 'Aceptar todas']")))
    #clic_aceptar_cookies.click()

    #comprobar que el login fue exitoso
    try:
        wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "div[data-test-id='pin']")))
        print("Login de cero completado!")
    except TimeoutException:
        print("ERROR AL CARGAR EL FEED")
        return "ERRROR"
    
    #guardar las cookies
    cookies = driver.get_cookies()  
    pickle.dump(cookies, open("pinterest.cookies", "wb"))
    print("cookies guardadas")
    return "OK"

def descargar_tablero(usuario, tablero):
    #ir a la url del tablero
    print(f'buscando por el tablero: {tablero} del usuario {usuario}')
    driver.get(f'https://es.pinterest.com/{usuario}/{tablero}')

    #obtener la cantidad de imágenes del tablero
    cantidad_imagenes = int(wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "div[data-test-id='board-summary-container']"))).text.split()[0])
   
   #obtener url de las imagenes
    url_fotos = set() #conjunto de imagenes
    while len(url_fotos) < cantidad_imagenes:
        #scroll
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #elemento de cada imagen en un tablero
        pines = driver.find_elements(By.CSS_SELECTOR, "div[data-test-id='pinrep-image']")
        for pin in pines:
            try:
                #obtener url y añadirla al conjunto
                url = pin.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
                url_fotos.add(url)
            except:
                pass
        print(f'total de elementos: {len(url_fotos)}')

    #descargar las imagenes
    if not os.path.exists(tablero):
        os.mkdir(tablero)
    n = 0
    for url_foto in url_fotos:
        n += 1
        print(f'descargando {n} de {len(url_fotos)}')
        nombre_archivo = wget.download(url_foto, tablero)
    return len(url_fotos)

if __name__ == '__main__':

    #definir modo de uso
    modo_de_uso = f'modo de uso:\n'
    modo_de_uso += f'{os.path.basename(sys.executable)} {sys.argv[0]} usuario tablero-ejemplo\n\n'
    modo_de_uso += f'Ejemplos:\n'
    modo_de_uso += f'nombres de tablero de una sola palabra\n'
    modo_de_uso += f'{os.path.basename(sys.executable)} {sys.argv[0]} xwhyo dibujitos\n'
    modo_de_uso += f'nombres de tablero de varias palabras\n'
    modo_de_uso += f'{os.path.basename(sys.executable)} {sys.argv[0]} xwhyo dibujitos-valeria-prueba\n'
    #controlar parámetros
    if(len(sys.argv) != 3):
        print(modo_de_uso)
        sys.exit(1)
    USUARIO = sys.argv[1]
    TABLERO = sys.argv[2].strip('"')

    driver = iniciar_chrome()
    wait = WebDriverWait(driver, 10)
    res = login_pinterest()
    if res == "ERROR":
        driver.quit()  
    res_descargas = descargar_tablero(USUARIO, TABLERO)
    print(f'han sido descargadas {res_descargas} fotos')
    input("Pulse enter para salir")
    driver.quit()
