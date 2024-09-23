import pygame
import pandas as pd
from pokemon import *
import os 

# Load Pokémon data
pokemon_value = pd.read_csv('All_Pokemon.csv')

pygame.init()

# ekran değişkenleri
width = 390
height = 540

ekran = pygame.display.set_mode((width, height))
pygame.display.set_caption('Mini Pokedex')
font = pygame.font.Font("ShareTechMono-Regular.ttf", 26)
pygame.display.set_icon(pygame.image.load('pokeball.png'))

input_text = ""

pokemon = Pokemon(x=90, y=110, en=100, boy=100)

# pokemon value yazdır
def get_pokemon_stats(name):
    row = pokemon_value[pokemon_value['Name'].str.lower() == name.lower()]
    if not row.empty:
        stats = row.iloc[0]
        return {
            'hp': stats['HP'],
            'attack': stats['Att'],
            'defense': stats['Def'],
            'special_attack': stats['Spa'],
            'special_defense': stats['Spd'],
            'speed': stats['Spe']
        }
    return None

# pokemonları çizdir
def pokemon_draw():
    if input_text.lower() in pokemon_value['Name'].str.lower().values:
        stats = get_pokemon_stats(input_text)
        if stats:
            # metin girişine göre pokemonu çiz 
            img_name = f'pokemon-images/{input_text.lower()}.jpg'
            
            if os.path.exists(img_name):
                pokemon.image = pygame.image.load(img_name)

            pokemon.image = pygame.transform.scale(pokemon.image, (240, 228)) 
            pokemon.x = 60
            pokemon.y = 40
            pokemon.draw(ekran)
            
            y_offset = 320
            for stat, value in stats.items():
                stat_text = font.render(f"{stat.replace('_', ' ').title()}: {value}", True, (0, 0, 0))
                ekran.blit(stat_text, (90, y_offset))
                y_offset += 30

# oyun döngüsü
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # metin girişi
        elif event.type == pygame.KEYDOWN:
            if len(input_text) < 20:
                if event.key == pygame.K_RETURN:
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode 

    # ekrana çizdir
    ekran.fill((255, 0, 0))
    pygame.draw.rect(ekran, (0, 0, 0), (45, 43, 300, 40), 2)
    pygame.draw.rect(ekran, (255, 255, 255), (47, 45, 296, 36))
    text_input = font.render(input_text, True, (0, 0, 0))
    ekran.blit(text_input, (50, 50))
    pokemon_draw()

    pygame.display.flip()
pygame.quit()