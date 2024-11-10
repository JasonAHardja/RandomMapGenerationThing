import pygame
import random

WIDTH, HEIGHT = 600, 600 
TILE_SIZE = 20  
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE  

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("dumb ahh pack man")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0) 

player_pos = [1, 1]  

# Graph Traversal (DFS for Maze Generation)
def create_empty_grid():
    return [[1 for _ in range(COLS)] for _ in range(ROWS)]  

def generate_maze(grid):
    def dfs(x, y):
        # Randomization Techniques (Randomized Direction Choice) 
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)  

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and grid[nx][ny] == 1:
                grid[x + dx // 2][y + dy // 2] = 0  
                grid[nx][ny] = 0  
                dfs(nx, ny)

    grid[1][1] = 0  
    dfs(1, 1)  

# Pathfinding Integration (optional for now, like BFS for player's start position or something like that)

# Randomization Techniques (Adding Pellets in Random Open Spaces)
def add_pellets(grid):
    pellets = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == 0:
                pellets[row][col] = 1  
    return pellets

def draw_grid(grid, pellets):
    for row in range(ROWS):
        for col in range(COLS):
            # Maze and Game Design Pattern (Visual representation of game states) 
            color = WHITE if grid[row][col] == 1 else BLACK
            pygame.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

            
            if pellets[row][col] == 1:
                pygame.draw.circle(screen, YELLOW, (col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 6)

def draw_player():
    pygame.draw.circle(screen, BLUE, (player_pos[1] * TILE_SIZE + TILE_SIZE // 2, player_pos[0] * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2)

def move_player(grid, pellets, direction):
    row, col = player_pos
    if direction == 'UP' and row > 0 and grid[row - 1][col] == 0:
        player_pos[0] -= 1
    elif direction == 'DOWN' and row < ROWS - 1 and grid[row + 1][col] == 0:
        player_pos[0] += 1
    elif direction == 'LEFT' and col > 0 and grid[row][col - 1] == 0:
        player_pos[1] -= 1
    elif direction == 'RIGHT' and col < COLS - 1 and grid[row][col + 1] == 0:
        player_pos[1] += 1

    
    row, col = player_pos
    if pellets[row][col] == 1:
        pellets[row][col] = 0  

def main():
    grid = create_empty_grid()  
    generate_maze(grid)  
    pellets = add_pellets(grid)  

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_player(grid, pellets, 'UP')
                elif event.key == pygame.K_DOWN:
                    move_player(grid, pellets, 'DOWN')
                elif event.key == pygame.K_LEFT:
                    move_player(grid, pellets, 'LEFT')
                elif event.key == pygame.K_RIGHT:
                    move_player(grid, pellets, 'RIGHT')

        screen.fill(WHITE)
        draw_grid(grid, pellets)
        draw_player()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()


