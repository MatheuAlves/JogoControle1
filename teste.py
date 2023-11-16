import pygame
import sys

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the screen
screen_width, screen_height = 800, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Number Input")

# Set up the clock
clock = pygame.time.Clock()

# Number variables
number_value_1 = 0.0
number_value_2 = 0.0
font = pygame.font.Font(None, 36)

# Icon variables
icon_size = 30
icon_spacing = 20
icon_center_y = 150

icons_options = [
    {
        "group" : 1,
        "icons" : [
            {"rect": pygame.Rect(160, icon_center_y, icon_size, icon_size), "text": "+1"},
            {"rect": pygame.Rect(160 + icon_size + icon_spacing, icon_center_y, icon_size, icon_size), "text": "-1"},
            {"rect": pygame.Rect(160 + 2 * (icon_size + icon_spacing), icon_center_y, icon_size, icon_size), "text": "+0.1"},
            {"rect": pygame.Rect(160 + 3 * (icon_size + icon_spacing), icon_center_y, icon_size, icon_size), "text": "-0.1"}
        ]
    },
    {   
        "group" : 2,
        "icons" : [
            {"rect": pygame.Rect(400, icon_center_y, icon_size, icon_size), "text": "+1"},
            {"rect": pygame.Rect(400 + icon_size + icon_spacing, icon_center_y, icon_size, icon_size), "text": "-1"},
            {"rect": pygame.Rect(400 + 2 * (icon_size + icon_spacing), icon_center_y, icon_size, icon_size), "text": "+0.1"},
            {"rect": pygame.Rect(400 + 3 * (icon_size + icon_spacing), icon_center_y, icon_size, icon_size), "text": "-0.1"}
        ]
    }
]

def handle_icon_press(mouse_pos, icons_list):
    for icon in icons_list:
        if icon["rect"].collidepoint(mouse_pos):
            return icon["text"]
    return None

# Main game loop
while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            for icons in icons_options:
                pressed_icon = handle_icon_press(event.pos, icons["icons"])
                if pressed_icon is not None:
                    if pressed_icon == "+1":
                        match icons["group"]:
                            case 1:
                                number_value_1 += 1
                            case 2:
                                number_value_2 += 1
                    elif pressed_icon == "-1":
                        match icons["group"]:
                            case 1:
                                number_value_1 += -1
                            case 2:
                                number_value_2 += -1
                    elif pressed_icon == "+0.1":
                        match icons["group"]:
                            case 1:
                                number_value_1 += 0.1
                            case 2:
                                number_value_2 += 0.1
                    elif pressed_icon == "-0.1":
                        match icons["group"]:
                            case 1:
                                number_value_1 += -0.1
                            case 2:
                                number_value_2 += -0.1
                    break

    # Draw number value
    text = font.render("{:.1f}".format(number_value_1), True, BLACK)
    text_rect = text.get_rect(center=(screen_width // 4, icon_center_y - 50))
    screen.blit(text, text_rect)

    # Draw number value for the second set
    text = font.render("{:.1f}".format(number_value_2), True, BLACK)
    text_rect = text.get_rect(center=(3 * screen_width // 4, icon_center_y - 50))
    screen.blit(text, text_rect)
    
    for group in icons_options:
        for icon in group["icons"]:
            text = font.render(icon["text"], True, BLACK)
            text_rect = text.get_rect(center=icon["rect"].center)
            screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(30)
