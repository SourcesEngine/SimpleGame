import pygame
import random
import os
import sys

# --- CONFIGURATION ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 60
GRAVITY = 0.8
JUMP_STRENGTH = -12
AUTO_PILOT = True 

# Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
NEON_BLUE = (0, 255, 255)
SPY_RED = (255, 50, 50)
FLOOR_COLOR = (80, 80, 80)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(NEON_BLUE)
        self.rect = self.image.get_rect(midbottom=(100, SCREEN_HEIGHT - 50))
        self.velocity_y = 0
        self.is_on_ground = True

    def jump(self):
        if self.is_on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.is_on_ground = False
            play_effect("jump_sfx.wav")

    def update(self, obstacles):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        if self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.velocity_y = 0
            self.is_on_ground = True

        if AUTO_PILOT:
            for obs in obstacles:
                # Dynamic sensor: looks slightly further ahead as game speeds up
                if 0 < (obs.rect.left - self.rect.right) < 130:
                    self.jump()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, speed):
        super().__init__()
        self.image = pygame.Surface((30, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, SPY_RED, [(15, 0), (0, 40), (30, 40)])
        self.rect = self.image.get_rect(midbottom=(x, SCREEN_HEIGHT - 50))
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# --- UTILITY FUNCTIONS ---
def play_bg_music():
    if os.path.exists("background_track.mp3"):
        pygame.mixer.music.load("background_track.mp3")
        pygame.mixer.music.set_volume(0.3) 
        pygame.mixer.music.play(-1)

def play_effect(file_name):
    if os.path.exists(file_name):
        sound = pygame.mixer.Sound(file_name)
        sound.set_volume(0.7)
        sound.play()

def draw_text(screen, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont("arial", size, bold=True)
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(x, y))
    screen.blit(surf, rect)

def draw_progress_bar(screen, score):
    # Calculate progress toward the next 1000 (0.0 to 1.0)
    progress = (score % 1000) / 1000
    
    bar_width = 400
    bar_height = 15
    x = (SCREEN_WIDTH - bar_width) // 2
    y = 80 # Positioned below the score text
    
    # Draw the background (Empty Bar)
    pygame.draw.rect(screen, (50, 50, 50), (x, y, bar_width, bar_height))
    
    # Draw the filling (Neon Blue)
    pygame.draw.rect(screen, NEON_BLUE, (x, y, int(bar_width * progress), bar_height))
    
    # Draw a thin border
    pygame.draw.rect(screen, WHITE, (x, y, bar_width, bar_height), 1)

def get_high_score():
    """Reads the high score from a file. If no file exists, returns 0."""
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            try:
                return int(f.read())
            except ValueError:
                return 0
    return 0

def save_high_score(new_score):
    """Saves the new high score to a file."""
    high_score = get_high_score()
    if new_score > high_score:
        with open("highscore.txt", "w") as f:
            f.write(str(new_score))

# --- THE GAME LOOP ---
def run_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Geometry Dash: AI Evolution")
    clock = pygame.time.Clock()

    high_score = get_high_score() # Load the record once at startup

    while True: # Main Restart Loop
        play_bg_music()
        player = Player()
        player_group = pygame.sprite.GroupSingle(player)
        obstacles = pygame.sprite.Group()
        
        score = 0
        spawn_timer = 0
        game_speed = 8
        running = True
        
        while running:
            # 1. Leveling Logic (Difficulty spikes at 1000, 2000, etc.)
            level = score // 1000
            
            # Speed increases with level
            current_speed = game_speed + level
            
            # Spawn rate increases (lower number = faster spawning)
            spawn_rate = max(18, 50 - (level * 5)) 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and not AUTO_PILOT:
                    if event.key == pygame.K_SPACE:
                        player.jump()

            # 2. Spawn Obstacles
            spawn_timer += 1
            if spawn_timer > random.randint(spawn_rate, spawn_rate + 20):
                obstacles.add(Obstacle(SCREEN_WIDTH + 50, current_speed))
                
                # Bonus difficulty: Small chance for double spikes at Level 2+
                if level >= 2 and random.random() > 0.8:
                    obstacles.add(Obstacle(SCREEN_WIDTH + 95, current_speed))
                spawn_timer = 0

            # 3. Update
            player_group.update(obstacles)
            obstacles.update()
            score += 1


            # 4. Collision Check
            if pygame.sprite.spritecollide(player, obstacles, False):
                play_effect("death_sfx.wav")
                pygame.mixer.music.stop()

                # ... (collision happened) ...
                save_high_score(score) # Check if current score beat the record
                high_score = get_high_score() # Refresh the variable for the Death Screen

                running = False 


            # 5. Draw
            bg_color = BLACK
            # Milestone Flash
            if 0 < score % 1000 < 15: bg_color = (40, 40, 60)
            
            screen.fill(bg_color)
            pygame.draw.rect(screen, FLOOR_COLOR, (0, SCREEN_HEIGHT-50, SCREEN_WIDTH, 50))
            player_group.draw(screen)
            obstacles.draw(screen)

            draw_text(screen, f"BEST: {high_score}", 18, SCREEN_WIDTH - 70, 30, (200, 200, 200))
            draw_text(screen, f"SCORE: {score}", 25, SCREEN_WIDTH//2, 30)
            draw_text(screen, f"LEVEL: {level}", 18, SCREEN_WIDTH//2, 60, NEON_BLUE)

            draw_progress_bar(screen, score)

            pygame.display.flip()
            clock.tick(FPS)
        
        show_death_screen(screen, score, high_score) # Pass it to the UI

        # Death Screen
        screen.fill(BLACK)
        draw_text(screen, "GAME OVER", 60, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40, SPY_RED)
        draw_text(screen, f"Final Score: {score}", 30, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20)
        draw_text(screen, "Press SPACE to Restart", 20, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80)
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

if __name__ == "__main__":
    run_game()