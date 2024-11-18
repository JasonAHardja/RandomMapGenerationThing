import pygame
import random

# Constants
WIDTH, HEIGHT = 600, 600  
TILE_SIZE = 20  
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE  
SCOREBOARD_HEIGHT = 40  

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200) 

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + SCOREBOARD_HEIGHT))
pygame.display.set_caption("pack man when he packs the man idk never played before")

player_pos = [1, 1]  

score = 0

def create_empty_grid():
    return [[1 for _ in range(COLS)] for _ in range(ROWS)]

def generate_maze(grid):
    start_x, start_y = 1, 1
    grid[start_x][start_y] = 0
    walls = [(start_x + dx, start_y + dy) for dx, dy in [(2, 0), (0, 2), (-2, 0), (0, -2)] if 0 <= start_x + dx < ROWS and 0 <= start_y + dy < COLS]

    while walls:
        wx, wy = random.choice(walls)
        walls.remove((wx, wy))

        neighbors = [(wx + dx, wy + dy) for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)] if 0 <= wx + dx < ROWS and 0 <= wy + dy < COLS]
        passages = [(nx, ny) for nx, ny in neighbors if grid[nx][ny] == 0]

        if len(passages) == 1:
            grid[wx][wy] = 0
            px, py = passages[0]
            grid[(wx + px) // 2][(wy + py) // 2] = 0 

            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nx, ny = wx + dx, wy + dy
                if 0 <= nx < ROWS and 0 <= ny < COLS and grid[nx][ny] == 1:
                    walls.append((nx, ny))

    remove_dead_ends(grid)

def remove_dead_ends(grid):
    for row in range(1, ROWS - 1):
        for col in range(1, COLS - 1):
            if grid[row][col] == 0:
                wall_count = sum(
                    1 for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    if grid[row + dx][col + dy] == 1
                )
                if wall_count >= 3:
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        if grid[row + dx][col + dy] == 1:
                            grid[row + dx][col + dy] = 0
                            break

def add_pellets(grid, ghost_room):
    pellets = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == 0 and not (ghost_room[1] <= row <= ghost_room[3] and ghost_room[0] <= col <= ghost_room[2]):
                pellets[row][col] = 1
    return pellets

def draw_grid(grid, pellets, ghost_room):
    for row in range(ROWS):
        for col in range(COLS):
            color = BLACK if grid[row][col] == 0 else WHITE  
            pygame.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE + SCOREBOARD_HEIGHT, TILE_SIZE, TILE_SIZE))

            if pellets[row][col] == 1:
                pygame.draw.circle(screen, YELLOW, (col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + SCOREBOARD_HEIGHT + TILE_SIZE // 2), TILE_SIZE // 6)

    ghost_start_x, ghost_start_y = ghost_room[0] * TILE_SIZE, ghost_room[1] * TILE_SIZE + SCOREBOARD_HEIGHT
    ghost_width = (ghost_room[2] - ghost_room[0] + 1) * TILE_SIZE
    ghost_height = (ghost_room[3] - ghost_room[1] + 1) * TILE_SIZE
    pygame.draw.rect(screen, RED, (ghost_start_x, ghost_start_y, ghost_width, ghost_height))

def draw_player():
    pygame.draw.circle(screen, BLUE, (player_pos[1] * TILE_SIZE + TILE_SIZE // 2, player_pos[0] * TILE_SIZE + SCOREBOARD_HEIGHT + TILE_SIZE // 2), TILE_SIZE // 2)

def draw_scoreboard():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, SCOREBOARD_HEIGHT))  # Scoreboard bar
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 5))

def move_player(grid, pellets, direction, ghost_room):
    global score  
    row, col = player_pos
    if direction == 'UP' and row > 0 and grid[row - 1][col] == 0 and not (ghost_room[1] <= row - 1 <= ghost_room[3] and ghost_room[0] <= col <= ghost_room[2]):
        player_pos[0] -= 1
    elif direction == 'DOWN' and row < ROWS - 1 and grid[row + 1][col] == 0 and not (ghost_room[1] <= row + 1 <= ghost_room[3] and ghost_room[0] <= col <= ghost_room[2]):
        player_pos[0] += 1
    elif direction == 'LEFT' and col > 0 and grid[row][col - 1] == 0 and not (ghost_room[1] <= row <= ghost_room[3] and ghost_room[0] <= col - 1 <= ghost_room[2]):
        player_pos[1] -= 1
    elif direction == 'RIGHT' and col < COLS - 1 and grid[row][col + 1] == 0 and not (ghost_room[1] <= row <= ghost_room[3] and ghost_room[0] <= col + 1 <= ghost_room[2]):
        player_pos[1] += 1

    row, col = player_pos
    if pellets[row][col] == 1:
        pellets[row][col] = 0
        score += 100  

def generate_map_patterns():
    maps = []
    for _ in range(3):
        grid = create_empty_grid()
        generate_maze(grid)
        maps.append(grid)
    return maps

def main():
    global score  
    map_patterns = generate_map_patterns()  
    current_map = random.choice(map_patterns)  

    ghost_room_width = 10
    ghost_room_height = 4
    ghost_room_start_col = (COLS - ghost_room_width) // 2
    ghost_room_start_row = (ROWS - ghost_room_height) // 2
    ghost_room_end_col = ghost_room_start_col + ghost_room_width - 1
    ghost_room_end_row = ghost_room_start_row + ghost_room_height - 1
    ghost_room = (ghost_room_start_col, ghost_room_start_row, ghost_room_end_col, ghost_room_end_row)

    pellets = add_pellets(current_map, ghost_room) 

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_player(current_map, pellets, 'UP', ghost_room)
                elif event.key == pygame.K_DOWN:
                    move_player(current_map, pellets, 'DOWN', ghost_room)
                elif event.key == pygame.K_LEFT:
                    move_player(current_map, pellets, 'LEFT', ghost_room)
                elif event.key == pygame.K_RIGHT:
                    move_player(current_map, pellets, 'RIGHT', ghost_room)

        screen.fill(WHITE)
        draw_scoreboard()  
        draw_grid(current_map, pellets, ghost_room)
        draw_player()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
