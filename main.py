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

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        
        self.image = pygame.image.load('assets/fish.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (screen.get_width()/10,screen.get_height()/10))
        self.rect = self.image.get_rect()
        self.rect.size = self.image.get_size()

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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    screen.fill("darkgreen")
    player_sprite = pygame.Rect(50, 50, 25, 25)
    player_sprite.center = player_pos
    screen.blit(food.image,  food.pos)
    food.rect.center = food.pos
    screen.blit(fish.image, player_pos)
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
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    


    pygame.display.flip()

    dt = clock.tick(60)/1000


pygame.quit()
