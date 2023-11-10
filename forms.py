import pygame
import sys

# Iniciar o Pygame
pygame.init()

# Configurações da tela do Pygame
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Form")

# Cores
white = (255, 255, 255)
black = (0, 0, 0)

# Fonte
font = pygame.font.Font(None, 36)

# Função para desenhar botão de rádio
def draw_radio_button(surface, x, y, text, selected):
    radio_button_rect = pygame.Rect(x, y, 20, 20)
    pygame.draw.rect(surface, white, radio_button_rect, 2)

    if selected:
        pygame.draw.circle(surface, white, (x + 10, y + 10), 8)

    text_surface = font.render(text, True, white)
    surface.blit(text_surface, (x + 30, y))

# Loop principal do Pygame
running = True
selected_option = {
    "P" : False,
    "I" : False,
    "D" : False
}

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 100 <= mouse_x <= 300 and 100 <= mouse_y <= 130:
                if(selected_option["P"]):
                    selected_option["P"] = False
                    if(selected_option["D"]):
                        selected_option["D"] = False
                else:
                    selected_option["P"] = True
            elif 100 <= mouse_x <= 300 and 150 <= mouse_y <= 180:
                if(selected_option["I"]):
                    selected_option["I"] = False
                else:
                    selected_option["I"] = True
            elif 100 <= mouse_x <= 300 and 200 <= mouse_y <= 230:
                if(selected_option["D"]):
                    selected_option["D"] = False
                else:
                    selected_option["D"] = True
                    selected_option["P"] = True

    # Limpar a tela
    screen.fill(black)

    # Desenhar botões de rádio
    draw_radio_button(screen, 100, 100, "Proporcional", selected_option["P"])
    draw_radio_button(screen, 100, 150, "Integral", selected_option["I"])
    draw_radio_button(screen, 100, 200, "Derivativo", selected_option["D"])

    # Atualizar a tela
    pygame.display.flip()

# Finalizar o Pygame
pygame.quit()
sys.exit()
