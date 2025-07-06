import pygame
import random
from enum import Enum
import os
import sys

# Change the working directory to the script's directory
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

class BlockType(Enum):
    OBSTACLE = 1
    KEY = 2
    DOOR = 3
    HAMMER = 4

class Block():
    def __init__(self, type, image):
        self.type = type
        self.image = image

class InventoryItem():
    def __init__(self, label, image):
        self.label = label
        self.image = image

class Progress():
    def __init__(self):
        self.new_game()

    def new_game(self):
        self.robot_pos = (0, 0)
        self.path_positions = []
        self.path_directions = []
        self.level = 0
        self.overall_turns = 0
        self.level_turns = 0
        self.total_keys = 0
        self.keys_collected = 0
        self.hammers_collected = 0
        self.total_hammers = 0
        self.training_mode = False
        self.use_walls = True
        self.show_score = False
        self.fast_mode = False
        self.robot = robotImg
        self.add_level(1)

    def select_robot(self):
        self.robot = penguinImg if random.randint(1, 10) == 1 else robotImg

    def toggle_score(self):
        self.show_score = not self.show_score

    def toggle_training_mode(self):
        self.training_mode = not self.training_mode

    def toggle_fast_mode(self):
        self.fast_mode = not self.fast_mode

    def toggle_use_walls(self):
        self.use_walls = not self.use_walls

    def clear_positions(self):
        self.path_positions = []
        self.path_directions = []

    def add_level(self, level):
        self.level = max(self.level + level, 1)
        self.overall_turns += self.level_turns
        self.level_turns = 0
        self.robot_pos = (0, 0)
        self.keys_collected = 0
        # Same number of keys as the level
        self.total_keys = self.level
        self.hammers_collected = 0
        # Hammer added every 2 levels
        self.total_hammers = int(self.level / 2)
        self.clear_positions()
        self.select_robot()

    def reset_level(self):
        self.level_turns = 0
        self.robot_pos = (0, 0)
        self.keys_collected = 0
        self.hammers_collected = 0
        self.clear_positions()
        self.select_robot()

    def add_move(self, direction, position):
        if direction is not None and position is not None:
            self.path_directions.append(direction)
            self.path_positions.append(position)
            return True
        return False

    def last_position(self):
        return self.path_positions[-1] if self.path_positions else self.robot_pos

    def remove_last_position(self):
        if self.path_positions:
            self.path_positions.pop()
            self.path_directions.pop()

    def next_position(self):
        if self.path_positions:
            self.path_directions.pop(0)
            return self.path_positions.pop(0)

    def any_keys_remaining(self):
        return self.keys_collected < self.total_keys

    def collect_key(self):
        self.keys_collected += 1

    def collect_hammer(self):
        self.hammers_collected += 1

    def bonus_hammer(self):
        self.hammers_collected += 1
        self.total_hammers += 1

    def use_hammer(self):
        if self.hammers_collected > 0:
            self.hammers_collected -= 1
            return True
        return False

    def animation_delay(self):
        return 50 if self.fast_mode else 300

class ModalDialog():
    def __init__(self, title, messages):
        self.title_font = pygame.font.SysFont("arial", 32, bold=True)
        self.text_font = pygame.font.SysFont("arial", 24)
        self.title_surface = self.title_font.render(title, True, WHITE)

        lines = []
        max_text_width = MODAL_WIDTH - 2 * MODAL_PADDING
        for message in messages:
            words = message.split()
            line = ""
            for word in words:
                test_line = f"{line} {word}".strip()
                if self.text_font.size(test_line)[0] <= max_text_width:
                    line = test_line
                else:
                    lines.append(line)
                    line = word
            lines.append(line)

        self.text_surfaces = [self.text_font.render(l, True, WHITE) for l in lines]

    def show(self):
        modal_height = self.title_surface.get_height() + len(self.text_surfaces) * self.text_font.get_height() + 3 * MODAL_PADDING
        modal_rect = pygame.Rect((WIDTH - MODAL_WIDTH) // 2, (HEIGHT - modal_height) // 2, MODAL_WIDTH, modal_height)
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill(SEMI_TRANSPARENT)
        screen.blit(overlay, (0, 0))
        pygame.draw.rect(screen, DARK_GREY, modal_rect, border_radius=10)
        title_pos = self.title_surface.get_rect(center=(WIDTH // 2, modal_rect.top + MODAL_PADDING + self.title_surface.get_height() // 2))
        screen.blit(self.title_surface, title_pos)
        y = title_pos.bottom + MODAL_PADDING
        for surf in self.text_surfaces:
            text_pos = surf.get_rect(center=(WIDTH // 2, y + surf.get_height() // 2))
            screen.blit(surf, text_pos)
            y += surf.get_height()
        pygame.display.flip()
        waiting = True
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit()
                elif event.type == pygame.KEYDOWN:
                    return

# Constants
CELL_SIZE = 60
SCORE_ROW_GRID_HEIGHT, MOVES_ROW_GRID_HEIGHT = 40, 40
ROWS, COLS = 9, 18
GRID_WIDTH = COLS * CELL_SIZE
GRID_HEIGHT = ROWS * CELL_SIZE
WIDTH = GRID_WIDTH
HEIGHT = GRID_HEIGHT + SCORE_ROW_GRID_HEIGHT + MOVES_ROW_GRID_HEIGHT
MODAL_WIDTH = 800
MODAL_PADDING = 20
FPS = 5

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GREY = (50, 50, 50)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
ORANGE = (255, 165, 0)
SEMI_TRANSPARENT = (0, 0, 0, 180)

# Images
robotImg = pygame.image.load('robot.png')
penguinImg = pygame.image.load('penguin.png')
keyImg = pygame.image.load('key.png')
keyScoreImg = pygame.transform.scale(keyImg, (SCORE_ROW_GRID_HEIGHT * 0.75, SCORE_ROW_GRID_HEIGHT * 0.75))
doorImg = pygame.image.load('door.png')
hammerImg = pygame.image.load('hammer.png')
hammerScoreImg = pygame.transform.scale(hammerImg, (SCORE_ROW_GRID_HEIGHT * 0.75, SCORE_ROW_GRID_HEIGHT * 0.75))
obstacleImgList = [
    pygame.image.load('obstacle_1.png'),
    pygame.image.load('obstacle_2.png'),
    pygame.image.load('obstacle_3.png'),
    pygame.image.load('obstacle_4.png'),
    pygame.image.load('obstacle_5.png'),
    pygame.image.load('obstacle_6.png'),
    pygame.image.load('obstacle_7.png'),
    pygame.image.load('obstacle_8.png'),
    pygame.image.load('obstacle_9.png')
]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Obstacle Course")
clock = pygame.time.Clock()

def generate_grid(progress):
    grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
    # Keep track of positions that are free - leave the first row and column blank to not get blocked in
    free_positions = [ (r, c) for r in range(1, ROWS) for c in range(1, COLS) ]
    random.shuffle(free_positions)

    add_blocks(grid, free_positions, progress.total_keys, BlockType.KEY, [ keyImg ])
    add_blocks(grid, free_positions, 1, BlockType.DOOR, [ doorImg ])
    add_blocks(grid, free_positions, progress.total_hammers, BlockType.HAMMER, [ hammerImg ])
    add_blocks(grid, free_positions, 25, BlockType.OBSTACLE, obstacleImgList)
    return grid

def add_blocks(grid, free_positions, count, type, images):
    while count > 0:
        if not free_positions:
            ModalDialog('Game over!', ['Wow, no more space left.', 'Great work!.', 'Press "N" to start a new game.']).show()
            return
        r, c = free_positions.pop()
        count -= 1
        image_count = len(images)
        index = 0 if image_count == 1 else random.randint(0, image_count - 1)
        grid[r][c] = Block(type, images[index])

def draw_empty_position(c, r, outline_colour):
    rect = pygame.Rect(c * CELL_SIZE, (r * CELL_SIZE) + SCORE_ROW_GRID_HEIGHT, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, GRAY, rect)
    pygame.draw.rect(screen, outline_colour, rect, 1)

# Draw the grid, robot, and blocks
def draw(grid, progress):
    screen.fill(WHITE)
    for r in range(ROWS):
        for c in range(COLS):
            border_colour = WHITE
            # If in training mode then show where the user has planned
            if progress.training_mode and (r, c) in progress.path_positions:
                border_colour = ORANGE
            draw_empty_position(c, r, border_colour)
            if grid[r][c] is not None:
                screen.blit(grid[r][c].image, (c * CELL_SIZE, (r * CELL_SIZE) + SCORE_ROW_GRID_HEIGHT))

    # Draw robot
    r, c = progress.robot_pos
    screen.blit(progress.robot, (c * CELL_SIZE, (r * CELL_SIZE) + SCORE_ROW_GRID_HEIGHT))

    # Draw header and footer
    for row_info in (
        (0, SCORE_ROW_GRID_HEIGHT),
        ((len(grid) * CELL_SIZE) + SCORE_ROW_GRID_HEIGHT, MOVES_ROW_GRID_HEIGHT)
    ):
        rect = pygame.Rect(0, row_info[0], GRID_WIDTH, row_info[1])
        pygame.draw.rect(screen, BLACK, rect)

    # Draw the score
    score_text = []
    score_text.append(f"Level {progress.level}")
    if progress.show_score and progress.level_turns is not None:
        score_text.append(f"Level Score: {progress.level_turns}")
    if progress.show_score and progress.level > 1:
        score_text.append(f"Overall Score: {progress.overall_turns / (progress.level - 1)}")
    if progress.training_mode:
        score_text.append("Training Mode is on")
    if not progress.use_walls:
        score_text.append("Walls are off")

    font = pygame.font.SysFont(None, 24)
    if score_text:
        screen.blit(font.render('    '.join(score_text), True, WHITE), (5, 10))

	# Inventory
    inventory_items = [ InventoryItem(f'{progress.keys_collected} / {progress.total_keys}', keyScoreImg) ]
    if progress.total_hammers > 0:
        inventory_items.append(InventoryItem(f'X {progress.hammers_collected}', hammerScoreImg))
    draw_inventory_items(inventory_items)

    # Draw queued path
    text = font.render("Queued: " + " ".join([ direction for direction in progress.path_directions ]), True, WHITE)
    screen.blit(text, (5, GRID_HEIGHT - 30 + SCORE_ROW_GRID_HEIGHT + MOVES_ROW_GRID_HEIGHT))

    pygame.display.flip()

def draw_inventory_items(items):
    font = pygame.font.SysFont(None, 24)
    offset = 0
    for item in items:
        offset += SCORE_ROW_GRID_HEIGHT
        screen.blit(item.image, (GRID_WIDTH - offset, 5))
        offset += SCORE_ROW_GRID_HEIGHT
        screen.blit(font.render(item.label, True, WHITE), (GRID_WIDTH - offset, 10))
        offset += 10

# Get movement direction from key and new row, column
def get_direction(key, progress):
    r, c = progress.last_position()
    new_r = None
    new_c = None
    direction = None
    if key == pygame.K_UP:
        direction, new_r, new_c = "up", r - 1, c
    elif key == pygame.K_DOWN:
        direction, new_r, new_c = "down", r + 1, c
    elif key == pygame.K_LEFT:
        direction, new_r, new_c = "left", r, c - 1
    elif key == pygame.K_RIGHT:
        direction, new_r, new_c = "right", r, c + 1
    else:
        return None, None

    if not progress.use_walls:
        if new_r == -1:
            new_r = ROWS - 1
        elif new_r == ROWS:
            new_r = 0
        elif new_c == -1:
            new_c = COLS - 1
        elif new_c == COLS:
            new_c = 0
    return direction, (new_r, new_c)

def move_robot(grid, progress):
    complete = False
    moved = False
    next_position = progress.next_position()
    if next_position is not None:
        new_r, new_c = next_position
        blocked = True
        moved = True
        if new_r >= 0 and new_r < ROWS and new_c >= 0 and new_c < COLS:
            block = grid[new_r][new_c]
            if block is None:
                blocked = False
            elif block.type == BlockType.KEY:
                progress.collect_key()
                blocked = False
                grid[new_r][new_c] = None
            elif block.type == BlockType.HAMMER:
                blocked = False
                grid[new_r][new_c] = None
                progress.collect_hammer()
            elif block.type == BlockType.DOOR:
                if not progress.any_keys_remaining():
                    blocked = False
                    complete = True
            elif progress.use_hammer():
                grid[new_r][new_c] = None
                blocked = False

        if blocked:
            progress.clear_positions()
            ModalDialog('Blocked', ['Sorry, you got blocked']).show()
            draw(grid, progress)
        elif complete:
            progress.clear_positions()
        else:
            progress.robot_pos = (new_r, new_c)
            pygame.time.delay(progress.animation_delay())

    return complete, moved

def main():
    running = True
    moving = False
    progress = Progress()
    grid = generate_grid(progress)
    new_game = True

    while running:
        if not moving:
            clock.tick(FPS)
        draw(grid, progress)

        if new_game:
            new_game = False
            ModalDialog('Robot Obstacle Course', [
                'Welcome to the game. The aim is to use the arrows to program in directions for the robot to move so it can get all the keys. Once all keys have been collected then the door completes the level. If a hammer is collected it will break a single obstacle.',
                'The keys to use are as follows:',
                '',
                'Up, down, left, right: program in the robot movements.',
                'Enter: execute the programmed movements.',
                'Backspace: remove the last programmed movement.',
                'N: new game.',
                'T: toggle "training" mode to show where the robot would move.',
                'F: toggle "fast" mode to speed up the robot\'s movement.',
                'R: reset the level'
            ]).show()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit()

            if event.type == pygame.KEYDOWN:
                handled = False
                if not moving:
                    if event.key == pygame.K_RETURN:
                        moving = True
                        handled = True
                        progress.level_turns += 1
                    elif event.key == pygame.K_BACKSPACE:
                        handled = True
                        progress.remove_last_position()
                    else:
                        direction, position = get_direction(event.key, progress)
                        handled = direction is not None
                        progress.add_move(direction, position)

                if not handled:
                    if event.key == pygame.K_r:
                        progress.reset_level()
                        grid = generate_grid(progress)
                    if event.key == pygame.K_n:
                        progress.new_game()
                        grid = generate_grid(progress)
                        new_game = True
                    elif event.key == pygame.K_t:
                        progress.toggle_training_mode()
                    elif event.key == pygame.K_f:
                        progress.toggle_fast_mode()
                    elif event.key == pygame.K_s:
                        progress.toggle_score()
                    elif event.key == pygame.K_w:
                        progress.toggle_use_walls()
                    elif event.key == pygame.K_h:
                        progress.bonus_hammer()
                    elif event.key == pygame.K_l:
                        shift = event.mod & pygame.KMOD_LSHIFT | event.mod & pygame.KMOD_RSHIFT | event.mod & pygame.KMOD_SHIFT
                        progress.add_level(-1 if shift else 1)
                        grid = generate_grid(progress)

        if moving:
            complete, moving = move_robot(grid, progress)
            if complete:
                ModalDialog(f'Level {progress.level} complete', ['Great work!']).show()
                progress.add_level(1)
                grid = generate_grid(progress)

    pygame.quit()

if __name__ == "__main__":
    main()
