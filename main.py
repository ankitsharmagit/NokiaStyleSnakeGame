# main.py
import pygame
import sys
import random
import time

# --- Initialization ---
# This section initializes pygame and its modules.
pygame.init()
pygame.mixer.init() # Initialize the sound mixer

# --- Game Constants ---
# These constants define the core properties of the game window and elements.

# Screen and Grid Dimensions
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = (SCREEN_HEIGHT - 80) // GRID_SIZE # Reserve space for score

# Colors (Nokia Retro Style)
BACKGROUND_COLOR = (199, 240, 216)  # #c7f0d8
FOREGROUND_COLOR = (67, 82, 61)    # #43523d
SNAKE_HEAD_COLOR = (40, 50, 35)
HIGHLIGHT_COLOR = (255, 255, 255)
HIGHLIGHT_BG_COLOR = (90, 110, 80)
FLASH_COLOR = (230, 255, 238)
GAME_OVER_COLOR = (139, 0, 0) # Dark red for dreadful style

# Difficulty Levels (Snake Speed)
DIFFICULTY = {
    1: 7,   # Easy
    2: 12,  # Medium
    3: 18   # Hard
}

# --- Game Setup ---
# This sets up the main display window, clock, and font.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Retro Snake')
clock = pygame.time.Clock()
try:
    font = pygame.font.Font(None, 36)
    bold_font = pygame.font.Font(None, 38) # For bolding text
    large_font = pygame.font.Font(None, 72)
    ui_font = pygame.font.Font(None, 48) # Font for important UI text
except Exception:
    font = pygame.font.SysFont('Arial', 36)
    bold_font = pygame.font.SysFont('Arial', 36, bold=True)
    large_font = pygame.font.SysFont('Arial', 72)
    ui_font = pygame.font.SysFont('Arial', 48)

# Load the start screen image
try:
    # IMPORTANT: Make sure 'Snake-II-Featured.jpg' is in the same folder as this script.
    start_screen_image = pygame.image.load('Snake-II-Featured.jpg')
    img_width, img_height = start_screen_image.get_rect().size
    scale_factor = (SCREEN_WIDTH - 40) / img_width # Leave some margin
    start_screen_image = pygame.transform.scale(start_screen_image, (int(img_width * scale_factor), int(img_height * scale_factor)))
except pygame.error:
    print("Warning: 'Snake-II-Featured.jpg' not found. Displaying text title instead.")
    start_screen_image = None

# --- Sound Effects ---
try:
    # Sound for eating food
    eat_sound = pygame.mixer.Sound(buffer=bytearray([int(128 + 127 * 0.5 * (i // 50 % 2 - 0.5)) for i in range(2000)]))
    eat_sound.set_volume(0.1)
    # Dreadful sound for game over
    game_over_sound = pygame.mixer.Sound(buffer=bytearray([int(128 + 127 * random.uniform(-0.5, 0.5) * (1 - i/12000)) for i in range(12000)]))
    game_over_sound.set_volume(0.2)
except pygame.error:
    print("Warning: Could not create sound effects.")
    eat_sound = None
    game_over_sound = None

# --- Game Over Messages ---
GAME_OVER_MESSAGES = [
    "A noble effort!",
    "The snake rests.",
    "Better luck next time!",
    "You've been outsnaked.",
    "Final score:",
    "That's a wrap!"
]

# --- Game Object Classes ---

class Snake:
    """
    Represents the snake player with improved visuals.
    """
    def __init__(self):
        self.reset()

    def reset(self):
        """Initializes the snake's properties to their starting state."""
        self.length = 1
        self.positions = [((GRID_WIDTH // 2), (GRID_HEIGHT // 2))]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.score = 0
        self.grow_pending = False

    def get_head_position(self):
        """Returns the position of the snake's head."""
        return self.positions[0]

    def turn(self, point):
        """Changes the snake's direction, preventing reversal."""
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        """Moves the snake and checks for collisions."""
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x), (cur[1] + y))

        if new[0] < 0 or new[0] >= GRID_WIDTH or new[1] < 0 or new[1] >= GRID_HEIGHT:
            return True # Wall collision

        if len(self.positions) > 2 and new in self.positions:
            return True # Self collision

        self.positions.insert(0, new)
        if self.grow_pending:
            self.length += 1
            self.grow_pending = False
        else:
            self.positions.pop()
            
        return False # No collision

    def eat(self):
        """Marks the snake to grow and increases score."""
        self.grow_pending = True
        self.score += 10
        if eat_sound:
            eat_sound.play()

    def draw(self, surface):
        """Draws the snake with a distinct head (with eyes) and gradient body."""
        # Draw the body with a gradient
        for i, p in enumerate(self.positions[1:]):
            lerp_factor = (i + 1) / (len(self.positions) if len(self.positions) > 1 else 1)
            body_color = (
                int(SNAKE_HEAD_COLOR[0] + (FOREGROUND_COLOR[0] - SNAKE_HEAD_COLOR[0]) * lerp_factor),
                int(SNAKE_HEAD_COLOR[1] + (FOREGROUND_COLOR[1] - SNAKE_HEAD_COLOR[1]) * lerp_factor),
                int(SNAKE_HEAD_COLOR[2] + (FOREGROUND_COLOR[2] - SNAKE_HEAD_COLOR[2]) * lerp_factor)
            )
            r = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE + 80), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, body_color, r)

        # Draw the head
        head_pos = self.positions[0]
        head_rect = pygame.Rect((head_pos[0] * GRID_SIZE, head_pos[1] * GRID_SIZE + 80), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, SNAKE_HEAD_COLOR, head_rect)
        pygame.draw.rect(surface, tuple(max(0, c-20) for c in SNAKE_HEAD_COLOR), head_rect, 1)
        
        # Draw eyes on the head based on direction
        eye_size = 3
        eye_offset_1 = 4
        eye_offset_2 = GRID_SIZE - eye_offset_1 - eye_size
        dir_x, dir_y = self.direction

        if dir_y != 0: # Moving vertically (Up or Down)
            eye1_pos = (head_rect.left + eye_offset_1, head_rect.top + (eye_offset_1 if dir_y == -1 else eye_offset_2))
            eye2_pos = (head_rect.left + eye_offset_2, head_rect.top + (eye_offset_1 if dir_y == -1 else eye_offset_2))
        else: # Moving horizontally (Left or Right)
            eye1_pos = (head_rect.left + (eye_offset_1 if dir_x == -1 else eye_offset_2), head_rect.top + eye_offset_1)
            eye2_pos = (head_rect.left + (eye_offset_1 if dir_x == -1 else eye_offset_2), head_rect.top + eye_offset_2)

        pygame.draw.rect(surface, HIGHLIGHT_COLOR, (*eye1_pos, eye_size, eye_size))
        pygame.draw.rect(surface, HIGHLIGHT_COLOR, (*eye2_pos, eye_size, eye_size))


class Food:
    """Represents the food, with a subtle pulse effect."""
    def __init__(self):
        self.position = (0, 0)
        self.color = FOREGROUND_COLOR
        self.pulse_timer = 0
        self.randomize_position([])

    def randomize_position(self, snake_positions):
        """Sets food to a random position not on the snake."""
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if self.position not in snake_positions:
                break

    def draw(self, surface):
        """Draws the food with a pulsing effect."""
        self.pulse_timer += 1
        pulse_amount = (self.pulse_timer % 30) / 30 # Cycle every 30 frames
        size_offset = -2 * (0.5 - abs(0.5 - pulse_amount)) # Makes it shrink and grow
        
        size = GRID_SIZE + size_offset
        pos_offset = (GRID_SIZE - size) / 2

        r = pygame.Rect(
            (self.position[0] * GRID_SIZE + pos_offset, self.position[1] * GRID_SIZE + 80 + pos_offset),
            (size, size)
        )
        pygame.draw.rect(surface, self.color, r, border_radius=3)


# --- Helper Functions ---

def draw_text(surface, text, font, color, position, centered=True):
    """Renders and positions text on the screen."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if centered:
        text_rect.center = position
    else:
        text_rect.topleft = position
    surface.blit(text_surface, text_rect)

def draw_ui(surface, score):
    """Draws the top UI panel with a more distinct score."""
    pygame.draw.rect(surface, FOREGROUND_COLOR, (0, 0, SCREEN_WIDTH, 80))
    pygame.draw.rect(surface, BACKGROUND_COLOR, (5, 5, SCREEN_WIDTH - 10, 70))
    draw_text(surface, f"SCORE: {score}", ui_font, FOREGROUND_COLOR, (SCREEN_WIDTH / 2, 40))
    pygame.draw.rect(surface, FOREGROUND_COLOR, (0, 80, SCREEN_WIDTH, SCREEN_HEIGHT - 80), 5)

def screen_flash(surface):
    """Flashes the screen for one frame."""
    flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - 80))
    flash_surface.fill(FLASH_COLOR)
    flash_surface.set_alpha(150) # Semi-transparent
    surface.blit(flash_surface, (0, 80))
    pygame.display.flip()
    pygame.time.wait(50) # Hold flash for 50ms

# --- Game State Functions ---

def show_start_screen():
    """Displays the start screen and waits for difficulty selection."""
    selected_option = 1
    menu_options = {1: "EASY", 2: "MEDIUM", 3: "HARD"}

    while True:
        screen.fill(BACKGROUND_COLOR)
        if start_screen_image:
            img_rect = start_screen_image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
            screen.blit(start_screen_image, img_rect)
        else:
            draw_text(screen, "SNAKE II", large_font, FOREGROUND_COLOR, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))

        draw_text(screen, "SELECT DIFFICULTY", ui_font, FOREGROUND_COLOR, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        
        for option, text in menu_options.items():
            y_pos = SCREEN_HEIGHT / 2 + 60 + (option * 50)
            if option == selected_option:
                pygame.draw.rect(screen, HIGHLIGHT_BG_COLOR, (50, y_pos - 20, SCREEN_WIDTH - 100, 40), border_radius=5)
                draw_text(screen, text, font, HIGHLIGHT_COLOR, (SCREEN_WIDTH / 2, y_pos))
            else:
                draw_text(screen, text, font, FOREGROUND_COLOR, (SCREEN_WIDTH / 2, y_pos))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = max(1, selected_option - 1)
                elif event.key == pygame.K_DOWN:
                    selected_option = min(3, selected_option + 1)
                elif event.key == pygame.K_RETURN:
                    return DIFFICULTY[selected_option]
                elif event.key in [pygame.K_1, pygame.K_KP_1]: return DIFFICULTY[1]
                elif event.key in [pygame.K_2, pygame.K_KP_2]: return DIFFICULTY[2]
                elif event.key in [pygame.K_3, pygame.K_KP_3]: return DIFFICULTY[3]

def show_game_over_screen(score):
    """Displays the game over screen with a dreadful style."""
    if game_over_sound:
        game_over_sound.play()
        
    # Screen Shake Effect
    original_surface = screen.copy()
    shake_intensity = 10
    for i in range(10):
        offset = (random.randint(-shake_intensity, shake_intensity), random.randint(-shake_intensity, shake_intensity))
        screen.blit(original_surface, offset)
        pygame.display.flip()
        pygame.time.wait(20)
        shake_intensity = int(shake_intensity * 0.8)

    screen.fill(BACKGROUND_COLOR)
    message = random.choice(GAME_OVER_MESSAGES)
    
    draw_text(screen, "GAME OVER", large_font, GAME_OVER_COLOR, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
    draw_text(screen, f"{message} {score}", font, FOREGROUND_COLOR, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    
    # Draw "Press ENTER to Play Again" with bold "ENTER"
    text1 = font.render("Press ", True, FOREGROUND_COLOR)
    text2 = bold_font.render("ENTER", True, FOREGROUND_COLOR)
    text3 = font.render(" to Play Again", True, FOREGROUND_COLOR)
    
    total_width = text1.get_width() + text2.get_width() + text3.get_width()
    start_x = (SCREEN_WIDTH - total_width) / 2
    y_pos = SCREEN_HEIGHT / 2 + 50
    
    screen.blit(text1, (start_x, y_pos))
    screen.blit(text2, (start_x + text1.get_width(), y_pos - 1)) # -1 for slight vertical alignment
    screen.blit(text3, (start_x + text1.get_width() + text2.get_width(), y_pos))
    
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

def game_loop(speed):
    """The main loop for the gameplay state."""
    snake = Snake()
    food = Food()
    food.randomize_position(snake.positions)
    
    # Capture screen for shake effect
    last_frame = screen.copy()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: snake.turn((0, -1))
                elif event.key == pygame.K_DOWN: snake.turn((0, 1))
                elif event.key == pygame.K_LEFT: snake.turn((-1, 0))
                elif event.key == pygame.K_RIGHT: snake.turn((1, 0))

        collision = snake.move()
        if collision:
            return snake.score, last_frame

        if snake.get_head_position() == food.position:
            screen_flash(screen) # Flash effect on eat
            snake.eat()
            food.randomize_position(snake.positions)

        screen.fill(BACKGROUND_COLOR)
        snake.draw(screen)
        food.draw(screen)
        draw_ui(screen, snake.score)
        
        last_frame.blit(screen, (0,0))
        pygame.display.flip()
        clock.tick(speed)

# --- Main Game Execution ---
def main():
    """The main entry point that controls the overall game flow."""
    while True:
        speed = show_start_screen()
        final_score, last_frame = game_loop(speed)
        show_game_over_screen(final_score)

if __name__ == '__main__':
    main()
