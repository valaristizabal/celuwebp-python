#de python
import os
import sys
import time
import pickle
import tempfile

#de terceros
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys 

#propios
from config_chatgpt import *
from config_chrome_undetectedChromedriver import *

class ChatGpt:
    def __init__(self, user, password):
        #iniciar webdriver y loguear en chatgpt
        self.EMAIL = user
        self.PASSWORD = password
        #ruta dnde se guardarán las cookies
        self.COOKIES_FILE = f'{tempfile.gettempdir()}/openai.cookies'
        print("Iniciando webdriver")
        self.driver = iniciar_webdriver(pos="derecha")
        self.wait = WebDriverWait(self.driver, 30)
        #validar que el login fue exitoso
        login = self.login_openai()
        if not login: 
            sys.exit(1)
    #login por cookies o desde cero
    def login_openai(self):

        #LOGIN POR COOKIES
        if os.path.isfile(self.COOKIES_FILE):
            cookies = pickle.load(open(self.COOKIES_FILE, "rb"))
            self.driver.get("https://chatgpt.com/robots.txt")
            for cookie in cookies:
                try:
                    self.driver.add_cookie(cookie)
                except:
                    pass
            self.driver.get("https://chatgpt.com/auth/login")
            login = self.comprobar_login()
            if login:
                print("Login por cookies completado exitosamente")
                return login
            else:
                print("Hubo un error en el login por cookies")


        #LOGIN DE CERO
        self.driver.get("https://chatgpt.com/auth/login")

        #clic panel de opciones:

        #clic en iniciar sesión
        clic_login = self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='login-button']")))
        clic_login.click()

         # #introducir usuario y continuar
        input_gmail = self.wait.until(ec.element_to_be_clickable((By.ID, "email-input")))
        input_gmail.send_keys(self.EMAIL)

         # #clic a siguiente
        clic_siguente = self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button.continue-btn")))
        clic_siguente.click()

        # #ingresar la contraseña
        input_password = self.wait.until(ec.element_to_be_clickable((By.ID, "password")))
        input_password.send_keys(self.PASSWORD)

        # clic a continuar
        clic_continuar = self.wait.until(ec.element_to_be_clickable((By.NAME, "action")))
        clic_continuar.click()

        login = self.comprobar_login()
        if login:
            #guardar cookies en caso de que el login sea exitoso
            with open(self.COOKIES_FILE, "wb") as f:
             pickle.dump(self.driver.get_cookies(), f)

            print("Login desde cero completado exitosamente")
        else:
            print("Hubo un error en el login desde cero")
        return login
    
    def comprobar_login(self, tiempo = 30):
        login = False
        while tiempo > 0:
            try:
                input = self.driver.find_element(By.ID, "prompt-textarea")
                input.click()
                login = True
                break
            except:
                pass
            tiempo -= 1
        return login
    
    def enviar_mensaje(self, prompt):
      #enviar mensaje
        input = self.driver.find_element(By.ID, "prompt-textarea")
        input.send_keys(prompt)
        boton_enviar = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='send-button']")
        boton_enviar.click()

        #recibir respuesta
        respuesta = ""
        inicio = time.time()
        while True:
            e = self.driver.find_elements(By.CSS_SELECTOR, "div.markdown")[-1]
            respuesta = e.text
            try: 
                #elemento de botón cuadrado cuando se genera la respuesta
                cargando = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='stop-button']")
                #si existe es porque recién se está generando la respuesta
            except:
                #si ya no existen, es porque la repuesta ya fue generada
                if respuesta:
                    break
            segundos = int(time.time() - inicio)
            if segundos:
                print("generando respuesta... " + segundos + " segundos")
                time.sleep(1)
            
        print(f'repuesta generada en {segundos} segundos')
        respuesta = e.text
        return respuesta
            
    def cerrar(self):
        print(f'cerrando webdriver')
    
if __name__ == '__main__':
    gpt = ChatGpt(EMAIL, PASSWORD)
    while True: 
        prompt = input(f'Prompt (S=Salir)')
        if prompt == 'S':
            sys.exit()
        else:
            respuesta = gpt.enviar_mensaje(prompt)
            print(respuesta)