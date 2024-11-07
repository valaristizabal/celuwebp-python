import requests

#url a la que le haremos la petición
url = "https://www.amazon.es/dp/B079RC2CR8"


#uso de headers en caso de que la página detecte que es python
#headers = {
#    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#}
#lo llamaríamos así en el caso de necesitar personalizar el User-agent
#res = requests.get(url, headers=headers)


#guardar la respuesta del servidor
res = requests.get(url)

res.request #objeto
dir(res.request) #ver funciones variables etc del objeto

#atributos de la petición
res.request.headers #acceder a los headers de nuestra petición
res.request.url #acceder a la url
res.request.path_url #acceder al path de la url

#atributos de la respuesta
res.cookies #cookies
res.headers #headers de la respuesta
res.ok
res.content #body de la rspuesta en byte
res.text #body de la respuesta en string
res.json #body de la respuesta en JSON


#sirve para guardar en un archivo html lo wue retora la respuesta del string
with open("codigo_200.html", "w", encoding="utf-8") as f:
    f.write(res.text)
