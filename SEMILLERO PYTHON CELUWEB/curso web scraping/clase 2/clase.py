import requests
from bs4 import BeautifulSoup


url = "https://www.tiendagamermedellin.co/precog-s-35-mm-negra-xpg"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

#petición
res = requests.get(url, headers=headers)
res.status_code #verificar que todo salió bien

#objeto beautifulSoup
soup = BeautifulSoup(res.text, "html.parser")

#obtener el titulo!
soup.title.text

#obtener el título de la página
print(soup.find("h1", class_="product-heading__title").text)

#obtener el precio!
soup.find("h2", class_="product-heading__pricing") #obtener todo el h2 que incluye los span 
soup.find("h2", class_="product-heading__pricing").find("span").text #obtener el primer span (precio actual) en texto

#preparar el text para pasarlo a formato numérico
soup.find("h2", class_="product-heading__pricing").find("span").text.replace("$", "").replace("COP", "")

#pasarlo a float
float(soup.find("h2", class_="product-heading__pricing").find("span").text.replace("$", "").replace("COP", "")) 

#obtener categoría!
soup.find("span", class_="product-heading__brand").text

#obtener la descripción
soup.find("h3", class_="product-description__content").find_all("li") #obtener todos los li del h3
soup.find("h3", class_="product-description__content").find_all("li")[0] #podemos acceder a cada elemento por su indice

descripciones = []
elementos = soup.find("h3", class_="product-description__content").find_all("li") #Almacdenamos los li en una variable


#recorremos la lista elementos y los vamos añadiendo a la lista de descripciones
for elemento in elementos:
    descripciones.append(elemento.text)

print(descripciones)
#obtener enlace de la imagen!
soup.find("img", {"class":"product-gallery__image"}).attrs
soup.find("img", {"class":"product-gallery__image"}).attrs.get("src")

#obtener id del producto!
print(url.split("/")[-1])