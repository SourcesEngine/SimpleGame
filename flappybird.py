import pygame, random, sys, os
from PIL import Image, ImageSequence

# --- Step 1: Split GIF into frames automatically ---
gif_path = "phoenix1.gif"
frames_folder = "frames"

if not os.path.exists(frames_folder):
    os.makedirs(frames_folder)

# Extract frames if not already done
if not os.listdir(frames_folder):
    gif = Image.open(gif_path)
    for i, frame in enumerate(ImageSequence.Iterator(gif)):
        frame = frame.convert("RGBA")
        frame.save(os.path.join(frames_folder, f"phoenix{i+1}.png"))
    print("GIF split complete! Frames saved in 'frames' folder.")

# --- Step 2: Initialize Pygame ---
pygame.init()
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load frames
frames = []
for file in sorted(os.listdir(frames_folder)):
    if file.endswith(".png"):
        img = pygame.image.load(os.path.join(frames_folder, file)).convert_alpha()
        frames.append(pygame.transform.scale(img, (64,64)))

bird_x, bird_y = 50, HEIGHT//2
velocity, gravity = 0, 0.5
pipe_width, pipe_gap = 150, 180
pipes = []
pipe_speed = 3
score = 0
auto_pilot = True  # start in autopilot mode

# Animation control
frame_index = 0
frame_counter = 0

# Particle system
particles = []

def create_pipe():
    gap_y = random.randint(120, HEIGHT-120)
    pipes.append({"x": WIDTH, "gap_y": gap_y})

def draw_pipes():
    for pipe in pipes:
        pygame.draw.rect(screen, (0,200,0), (pipe["x"], 0, pipe_width, pipe["gap_y"]-pipe_gap//2))
        pygame.draw.rect(screen, (0,200,0), (pipe["x"], pipe["gap_y"]+pipe_gap//2, pipe_width, HEIGHT))

def draw_phoenix():
    global frame_index, frame_counter
    screen.blit(frames[frame_index], (bird_x, int(bird_y)))
    # glow effect
    glow = pygame.Surface((100,100), pygame.SRCALPHA)
    pygame.draw.circle(glow, (255,150,0,80), (50,50), 50)
    screen.blit(glow, (bird_x-20, int(bird_y)-20))

    # cycle animation frames
    frame_counter += 1
    if frame_counter >= 5:  # adjust speed
        frame_index = (frame_index + 1) % len(frames)
        frame_counter = 0

def update_particles():
    # Add continuous trail
    particles.append([bird_x, bird_y, random.randint(4,8), random.choice([(255,100,0),(255,200,50),(200,0,200),(0,150,255)])])
    for particle in particles[:]:
        particle[0] -= 2  # drift left
        particle[2] -= 0.2  # shrink
        if particle[2] <= 0:
            particles.remove(particle)
        else:
            pygame.draw.circle(screen, particle[3], (int(particle[0]), int(particle[1])), int(particle[2]))

def flame_burst():
    # Create a burst of multi-colored particles
    for i in range(20):
        size = random.randint(4, 10)
        offset_x = random.randint(-15, 15)
        offset_y = random.randint(-15, 15)
        color = random.choice([(255,100,0),(255,200,50),(200,0,200),(0,150,255)])
        particles.append([bird_x+offset_x, bird_y+offset_y, size, color])

def autopilot():
    global velocity
    if pipes:
        next_pipe = pipes[0]
        if bird_y > next_pipe["gap_y"]:
            velocity = -7
            flame_burst()

create_pipe()

# --- Step 3: Game Loop ---
while True:
    screen.fill((30,30,40))  # dark mystical background
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not auto_pilot:
                velocity = -7
                flame_burst()
            if event.key == pygame.K_a:  # toggle autopilot
                auto_pilot = not auto_pilot

    if auto_pilot:
        autopilot()

    velocity += gravity
    bird_y += velocity

    for pipe in pipes:
        pipe["x"] -= pipe_speed
    if pipes[0]["x"]+pipe_width < 0:
        pipes.pop(0); create_pipe(); score += 1

    draw_pipes()
    draw_phoenix()
    update_particles()

    font = pygame.font.SysFont(None, 28)
    text = font.render(f"Score: {score} | Mode: {'Auto' if auto_pilot else 'Manual'}", True, (255,255,255))
    screen.blit(text, (10,10))

    pygame.display.flip()
    clock.tick(30)