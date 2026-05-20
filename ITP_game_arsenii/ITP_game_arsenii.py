import pygame;
import sys;
import time;

pygame.init();
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT));
clock = pygame.time.Clock()


state = "MENU"
running = True

start_btn = pygame.Rect(300, 220, 200, 50)
exit_btn = pygame.Rect(300, 300, 200, 50)

WHITE = (255, 255, 255)
DARK_BG = (30, 30, 40)
GAME_BG = (50, 100, 50)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 149, 237)






def draw_menu():
    screen.fill(DARK_BG)

def draw_game():
    
    
    pass;




while running:
    if state == "MENU":
                draw_menu()
    if state == "GAME":
        draw_game;
    pygame.display.flip();
    clock.tick(60);
