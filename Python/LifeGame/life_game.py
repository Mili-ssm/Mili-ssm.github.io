"""A simple implementation of Conway's Game of Life."""
import numpy as np
import pygame
from scipy.ndimage import convolve


def create_grid(width: int, height: int) -> np.ndarray:
    """Create a grid of cells."""
    grid = np.random.choice([0, 1], size=(width, height))
    return grid


def count_neighbors(grid: np.ndarray) -> np.ndarray:
    """Count the number of neighbors for each cell."""
    mask = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    return convolve(grid, mask, mode="constant", cval=0.0)


def tick(grid: np.ndarray) -> None:
    """Update the grid."""
    neighbors_count = count_neighbors(grid)
    grid[(grid == 1) & ((neighbors_count < 2) | (neighbors_count > 3))] = 0
    grid[(grid == 0) & (neighbors_count == 3)] = 1


def draw_grid(grid: np.ndarray, screen: pygame.Surface, cell_size: int) -> None:
    """Draw the grid."""
    # Create a surface from the grid
    surface = pygame.surfarray.make_surface(grid.T * 255)

    # Scale the surface to the desired cell size
    surface = pygame.transform.scale(
        surface, (grid.shape[1] * cell_size, grid.shape[0] * cell_size)
    )

    # Blit the surface to the screen
    screen.blit(surface, (0, 0))


def main() -> None:
    """Run the game."""
    pygame.init()
    width, height = 1000, 1000
    cell_size = 1
    grid_width, grid_height = width // cell_size, height // cell_size
    screen = pygame.display.set_mode((width, height))
    print(type(screen))
    pygame.display.set_caption("Conway's Game of Life.")

    clock = pygame.time.Clock()

    grid = create_grid(grid_width, grid_height)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        draw_grid(grid, screen, cell_size)
        pygame.display.set_caption('Juego de Sant  -- FPS : {}'.format(clock.get_fps()))
        pygame.display.flip()
        tick(grid)

        clock.tick()
        #print(f"FPS: {clock.get_fps()}")
    pygame.quit()


if __name__ == "__main__":
    main()
