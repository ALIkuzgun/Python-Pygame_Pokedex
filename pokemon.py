import pygame

# pokemon sınıfı
class Pokemon():
    def __init__(self, en, boy, x, y):
        super().__init__()
        # başlangıç için random png
        self.image = pygame.image.load('pokemon-images/bulbasaur.jpg')
        self.image = pygame.transform.scale(self.image, (180,168)) 
        self.en = en
        self.boy = boy 
        self.x = x
        self.y = y

    def draw(self, ekran):
        ekran.blit(self.image,(self.x,self.y,self.en,self.boy))