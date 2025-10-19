import pygame

def get_mouse_input():
    """Get the mouse input for the game."""
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return mouse_x, mouse_y

def handle_events():
    """Handle user input events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 'QUIT'
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                return 'LEFT_CLICK', get_mouse_input()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'QUIT'
    return None