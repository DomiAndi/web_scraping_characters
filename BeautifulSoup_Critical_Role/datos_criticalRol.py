import requests
from bs4 import BeautifulSoup
import pandas as pd

# Lista de URLs de los personajes principales
urls = [
    "https://criticalrole.fandom.com/wiki/Grog_Strongjaw",
    "https://criticalrole.fandom.com/wiki/Keyleth",
    "https://criticalrole.fandom.com/wiki/Percival_de_Rolo",
    "https://criticalrole.fandom.com/wiki/Pike_Trickfoot",
    "https://criticalrole.fandom.com/wiki/Scanlan_Shorthalt",
    "https://criticalrole.fandom.com/wiki/Vax%27ildan",
    "https://criticalrole.fandom.com/wiki/Vex%27ahlia"
]

# Lista para guardar los datos de los personajes
characters = []

# Función para extraer datos de un personaje
def extract_character_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error al acceder a {url}: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraer el nombre del personaje
    name = soup.find("h1", class_="page-header__title").text.strip()

    # Extraer la descripción general
    try:
        description = soup.find("div", class_="mw-parser-output").find("p").text.strip()
    except AttributeError:
        description = "Descripción no disponible"

    # Extraer información adicional de la tabla lateral
    info_table = {}
    try:
        table = soup.find("aside", class_="portable-infobox")
        rows = table.find_all("div", class_="pi-item")
        for row in rows:
            label = row.find("h3", class_="pi-data-label").text.strip()
            value = row.find("div", class_="pi-data-value").text.strip()
            info_table[label] = value
    except AttributeError:
        info_table = {"Información adicional": "No disponible"}

    # Retornar los datos como un diccionario
    return {
        "Nombre": name,
        "Descripción": description,
        **info_table
    }

# Procesar cada URL
for url in urls:
    print(f"Procesando: {url}")
    data = extract_character_data(url)
    if data:
        characters.append(data)

# Convertir los datos a un DataFrame de pandas
df = pd.DataFrame(characters)

# Guardar los datos en un archivo CSV
df.to_csv("personajes_principales.csv", index=False, encoding="utf-8")
print("Datos guardados en personajes_principales.csv")

# Guardar los datos en un archivo JSON
with open("personajes_principales.json", "w", encoding="utf-8") as json_file:
    json.dump(characters, json_file, ensure_ascii=False, indent=4)

print("Datos guardados en personajes_principales.json")