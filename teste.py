import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Text Example")

# Set up the font
font = pygame.font.Font(None, 36)  # You can specify the font file or use None for the default font

# Set up the texts
text1 = "Hello, Pygame!"
text2 = "Welcome to the World of Games!"
text1_surface = font.render(text1, True, (255, 255, 255))  # Render the text with white color
text2_surface = font.render(text2, True, (255, 255, 255))

# Calculate positions
text1_pos = (width // 2 - text1_surface.get_width() // 2, height // 2 - text1_surface.get_height())
text2_pos = (width // 2 - text2_surface.get_width() // 2, height // 2 + text1_surface.get_height())

# Set up the button
button_rect = pygame.Rect(width // 2 - 50, height // 2 + text1_surface.get_height() + 20, 100, 40)
button_color = (0, 128, 255)

# Set up the line
line_start = (width // 2, height // 2)
line_end = (width // 2 + 10, height // 2)
line_size = 2
# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click is inside the button
            if button_rect.collidepoint(event.pos):
                # Redraw the texts with new content
                text1 = "Text Updated!"
                text2 = "Click Again!"
                text1_surface = font.render(text1, True, (255, 255, 255))
                text2_surface = font.render(text2, True, (255, 255, 255))
                # Remove the line
                line_start = (width // 2, height // 2)
                line_end = (width // 2, height // 2)
                line_size = 0

    # Draw the texts, line, and button onto the screen
    screen.fill((0, 0, 0))  # Fill the screen with a black background
    screen.blit(text1_surface, text1_pos)
    screen.blit(text2_surface, text2_pos)

    # Draw the line
    pygame.draw.line(screen, (255, 255, 255), line_start, line_end, line_size)

    # Draw the button
    pygame.draw.rect(screen, button_color, button_rect)
    button_font = pygame.font.Font(None, 24)
    button_text = button_font.render("Update Text", True, (255, 255, 255))
    screen.blit(button_text, (width // 2 - button_text.get_width() // 2, height // 2 + text1_surface.get_height() + 30))

    pygame.display.flip()
