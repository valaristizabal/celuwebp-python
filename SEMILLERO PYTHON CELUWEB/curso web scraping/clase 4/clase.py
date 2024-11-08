from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

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
    options.add_argument("--no-first-run") #evitar la ejecución de tareas que se ejecutan la primera vez que se abre chrome
    options.add_argument("--no-proxy-server") #para no usar proxy, sino conexiones directas
    options.add_argument("--disable-blink-features=AutomationControlled") #evita que selenium sea detectado / no nos detecta como bot
    
    #PARÁMETROS A OMITIR EN EL INICIO DE CHROMEDRIVER
    exp_opt = [
        'enable-automation', #para que no muestre la notificación "Un software automatizado de pruebas está controlando chrome"
        'ignore-certificate-errors' #para ignorar errores de certificados
        'enable-logging' #para que no se muestre en la terminal "DevTools listening on..."
        ]
    options.add_experimental_option("excludeSwitches", exp_opt)
    
    #PARÁMETROS QUE DEFINEN PREFERENCIAS EN CHROMEDRIVER
    prefs = {
        "profile.default_content_setting_values.notifications" : 2, #notificaciones -> 0=preguntar | 1=permitir | 2= no permitir
        "intl.accept_languages":["es-ES", "es"], #definir el idioma del navegdor
        "credentials_enable_service": False #evita que chrome pregunte si queremos guardar la contraseña al loguearnos
        }
    
    options.add_experimental_option("prefs", prefs)
    
    s = Service(ruta)
    driver = webdriver.Chrome(service=s, options=options)
    return driver

if __name__ == '__main__':
    driver = iniciar_chrome()
    url = "https://clonesyperifericos.com/comprar/memoria-ram-adata-xpg-spectrix-d50-32gb-3200-mhz/"
    driver.get(url)
    #nombre del producto
    nombre = driver.find_element(By.CSS_SELECTOR, ".product_title").text
    print(nombre)
    
    #categoria
    categoria = driver.find_element(By.CSS_SELECTOR, ".woocommerce-breadcrumb").find_elements(By.TAG_NAME, "a")[-1].text
    print(categoria)
    
    #precio anterior
    precio_anterior = driver.find_element(By.CSS_SELECTOR, ".price").find_elements(By.TAG_NAME, "bdi")[0].text.replace("$", "").replace(",", ".")
    print(precio_anterior)
    
    #precio actual
    precio_actual = driver.find_element(By.CSS_SELECTOR, ".price").find_elements(By.TAG_NAME, "bdi")[-1].text.replace("$", "").replace(",", ".")
    print(precio_actual)
    
    #caracteristicas
    caracteristicas = []
    elementos = driver.find_element(By.CSS_SELECTOR, ".woocommerce-product-details__short-description").find_elements(By.TAG_NAME, "p")[-1].text.split("\n")
    for elemento in elementos:
        caracteristicas.append(elemento)
    print(caracteristicas)
    
    #url de la imagen
    url_imagen = driver.find_element(By.CSS_SELECTOR, ".attachment-woocommerce_single").get_attribute("src")
    print(url_imagen)
    input("pulse enter para cerrar")
    driver.quit()