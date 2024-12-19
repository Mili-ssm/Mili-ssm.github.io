import numpy as np
import pygame

# Initialize grid with random values
N = 100
grid = np.random.randint(2, size=(N, N))

# Use JIT compilation to speed up cell updates
def update_cell(grid, i, j):
    # Get number of alive neighbors
    alive_neighbors = (
        grid[i-1, j-1] + grid[i-1, j] + grid[i-1, j+1] +
        grid[i, j-1] + grid[i, j+1] +
        grid[i+1, j-1] + grid[i+1, j] + grid[i+1, j+1]
    )

    # Apply rules of the game
    if grid[i, j] == 1:
        if alive_neighbors < 2 or alive_neighbors > 3:
            return 0
        else:
            return 1
    else:
        if alive_neighbors == 3:
            return 1
        else:
            return 0

# Initialize Pygame
pygame.init()

# Set up screen
SCREEN_SIZE = (800, 600)
screen = pygame.display.set_mode(SCREEN_SIZE)

# Set up clock
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update grid
    new_grid = np.empty((N, N))
    for i in range(1, N-1):
        for j in range(1, N-1):
            new_grid[i, j] = update_cell(grid, i, j)

    # Get size of window
    window_size = pygame.display.get_surface().get_size()

    # Calculate number of rows and columns to display
    n_cols = window_size[0] // 8
    n_rows = window_size[1] // 8

    # Calculate size of each cell
    cell_width = window_size[0] // n_cols
    cell_height = window_size[1] // n_rows

    # Draw grid on screen
    screen.fill((0, 0, 0))
    for i in range(n_cols):
        for j in range(n_rows):
            if grid[i, j] == 1:
                color = (255, 255, 255)
            else:
                color = (0, 0, 0)
            rect = (i*cell_width, j*cell_height, cell_width, cell_height)

class Cell:
    def __init__(self, state):
        self.state = state

    def update(self, neighbors):
        pass

class BasicCell(Cell):
    def update(self, neighbors):
        # Get number of alive neighbors
        alive_neighbors = sum(neighbors)

        # Apply rules of the game
        if self.state == 1:
            if alive_neighbors < 2 or alive_neighbors > 3:
                return 0
            else:
                return 1
        else:
            if alive_neighbors == 3:
                return 1
            else:
                return 0

class AdjacentCell(Cell):
    def update(self, neighbors):
        # Count number of alive and dead neighbors
        alive_neighbors = sum(neighbors)
        dead_neighbors = len(neighbors) - alive_neighbors

        # Apply different rules depending on state
        if self.state == 1:
            if alive_neighbors == 2 or alive_neighbors == 3:
                return 1
            else:
                return 0
        else:
            if alive_neighbors == 3 and dead_neighbors == 1:
                return 1
            else:
                return 0


# Main loop
generation = 0
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Create new grid
    new_grid = np.empty((N, N), dtype=object)
    for i in range(1, N-1):
        for j in range(1, N-1):
            # Get current cell and its neighbors
            cell = grid[i, j]
            neighbors = [
                grid[i-1, j-1], grid[i-1, j], grid[i-1, j+1],
                grid[i, j-1], grid[i, j+1],
                grid[i+1, j-1], grid[i+1, j], grid[i+1, j+1]
            ]

            # Create new cell with updated state
            if isinstance(cell, BasicCell):
                new_grid[i, j] = BasicCell(cell.update(neighbors))
            elif isinstance(cell, AdjacentCell):
                new_grid[i, j] = AdjacentCell(cell.update(neighbors))

    # Set window title to show generation number
    pygame.display.set_caption(f"Generation {generation}")

    # Draw grid on screen
    screen.fill((0, 0, 0))
    for i in range(n_cols):
        for j in range(n_rows):
            # Get current cell
            cell = grid[i, j]

            # Set color based on cell's state
            if cell.state == 1:
                color = (255, 255, 255)
            else:
                color = (0, 0, 0)

            # Draw cell on screen
            rect = (i*cell_width, j*cell_height, cell_width, cell_height)
            pygame.draw.rect(screen, color, rect)

    # Swap grids
    grid = new_grid
    generation += 1

    # Update screen
    pygame.display.flip()

    # Limit frame rate
    clock.tick(30)

# Clean up
pygame.quit()
