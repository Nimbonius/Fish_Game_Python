import pygame
import pickle
import random
import os
from os.path import abspath, dirname
os.chdir(dirname(abspath(__file__))) #Launches file from its parent directory
pygame.init()
pygame.font.init()

mainFont = pygame.font.SysFont('Comic Sans MS', 30)
smallFont = pygame.font.SysFont('Comis Sans MS', 15)

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
    def __init__(self, rect_size, rect_pos, text, subtext):
        #self.rect = pygame.Rect(rect_pos[0], rect_pos[1], rect_size[0], rect_size[1])
        self.text = mainFont.render(str(text), False, (0,0,0))
        self.subtext = smallFont.render(str(subtext), False, (0,0,0))
        self.rect = pygame.Rect((self.text.get_rect().width + self.subtext.get_rect().width), (self.text.get_rect().height + self.subtext.get_rect().height), (self.text.get_rect().width + self.subtext.get_rect().width), (self.text.get_rect().height + self.subtext.get_rect().height))
        print(self.text.get_width(), self.subtext.get_width())
        if self.text.get_rect().width >= self.subtext.get_rect().width: #Fixes width of button based on the largest text
            self.rect.width = self.text.get_width()
        self.rect.center = checkScreenPosition(rect_pos, self.rect)

    def render(self, text, subtext):
        if text:
            self.text = mainFont.render(str(text), False, (0,0,0))
        if subtext:
            self.subtext = smallFont.render(str(subtext), False, (0,0,0)) 
        self.rendered_rect = pygame.draw.rect(screen, (255,0,0), self.rect)
        #pygame.draw.rect(screen, (255,0,0), self.subtext.get_rect())
        screen.blit(self.text, (self.rect.x, self.rect.y))
        screen.blit(self.subtext, (self.rect.x, self.rect.y))
    
    
        
        

fish = Player()
food = Food()
saveData = None
foodIncrement = 1
exponentialUpgrades = 0
linearUpgrades = 0
foodTotal = 0
linearIncrement = 1
foodPrice = 10
foodPriceExponential = 100

try: #saveData = [foodIncrement, exponentialUpgrades, linearUpgrades, foodTotal, linearIncrement, foodPrice, foodPriceExponential]
    with open('saveData.pickle', "rb") as F:
        saveData = pickle.load(F)
    foodIncrement = saveData[0]
    exponentialUpgrades = saveData[1]
    linearUpgrades = saveData[2]
    foodTotal = saveData[3]
    linearIncrement = saveData[4]
    foodPrice = saveData[5]
    foodPriceExponential = saveData[6]
except:
    saveData = None














upgradeLinearButton = Button((50,50), [(screen.get_width()/2)-65, screen.get_height()], "Upgrade", "Price: ")
upgradeExponetialButton = Button((50,50), [(screen.get_width()/2)+70, screen.get_height()], "Upgrade^2", "Price: ")




heading_x = True # True if the fish in heading in the x-positive direciton

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            with open('saveData.pickle', 'wb') as F:
                saveData = [foodIncrement, exponentialUpgrades, linearUpgrades, foodTotal, linearIncrement, foodPrice, foodPriceExponential]
                pickle.dump(saveData, F)
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.BUTTON_LEFT:
            if upgradeLinearButton.rect.collidepoint(pygame.mouse.get_pos()): #Linear Upgrade Button
                if foodTotal >= foodPrice:
                    foodTotal -= foodPrice
                    linearUpgrades += 1
                    foodIncrement += linearIncrement
                    foodPrice = linearUpgrades*linearUpgrades + 10
                    print(foodTotal, foodIncrement, foodPrice)
            if upgradeExponetialButton.rect.collidepoint(pygame.mouse.get_pos()): #Exponential Upgrade Button
                if foodTotal >= foodPriceExponential:
                    foodTotal -= foodPriceExponential
                    exponentialUpgrades += 1
                    foodIncrement *= 2
                    linearIncrement *= 2
                    foodPriceExponential = 1000*(2**exponentialUpgrades)
                    

    
    screen.fill("blue")

    # Buttons

    upgradeLinearButton.render(None, "Price: "+str(foodPrice)) 
    upgradeExponetialButton.render(None, "Price: "+str(foodPriceExponential))

    #Sprites

    player_sprite = pygame.Rect(50, 50, 25, 25)
    player_sprite.center = player_pos
    screen.blit(food.image,  checkScreenPosition(food.pos, food.rect))
    food.rect.center = food.pos
    screen.blit(fish.image, checkScreenPosition(player_pos, fish.rect))
    fish.rect.center = player_pos

    # Text
    total_text = mainFont.render("Total Food: " + str(foodTotal), False, (0,0,0))
    increment_text = mainFont.render("Food Increment: " + str(foodIncrement),False, (0,0,0))
    screen.blit(total_text, (0,0))
    screen.blit(increment_text, (0, 0 + total_text.get_height()))

    
    
    

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


