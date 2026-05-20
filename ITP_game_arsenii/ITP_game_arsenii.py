import pygame
import sys
import json
import os

pygame.init();
WIDTH, HEIGHT = 1600, 900
DATA_FILE = "highscores.json"

screen = pygame.display.set_mode((WIDTH, HEIGHT));
clock = pygame.time.Clock()


state = "MENU"
running = True

start_btn = pygame.Rect(300, 220, 200, 50)
exit_btn = pygame.Rect(300, 300, 200, 50)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BG = (20, 20, 30)
GAME_BG = (35, 35, 45)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 149, 237)



class Game:
    def __init__(self):
  
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("ITP Game")
        self.clock = pygame.time.Clock()
        self.running = True
        
    
        self.state = "MENU"
        
   
        self.font_title = pygame.font.SysFont("Arial", 50)
        self.font_ui = pygame.font.SysFont("Arial", 30)
        
        self.start_btn = pygame.Rect(300, 250, 200, 50)
        self.exit_btn = pygame.Rect(300, 330, 200, 50)
        
   
        self.score = 0
        #self.high_score = self.load_high_score() 




        def handle_events(self):
       
            mouse_pos = pygame.mouse.get_pos()
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                
                if self.state == "MENU":
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.start_btn.collidepoint(mouse_pos):
                            self.reset_game()
                            self.state = "GAME"
                        elif self.exit_btn.collidepoint(mouse_pos):
                            self.running = False
                        
                
                elif self.state == "GAME":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.check_and_update_highscore()
                            self.state = "MENU"
                        
                        if event.key == pygame.K_k:
                            self.check_and_update_highscore()
                            self.state = "GAMEOVER"

            
                elif self.state == "GAMEOVER":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                            self.state = "MENU"





def draw_menu():
    screen.fill(DARK_BG)

def draw_game():
    
    
    pass;




if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
