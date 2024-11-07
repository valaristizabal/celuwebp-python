from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

ruta = ChromeDriverManager().install() #instalará chromedriver en el directorio determinado
#print("ChromeDriver instalado en:", ruta)

s = Service(ruta)
driver = webdriver.Chrome(service = s)

#url de la página a scrapear
url = "https://clonesyperifericos.com/comprar/memoria-ram-adata-xpg-spectrix-d50-32gb-3200-mhz/"
driver.get(url)
#acceder al HTML
driver.page_source

#objeto beautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

#nombre del producto
print(soup.find("h1", class_ = "product_title").text)

#categoria
print(soup.find("nav", class_ ="woocommerce-breadcrumb").find_all("a")[-1].text)

#precio anterior
print(float(soup.find("p", class_ ="price").find_all("bdi")[0].text.replace("$", "").replace(",", ".")))

#precio actual
print(float(soup.find("p", class_ ="price").find_all("bdi")[-1].text.replace("$", "").replace(",", ".")))

#caracteristicas
caracteristicas = []
elementos = soup.find("div", class_ = "woocommerce-product-details__short-description").find_all("p")[-1].text.split("\n")
for elemento in elementos:
    caracteristicas.append(elemento)
    
#url de la imagen

print(soup.find("img", class_ ="attachment-woocommerce_single").attrs.get("src"))

#hacer que no se cierre la página de chrome sola
input("Presiona Enter para cerrar el navegador...")


