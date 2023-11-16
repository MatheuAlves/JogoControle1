import pygame
import sys
import subprocess
import time

# Iniciar o Pygame
pygame.init()

# Configurações da tela do Pygame
width = 800
height = 600
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
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
    
    # Texto
    text = font.render('Aperte espaço para iniciar o jogo', True, black)
    text_rect = text.get_rect(center=(width / 2, 450))

    # Desenhar retângulo branco de fundo
    pygame.draw.rect(screen, white, (0, 400, width , 100))

    # Desenhar o texto no centro da tela
    screen.blit(text, text_rect)


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
    # Verificar se a tecla de espaço foi pressionada
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        running = False
        # Fechar a janela antes de abrir o subprocesso
        pygame.quit()

        # Adicionar um pequeno atraso para garantir que a janela seja fechada antes de abrir o subprocesso
        time.sleep(0.5)
        subprocess.run(["python", "game.py"])  # Executar o script 'jogo.py'
        # Finalizar o Pygame
        pygame.quit()
        sys.exit()


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
