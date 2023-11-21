import pygame
import sys
import subprocess
import time
import pygame.gfxdraw

# Inicialização do Pygame
pygame.init()

# Configurações da tela
width, height = 800, 600
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Menu Pygame")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PINK = (252, 108, 133)

# Carregando imagens
background_image = pygame.image.load("images/background1.jpg")
background_image = pygame.transform.scale(background_image, (1200, 900))
sound_button_image = pygame.image.load("images/sound.png")
sound_button_image = pygame.transform.scale(sound_button_image, (30, 30))
muted_button_image = pygame.image.load("images/mute.png")
muted_button_image = pygame.transform.scale(muted_button_image, (30, 30))
title_image = pygame.image.load("images/CarRace.png")

# Carregando fonte
font = pygame.font.Font(None, 36)

# Música de fundo
pygame.mixer.music.load("songs/menu.mp3")
pygame.mixer.music.play(-1)

# Variável para rastrear se o som está mudo ou não
is_muted = False

# Definindo as áreas clicáveis dos botões
play_button_rect = pygame.Rect((width // 2 - 50, 330, 100, 50))
info_button_rect = pygame.Rect((width // 2 - 50, 400, 100, 50))
mute_button_rect = pygame.Rect((770, 570, 30, 30))
info_close_rect = pygame.Rect((698, 52, 50, 50))

# Loop principal
running = True
info_box = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                pygame.mixer.Sound("songs/confirm.mp3").play()
                pygame.quit()
                time.sleep(0.5)
                subprocess.run(["python", "forms.py"])
                running = False
                break
            if info_button_rect.collidepoint(event.pos):
                pygame.mixer.Sound("songs/confirm.mp3").play()
                info_box = True
            if mute_button_rect.collidepoint(event.pos):
                is_muted = not is_muted
                if is_muted:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            if info_close_rect.collidepoint(event.pos):
                info_box = False

    screen.fill(WHITE)
    screen.blit(background_image, (-200, -100))

    # Desenhar os botões com gradiente
    def draw_gradient_rect(surface, color_top, color_bottom, rect):
        pygame.draw.rect(surface, color_top, rect)
        for y in range(rect.top, rect.bottom):
            t = (y - rect.top) / (rect.height - 1)
            color = (
                int(color_top[0] * (1 - t) + color_bottom[0] * t),
                int(color_top[1] * (1 - t) + color_bottom[1] * t),
                int(color_top[2] * (1 - t) + color_bottom[2] * t)
            )
            pygame.gfxdraw.hline(surface, rect.left, rect.right - 1, y, color)

    draw_gradient_rect(screen, BLUE, PINK, play_button_rect)
    draw_gradient_rect(screen, BLUE, PINK, info_button_rect)

    pygame.draw.rect(screen, BLACK, play_button_rect, 2)
    pygame.draw.rect(screen, BLACK, info_button_rect, 2)

    play_button_text = font.render("Jogar", True, BLACK)
    info_button_text = font.render("Info", True, BLACK)

    screen.blit(play_button_text, (width // 2 - play_button_text.get_width() // 2, 340))
    screen.blit(info_button_text, (width // 2 - info_button_text.get_width() // 2, 415))

    # Escolha a imagem do botão de mudo com base no estado de is_muted
    mute_button_rect = screen.blit(muted_button_image if is_muted else sound_button_image, (770, 570))

    # Título "CAR RACE" acima do botão "Jogar"
    screen.blit(title_image, (width // 2 - title_image.get_width() // 2, 100))

    if info_box:
        pygame.draw.rect(screen, BLACK, (50, 50, 700, 500))
        pygame.draw.rect(screen, WHITE, (50, 50, 700, 500), 2)
        info_text = "Central de Informações"
        text_surface = font.render(info_text, True, WHITE)
        screen.blit(text_surface, (60, 70))
        info_text1 = "O Jogo aleatoriza uma função de Transferência para "
        text_surface1 = font.render(info_text1, True, WHITE)
        screen.blit(text_surface1, (60, 150))
        info_text2 = "ambos os jogadores. Você deve escolher qual controle"
        text_surface2 = font.render(info_text2, True, WHITE)
        screen.blit(text_surface2, (60, 180))
        info_text3 = "usará para vencer esse desafio."
        text_surface3 = font.render(info_text3, True, WHITE)
        screen.blit(text_surface3, (60, 210))
        info_text4 = "Temos opções P, I e D, e você pode alterar os valores"
        text_surface4 = font.render(info_text4, True, WHITE)
        screen.blit(text_surface4, (60, 240))
        info_text5 = "de cada um e pisar no acelerador. BOM JOGO!"
        text_surface5 = font.render(info_text5, True, WHITE)
        screen.blit(text_surface5, (60, 270))

        info_close_image = pygame.image.load("images/botao-fechar.png")
        info_close_image = pygame.transform.scale(info_close_image, (50, 50))
        screen.blit(info_close_image, (698, 52))

    pygame.display.flip()

# Encerrar o Pygame
pygame.quit()
sys.exit()
