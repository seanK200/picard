import gpiozero as gpio
import pygame

KEY_1 = 18
KEY_2 = 23
KEY_3 = 24
KEY_4 = 25
FPS = 30

def move_left(pos):
    pos.x -= 10

def move_right(pos):
    pos.x += 10

def move_up(pos):
    pos.y -= 10

def move_down(pos):
    pos.y += 10


def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    running = True
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    up = gpio.Button(KEY_1)
    down = gpio.Button(KEY_2)
    left = gpio.Button(KEY_3)
    right = gpio.Button(KEY_4)

    up.when_pressed = lambda x: move_left(player_pos)
    down.when_pressed = lambda x: move_down(player_pos)
    left.when_pressed = lambda x: move_left(player_pos)
    right.when_pressed = lambda x: move_right(player_pos)

    PURPLE = pygame.Color("purple")
    GRAY = pygame.Color("darkgrey")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(PURPLE)

        pygame.draw.circle(screen, (128, 128, 128), player_pos, 20)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()

main()
