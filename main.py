import pygame
import random
import os
from os.path import abspath, dirname
os.chdir(dirname(abspath(__file__))) #Launches file from its parent directory
pygame.init()
pygame.font.init()

my_font = pygame.font.SysFont('Comic Sans MS', 30)

screen = pygame.display.set_mode((1280/2,720/2))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2 , screen.get_height() / 2) 

def checkScreenPosition(pos, rect): #Keeps positions inside of the visible screen
    
    #Keep X position in screen
    if pos[0] < 0:
        pos[0] = 0
    elif pos[0] > screen.get_width() - rect.width:
        pos[0] = (screen.get_width() - rect.width)

    if pos[1] < 0:
        pos[1] = 0
    elif pos[1] > screen.get_height() - rect.height:
        pos[1] = (screen.get_height() - rect.height)
    return pos




class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        
        self.image = pygame.image.load('assets/fish.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (screen.get_width()/10,screen.get_height()/10))
        self.rect = self.image.get_rect()
        self.rect.size = self.image.get_size()
    
    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)

class Food(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/food.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (screen.get_width()/10,screen.get_height()/10))
        self.rect = self.image.get_rect()
        self.rect.size = self.image.get_size()
        self.pos = pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))

class Button():
    def __init__(self, rect_size, rect_pos, text):
        #self.rect = pygame.Rect(rect_pos[0], rect_pos[1], rect_size[0], rect_size[1])
        self.text = my_font.render(str(text), False, (0,0,0))
        self.rect = self.text.get_rect()
        self.rect.center = checkScreenPosition(rect_pos, self.rect)

    def render(self):
        self.rendered_rect = pygame.draw.rect(screen, (255,0,0), self.rect)
        screen.blit(self.text, (self.rect.x, self.rect.y))
    
    
        
        

fish = Player()
food = Food()
foodIncrement = 1
foodPrice = 10
upgradeButton = Button((50,50), [screen.get_width()/2, screen.get_height()], "Upgrade")

foodTotal = 0
heading_x = True # True if the fish in heading in the x-positive direciton

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.BUTTON_LEFT:
            if upgradeButton.rect.collidepoint(pygame.mouse.get_pos()):
                if foodTotal >= foodPrice:
                    foodTotal -= foodPrice
                    foodIncrement += 1
                    foodPrice = foodIncrement*foodIncrement + 10
                    print(foodTotal, foodIncrement, foodPrice)
                    

    
    screen.fill("blue")

    # Buttons

    upgradeButton.render() 

    #Sprites

    player_sprite = pygame.Rect(50, 50, 25, 25)
    player_sprite.center = player_pos
    screen.blit(food.image,  checkScreenPosition(food.pos, food.rect))
    food.rect.center = food.pos
    screen.blit(fish.image, checkScreenPosition(player_pos, fish.rect))
    fish.rect.center = player_pos
    text_surface = my_font.render(str(foodTotal), False, (0,0,0))

    # Text
    screen.blit(text_surface, (0,0))

    
    
    

    if pygame.sprite.collide_rect(fish,food): #checks for collision with fish food
        foodTotal += foodIncrement
        food.pos = pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt
        if heading_x == False: #Flips fish image when changing direction
            heading_x = True
            fish.flip()
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
        if heading_x == True: #Flips fish image when changing direction
            heading_x = False
            fish.flip()
    


    pygame.display.flip() #Displays new Information

    dt = clock.tick(60)/1000


pygame.quit()


