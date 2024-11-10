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
def create_empty_grid():
    return [[1 for _ in range(COLS)] for _ in range(ROWS)]

#Prim's algorithm
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

#Complexity Analysis O (N x M)
def remove_dead_ends(grid):
    for row in range(1, ROWS - 1):
        for col in range(1, COLS - 1):
            if grid[row][col] == 0:
                neighbors = [(row + dx, col + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
                open_neighbors = [(nx, ny) for nx, ny in neighbors if grid[nx][ny] == 0]

                if len(open_neighbors) == 1:
                    #Complexity Anaylsis O(1)
                    neighbor_to_open = random.choice(neighbors)
                    grid[neighbor_to_open[0]][neighbor_to_open[1]] = 0

#Complexity Analysis O (N x M)
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
            color = BLACK if grid[row][col] == 0 else WHITE  
            pygame.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

            if pellets[row][col] == 1:
                pygame.draw.circle(screen, YELLOW, (col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 6)

def draw_player():
    pygame.draw.circle(screen, BLUE, (player_pos[1] * TILE_SIZE + TILE_SIZE // 2, player_pos[0] * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2)

#Complexity Analysis O (1)
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
