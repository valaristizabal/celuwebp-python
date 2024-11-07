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

#obtener el titulo
soup.title.text

#obtener el título de la página
print(soup.find("h1", class_="product-heading__title").text)

#obtener el precio
print(soup.find("h2", class_="product-heading__pricing")) #obtener todo el h2 que incluye los span 
soup.find("h2", class_="product-heading__pricing").find("span").text #obtener el primer span (precio actual) en texto

#preparar el text para pasarlo a formato numérico
print(soup.find("h2", class_="product-heading__pricing").find("span").text.replace("$", "").replace("COP", ""))

#pasarlo a float
float(soup.find("h2", class_="product-heading__pricing").find("span").text.replace("$", "").replace("COP", "")) 

