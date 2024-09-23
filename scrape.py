import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time 

"""
 Scraping pokemon images from --> https://pokemondb.net/pokedex/all
"""

# İndirme klasörünü oluştur
download_folder = "pokemon-images"
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Site URL'si
url =  "https://pokemondb.net/pokedex/all"

# Siteye istek gönder ve içeriği al
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Belirtilen class'a sahip img etiketlerini bul
img_tags = soup.find_all("img", class_="img-fixed icon-pkmn")

# Resim dosyalarını indir
for img in img_tags:
    img_url = img.get("src")
    
    # Tam URL'yi oluştur (göreceli URL'leri tam URL'ye çevirir)
    img_url = urljoin(url, img_url)
    
    # Resim ismini al
    img_name = os.path.basename(img_url)
    
    # Resmi indir
    img_data = requests.get(img_url).content
    with open(os.path.join(download_folder, img_name), "wb") as img_file:
        img_file.write(img_data)
    
    print(f"{img_name} indirildi.")

    time.sleep(0.1)

print("Belirtilen class'a sahip tüm resimler indirildi!")
