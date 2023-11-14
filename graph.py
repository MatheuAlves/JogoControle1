import pygame
import sys
import numpy as np
import matplotlib.backends.backend_agg as agg

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
pygame.display.set_caption("Pygame Graph Example")

# Set up the initial screen
current_screen = [1]

# Create buttons for screen 1 and screen 2
button_screen1 = Button(300, 200, 200, 50, blue, "Open Graph", action=lambda: current_screen.__setitem__(0, 2))
button_quit = Button(300, 300, 200, 50, (255, 0, 0), "Quit", action=sys.exit)

# Create a Pygame surface for the graph
graph_surface = pygame.Surface((width, height))

# Function to plot a simple graph
def plot_graph(surface):
    # Generate example data
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)

    # Plot the graph using Matplotlib
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x, y)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title('Graph Title')

    # Render the Matplotlib figure onto the Pygame surface
    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()

    # Convert the raw data to a Pygame surface
    img = pygame.image.fromstring(raw_data, fig.get_size(), "RGB")
    surface.blit(img, (0, 0))

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen[0] == 2 and button_quit.is_clicked(pygame.mouse.get_pos()):
                button_quit.action()

    # Clear the screen
    screen.fill(white)

    # Draw buttons based on the current screen
    if current_screen[0] == 1:
        button_screen1.draw(screen, black)
    elif current_screen[0] == 2:
        button_quit.draw(screen, black)

        # Draw the graph on the graph_surface
        plot_graph(graph_surface)

        # Draw the graph surface onto the main screen
        screen.blit(graph_surface, (0, 0))

    # Update the display
    pygame.display.flip()

    clock.tick(60)  # Cap the frame rate to 60 frames per second

# Quit Pygame
pygame.quit()
sys.exit()
