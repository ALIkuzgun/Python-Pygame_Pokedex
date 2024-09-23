import csv
import os
import requests
from bs4 import BeautifulSoup

# URL'yi belirtiyoruz
url = 'https://pokemondb.net/pokedex/all'

# Web sayfasını getiriyoruz
response = requests.get(url)

# BeautifulSoup ile parse ediyoruz
soup = BeautifulSoup(response.content, 'html.parser')

# <tbody> içindeki tüm <tr> öğelerini buluyoruz
tbody = soup.find('tbody')
tr_list = tbody.find_all('tr')

# Görselleri kaydedeceğimiz klasörü kontrol ediyoruz, yoksa oluşturuyoruz
image_folder = 'pokemon-images'
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

# CSV dosyasını oluşturuyoruz ve başlıkları yazıyoruz
with open('pokemon_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Başlık satırını yazıyoruz
    writer.writerow(["Name", "Type", "Total", "HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed", "Image Path"])
    
    # Her bir <tr> öğesinden verileri alıyoruz
    for tr in tr_list:
        # İsim ve varsa alt isim
        cell_name = tr.find('td', class_='cell-name')
        alt_name = cell_name.find('small', class_='text-muted')
        if alt_name:
            name = alt_name.text
        else:
            name = cell_name.find('a').text

        # Tipler
        types = [t.text for t in tr.find_all('a', class_='type-icon')]
        type_combined = '/'.join(types)

        # Statlar (Toplam, HP, Attack, Defense, Sp. Atk, Sp. Def, Speed)
        stats = tr.find_all('td', class_='cell-num')
        total = stats[1].text  # Total değer
        hp = stats[2].text     # HP
        attack = stats[3].text  # Attack
        defense = stats[4].text  # Defense
        sp_atk = stats[5].text  # Sp. Atk
        sp_def = stats[6].text  # Sp. Def
        speed = stats[7].text   # Speed

        # Görseli alıyoruz
        img_tag = tr.find('img', class_='img-fixed icon-pkmn')
        img_url = img_tag['src']  # Resim URL'si
        
        # Görseli indiriyoruz
        img_data = requests.get(img_url).content
        img_filename = os.path.join(image_folder, f"{name}.jpg")  # Kayıt ismi .jpg olacak
        
        # Görseli dosyaya kaydediyoruz
        with open(img_filename, 'wb') as img_file:
            img_file.write(img_data)

        # CSV'ye yazıyoruz
        writer.writerow([name, type_combined, total, hp, attack, defense, sp_atk, sp_def, speed, img_filename])

print("Veriler başarıyla pokemon_data.csv dosyasına ve görseller pokemon-images klasörüne kaydedildi!")
