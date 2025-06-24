import pygame
import sys
import random

# Dimensions de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
CELL_WIDTH = SCREEN_WIDTH // 3
CELL_HEIGHT = SCREEN_HEIGHT // 3
FONT_SIZE = 60
TEXT_COLOR = (255, 0, 0)  # Rouge
BACKGROUND_COLOR = (255, 255, 255)  # Blanc

def get_grid_cells(width, height):
    cells = []
    for row in range(3):
        for col in range(3):
            # Centre de chaque cellule
            x = col * CELL_WIDTH + CELL_WIDTH // 2
            y = row * CELL_HEIGHT + CELL_HEIGHT // 2
            cells.append((x, y))
    return cells

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("3x3 Grid with Random Number Placement")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, FONT_SIZE)

    cells = get_grid_cells(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Numéros de 1 à 9 mélangés aléatoirement
    numbers = list(range(1, 10))
    random.shuffle(numbers)

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        # Affiche les numéros dans la grille selon l’ordre mélangé
        for pos, num in zip(cells, numbers):
            text_surface = font.render(str(num), True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center=pos)
            screen.blit(text_surface, text_rect)

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
