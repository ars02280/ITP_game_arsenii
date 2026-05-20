import pygame
import sys
import json
import os
import random

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
PADDLE_COLOR = (0, 255, 200)
BALL_COLOR = (255, 215, 0)



class GameObject:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        
        pygame.draw.rect(screen, self.color, self.rect)






class Paddle(GameObject):
    def __init__(self):
        
        paddle_width = 180
        paddle_height = 15
        x = WIDTH // 2 - paddle_width // 2
        y = HEIGHT - 50
        
        super().__init__(x, y, paddle_width, paddle_height, PADDLE_COLOR)
        self.speed = 12  

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self, screen):
       
        pygame.draw.rect(screen, self.color, self.rect, border_radius=4)


class Ball(GameObject):
    def __init__(self):
        self.radius = 10
        x = WIDTH // 2
        y = HEIGHT // 2 + 100
        
        
        super().__init__(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2, BALL_COLOR)
        
        self.speed_x = random.choice([-6, 6])
        self.speed_y = -6

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0:
            self.speed_y = -self.speed_y

    def draw(self, screen):
        
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)


class Block(GameObject):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)





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
        self.paddle = None
        self.ball = None
        self.blocks = []

    

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
        
        self.score = 0
        self.paddle = Paddle()
        self.ball = Ball()
        self.blocks = []

       
        block_width = 150
        block_height = 50
        padding = 8
        offset_top = 80
        offset_left = 13

        colors = [(240, 80, 80), (240, 140, 80), (240, 200, 80), (80, 200, 80), (80, 200, 240), (140, 80, 240)]

        for row in range(6):
            for col in range(10):
                x = offset_left + col * (block_width + padding)
                y = offset_top + row * (block_height + padding)
                color = colors[row] 
                self.blocks.append(Block(x, y, block_width, block_height, color))






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
        
        if self.state == "GAME":
            self.paddle.move()
            self.ball.move()

            # ball paddle
            if self.ball.rect.colliderect(self.paddle.rect):
                
                if self.ball.speed_y > 0:
                    self.ball.speed_y = -self.ball.speed_y

            # bll block
            for block in self.blocks[:]: 
                if self.ball.rect.colliderect(block.rect):
                    self.ball.speed_y = -self.ball.speed_y 
                    self.blocks.remove(block)             
                    self.score += 10                      
                    break                                 

            
            if self.ball.rect.bottom >= HEIGHT:
                self.check_and_update_highscore()
                self.state = "GAMEOVER"

            
            if not self.blocks:
                self.check_and_update_highscore()
                self.state = "GAMEOVER"

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        
        #Main menu 
        if self.state == "MENU":
            self.screen.fill(DARK_BG)
            
            title = self.font_title.render("ITP game", True, WHITE)
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
            
            hs_text = self.font_ui.render(f"Record: {self.high_score}", True, WHITE)
            self.screen.blit(hs_text, (WIDTH // 2 - hs_text.get_width() // 2, 160))
            
            if self.start_btn.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, BUTTON_HOVER, self.start_btn, border_radius=6)
            else:
                pygame.draw.rect(self.screen, BUTTON_COLOR, self.start_btn, border_radius=6)
            txt_start = self.font_ui.render("Play", True, WHITE)
            self.screen.blit(txt_start, (self.start_btn.x + (self.start_btn.width // 2 - txt_start.get_width() // 2), 
                                         self.start_btn.y + (self.start_btn.height // 2 - txt_start.get_width() // 2)))
            
            if self.exit_btn.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, BUTTON_HOVER, self.exit_btn, border_radius=6)
            else:
                pygame.draw.rect(self.screen, BUTTON_COLOR, self.exit_btn, border_radius=6)
            txt_exit = self.font_ui.render("Exit", True, WHITE)
            self.screen.blit(txt_exit, (self.exit_btn.x + (self.exit_btn.width // 2 - txt_exit.get_width() // 2), 
                                        self.exit_btn.y + (self.exit_btn.height // 2 - txt_exit.get_height() // 2)))

        # game
        elif self.state == "GAME":
            self.screen.fill(GAME_BG)
            
            
            score_text = self.font_ui.render(f"Счет: {self.score}", True, WHITE)
            self.screen.blit(score_text, (20, 20))
            
           
            self.paddle.draw(self.screen)
            self.ball.draw(self.screen)
            for block in self.blocks:
                block.draw(self.screen)

        #game over
        elif self.state == "GAMEOVER":
            self.screen.fill(BLACK)
            go_title = self.font_title.render("GAME", True, (255, 0, 0))
            self.screen.blit(go_title, (WIDTH // 2 - go_title.get_width() // 2, HEIGHT // 3))
            
            res_text = self.font_ui.render(f"Score: {self.score} points", True, WHITE)
            self.screen.blit(res_text, (WIDTH // 2 - res_text.get_width() // 2, HEIGHT // 2))
            
            space_text = self.font_ui.render("press SPACE to return to menu", True, WHITE)
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
