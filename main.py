import pygame
import random
pygame.init()
pygame.font.init()

my_font = pygame.font.SysFont('Comic Sans MS', 30)

screen = pygame.display.set_mode((1280,720))
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


fish = Player()
food = Food()

foodTotal = 0
heading_x = True # True if the fish in heading in the x-positive direciton

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    screen.fill("darkgreen")
    player_sprite = pygame.Rect(50, 50, 25, 25)
    player_sprite.center = player_pos
    screen.blit(food.image,  checkScreenPosition(food.pos, food.rect))
    food.rect.center = food.pos
    screen.blit(fish.image, checkScreenPosition(player_pos, fish.rect))
    fish.rect.center = player_pos
    text_surface = my_font.render(str(foodTotal), False, (0,0,0))
    screen.blit(text_surface, (0,0))
    

    if pygame.sprite.collide_rect(fish,food): #checks for collision with fish food
        foodTotal += 1
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
    


    pygame.display.flip()

    dt = clock.tick(60)/1000


pygame.quit()
