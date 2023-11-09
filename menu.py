import pygame
import sys
import subprocess


# Inicialização do Pygame
pygame.init()

# Configurações da tela
width, height = 500, 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Menu Pygame")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Carregando imagens
background_image = pygame.image.load("images/background.png")
play_button_image = pygame.image.load("images/JOGAR.png")
info_button_image = pygame.image.load("images/INFO.PNG")
info_button_image = pygame.transform.scale(info_button_image, (125, 50))
# Imagem do botão de mudo quando o som está ativado
sound_button_image = pygame.image.load("images/sound.png")
sound_button_image = pygame.transform.scale(sound_button_image, (100, 100))
# Imagem do botão de mudo quando o som está mudo
muted_button_image = pygame.image.load("images/mute.png")
muted_button_image = pygame.transform.scale(muted_button_image, (100, 100))

# Carregando fonte
font = pygame.font.Font(None, 36)

# Música de fundo
pygame.mixer.music.load("songs/menu.mp3")
pygame.mixer.music.play(-1)

# Variável para rastrear se o som está mudo ou não
is_muted = False

# Loop principal
running = True
info_box = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                if play_button_rect.collidepoint(event.pos):
                    pygame.mixer.Sound("songs/confirm.mp3").play()
                    subprocess.run(["python", "game.py"])  # Executar o script 'jogo.py'
                    running = False
                    break

            if info_button_rect.collidepoint(event.pos):
                pygame.mixer.Sound("songs/confirm.mp3").play()
                info_box = True
            if mute_button_rect.collidepoint(event.pos):
                # Alternar entre som ativado e desativado
                is_muted = not is_muted
                if is_muted:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))

    play_button_rect = screen.blit(play_button_image, (width // 2 - play_button_image.get_width() // 2, 300))
    info_button_rect = screen.blit(info_button_image, (width // 2 - info_button_image.get_width() // 2, 400))

    # Escolha a imagem do botão de mudo com base no estado de is_muted
    if is_muted:
        mute_button_rect = screen.blit(muted_button_image, (400, 400))
    else:
        mute_button_rect = screen.blit(sound_button_image, (400, 400))

    # Título "CAR RACE" acima do botão "Jogar"
    title_text = font.render("CAR RACE", True, BLACK)
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 200))

    if info_box:
        pygame.draw.rect(screen, BLACK, (50, 50, 400, 200))
        info_text = "Você deve colocar as /n "
        text_surface = font.render(info_text, True, WHITE)
        screen.blit(text_surface, (60, 70))

        info_close_image = pygame.image.load("images/close.png")
        info_close_image = pygame.transform.scale(info_close_image, (30, 30))
        info_close_rect = pygame.draw.rect(screen, BLACK, (420, 50, 30, 30))
        info_close_rect = screen.blit(info_close_image, (420, 50))
        if info_close_rect.collidepoint(event.pos):
                info_box = False

    pygame.display.flip()

# Encerrar o Pygame
pygame.quit()
sys.exit()
