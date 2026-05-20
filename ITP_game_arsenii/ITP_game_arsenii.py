import pygame
import sys
import json
import os

pygame.init();
WIDTH, HEIGHT = 1600, 900
FPS=60;
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
        
        self.start_btn = pygame.Rect(500, 600, 200, 50)
        self.exit_btn = pygame.Rect(900, 600, 200, 50)
        
   
        self.score = 0
        self.high_score = self.load_high_score() 

    

    def load_high_score(self):
        
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("high_score", 0)
            except Exception:
                return 0 # err 
        return 0 # no file 

    def save_high_score(self):
    
        data = {"high_score": self.high_score}
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def check_and_update_highscore(self):
      
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

    
    def reset_game(self):
        #res all
        self.score = 0
        #center all 
        # self.paddle.rect.x = WIDTH // 2
        # self.blocks.generate() 







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




    def update(self):
        #logic
        if self.state == "GAME":
            
            # self.ball.move()
            # self.score += 10 
            pass

    def draw(self):
        
        mouse_pos = pygame.mouse.get_pos()
        
        #   MAIN MENU
        if self.state == "MENU":
            self.screen.fill(DARK_BG)
            
            # title
            title = self.font_title.render("ITP Game", True, WHITE)
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
            
            # rec in menu
            hs_text = self.font_ui.render(f"Record: {self.high_score}", True, WHITE)
            self.screen.blit(hs_text, (WIDTH // 2 - hs_text.get_width() // 2, 160))
            
            # start button
            if self.start_btn.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, BUTTON_HOVER, self.start_btn, border_radius=6)
            else:
                pygame.draw.rect(self.screen, BUTTON_COLOR, self.start_btn, border_radius=6)
            txt_start = self.font_ui.render("Play", True, WHITE)
            self.screen.blit(txt_start, (self.start_btn.x + (self.start_btn.width // 2 - txt_start.get_width() // 2), 
                                         self.start_btn.y + (self.start_btn.height // 2 - txt_start.get_height() // 2)))
            
            # exit button
            if self.exit_btn.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, BUTTON_HOVER, self.exit_btn, border_radius=6)
            else:
                pygame.draw.rect(self.screen, BUTTON_COLOR, self.exit_btn, border_radius=6)
            txt_exit = self.font_ui.render("Exit", True, WHITE)
            self.screen.blit(txt_exit, (self.exit_btn.x + (self.exit_btn.width // 2 - txt_exit.get_width() // 2), 
                                        self.exit_btn.y + (self.exit_btn.height // 2 - txt_exit.get_height() // 2)))

        # GAmE
        elif self.state == "GAME":
            self.screen.fill(GAME_BG)
            
            # score
            score_text = self.font_ui.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(score_text, (20, 20))
            
            # sm txt
            hint_text = self.font_ui.render("[K] - simulate death | [ESC] - menu", True, WHITE)
            self.screen.blit(hint_text, (WIDTH - hint_text.get_width() - 20, 20))
            
           
            # self.paddle.draw(self.screen)
            # self.ball.draw(self.screen)
            # self.blocks.draw(self.screen)

        #   GAME OVER   
        elif self.state == "GAMEOVER":
            self.screen.fill(BLACK)
            go_title = self.font_title.render("Game over", True, (255, 0, 0))
            self.screen.blit(go_title, (WIDTH // 2 - go_title.get_width() // 2, HEIGHT // 3))
            
            res_text = self.font_ui.render(f"Score: {self.score} points", True, WHITE)
            self.screen.blit(res_text, (WIDTH // 2 - res_text.get_width() // 2, HEIGHT // 2))
            
            space_text = self.font_ui.render("Press SPACE to return to menu", True, WHITE)
            self.screen.blit(space_text, (WIDTH // 2 - space_text.get_width() // 2, HEIGHT // 2 + 80))

        pygame.display.flip()

    def run(self):
        #main cycle
        while self.running:
            self.handle_events() 
            self.update()        
            self.draw()          
            self.clock.tick(FPS) 



if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
