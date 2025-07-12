import pygame
from random import randint
WIDTH = 600
HEIGHT = 600
VEL = 5
X = 350
Y = 350
BRICK_H, BRICK_W = 32, 32
GROWTH_PER_FRUIT = 6

x_vel = 0
y_vel = -VEL
pygame.init()
pygame.display.set_caption("SNAKE")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 60)
score = 0
snake_size = 40
snake = pygame.Surface((snake_size, snake_size))
snake.fill('forestgreen')
FRUIT_IMG = pygame.image.load('strawberry.png')
fruit_size = 35
FRUIT = pygame.transform.scale(FRUIT_IMG, (fruit_size, fruit_size))

# sprawdzamy kolizje

def  collision_wall(x, y):
    if x>=WIDTH-snake_size or y>=HEIGHT-snake_size or x<=0 or y<=0:
        return True
    return False

# funckaj ruchu
def move(x,y, x_velocity, y_velocity):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and x>0:
        x_velocity = -VEL
        y_velocity = 0
    if keys[pygame.K_d] and x<WIDTH-snake_size:
        x_velocity = VEL
        y_velocity = 0
    if keys[pygame.K_w] and y > 0:
        x_velocity = 0
        y_velocity = -VEL
    if keys[pygame.K_s] and y<HEIGHT-snake_size:
        x_velocity = 0
        y_velocity = VEL
    return x_velocity, y_velocity

# czy owoc i snakke kolizja

def collision_fruit(x_snake, y_snake, x_fruit, y_fruit, fruit_size, snake_size):
    snake_rect = pygame.Rect(x_snake, y_snake, snake_size, snake_size)
    fruit_rect = pygame.Rect(x_fruit, y_fruit, fruit_size, fruit_size)
    if snake_rect.colliderect(fruit_rect):
        return True
    return False



# main loop
run = True
game_over = False
fruit_spawn = True
snake_blocks = [(X,Y)]
growth_amount = 0
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # ruch
    x_vel, y_vel = move(X, Y, x_vel, y_vel)
    X = X+x_vel
    Y = Y+y_vel

    # sprawdzamy czy w scianie jestesmy
    game_over = collision_wall(X, Y)

    screen.fill((0, 0, 0))


    #kolizja weza
    for segment in snake_blocks[1:]:
        if segment[0] == snake_blocks[0][0] and segment[1] == snake_blocks[0][1]:
            game_over = True

    #game over
    if game_over:
        X = 350
        Y = 350
        score = 0
        game_over = False
        fruit_spawn = True
        snake_blocks = [(X,Y)]

    # sprawdzamy czy jest owoc na planszy jak nie to go tworzymy
    if fruit_spawn: 
        while True:
            x_fruit = randint(0, WIDTH - fruit_size)
            y_fruit = randint(0, HEIGHT - fruit_size)

            if not (X <= x_fruit <= X+snake_size) and not (Y <= y_fruit <= Y + snake_size):
                break

    screen.blit(FRUIT, (x_fruit, y_fruit))
    fruit_spawn = False
    snake_blocks.insert(0,(X,Y))
    # zjadanie owocu i przedluzanie weza
    eat = collision_fruit(snake_blocks[0][0], snake_blocks[0][1], x_fruit, y_fruit, fruit_size, snake_size)
    if eat:
        fruit_spawn = True
        score+=1
        growth_amount = GROWTH_PER_FRUIT
    else:
        if growth_amount > 0:
            growth_amount -= 1
        else:
            snake_blocks.pop()

    # wyswietlamy weza
    for segment in snake_blocks:
        screen.blit(snake, (segment[0], segment[1]))
    #screen.blit(snake, (X, Y))

    # wyswietlamy wynik
    score_text = font.render(f'{score}', True, (240, 240, 240))
    screen.blit(score_text, (WIDTH//2, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()