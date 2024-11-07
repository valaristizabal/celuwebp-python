from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

#inicia chrome con los parámetros indicados y devuelve el driver
def iniciar_chrome():
    #se instala la versión de chromedriver correspondiente
    ruta = ChromeDriverManager().install()
    #instanciamos options (opciones de chrome)
    options = Options()
    #definir el user_agent
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    options.add_argument(f"user_agent={user_agent}") #se agrega el argumento
    options.add_argument("--disable-web-security") #deshabilida el web security
    options.add_argument("--disable-extensions") #para que no carguen las extensiones de google
    options.add_argument("--disable-notifications") #para bloquear las comunicaciones de chrome
    options.add_argument("--ignore-certificate-errors") #para ignorar el aviso de "su conexión no es privada"
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3") #para que chromedriver no muestre nada en la terminal
    options.add_argument("--allow-running-insecure-content") #evitar el aviso de que "contenido no seguro"
    options.add_argument("--no-default-browser-check") #evitar el aviso de que chrome no es el navegador por defecto
    