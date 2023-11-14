import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up screen dimensions
width, height = 800, 600

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)

# Set up fonts
font = pygame.font.Font(None, 36)

# Create a button class
class Button:
    def __init__(self, x, y, width, height, color, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.action = action

    def draw(self, screen, outline=None):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        if outline:
            pygame.draw.rect(screen, outline, self.rect, 2)

        if self.text:
            font_surface = font.render(self.text, True, black)
            font_rect = font_surface.get_rect(center=self.rect.center)
            screen.blit(font_surface, font_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Set up the Pygame screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Button Example")

# Set up the initial screen
current_screen = [1]

# Create buttons for screen 1 and screen 2
button_screen1 = Button(0, 0, 200, 50, blue, "Open Screen 2", action=lambda: current_screen.__setitem__(0, 2))
button_screen2 = Button(0, 0, 200, 50, blue, "Open Screen 1", action=lambda: current_screen.__setitem__(0, 1))

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen[0] == 1 and button_screen1.is_clicked(pygame.mouse.get_pos()):
                button_screen1.action()
            elif current_screen[0] == 2 and button_screen2.is_clicked(pygame.mouse.get_pos()):
                button_screen2.action()

    # Clear the screen
    screen.fill(white)

    # Draw buttons based on the current screen
    if current_screen[0] == 1:
        button_screen1.draw(screen, black)
    elif current_screen[0] == 2:
        button_screen2.draw(screen, black)

    # Update the display
    pygame.display.flip()

    clock.tick(60)  # Cap the frame rate to 60 frames per second

# Quit Pygame
pygame.quit()
sys.exit()
