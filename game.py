import pygame
from pygame.locals import *
import random
import subprocess
import time
import sys
import ast
import numpy as np
import control.matlab as clt

TOTAL_TIME = 20.0

subprocess_data_str = sys.argv[1]

try:
    subprocess_data = ast.literal_eval(subprocess_data_str)
    if not isinstance(subprocess_data, dict):
        raise ValueError("Invalid data format")
except (ValueError, SyntaxError) as e:
    print(f"Error converting string to dictionary: {e}")
    sys.exit(1)

sys.stdout.flush()

pygame.init()
# create the window
width = 800
height = 600
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Car Game')

# colors
gray = (100, 100, 100)
green = (76, 208, 56)
red = (255, 0, 0)
white = (255, 255, 255)
yellow = (238, 219, 0)
black = (0, 0, 0)
purple = (128, 0, 128)


# Música de fundo
pygame.mixer.Sound("songs/alarm.mp3").play()
time.sleep(0.3)
pygame.mixer.music.load("songs/game.mp3")
pygame.mixer.music.play(-1)

# road and marker sizes
road_width = 200
marker_width = 10
marker_height = 50

# lane coordinates
lane1 = 200
lane2 = 590

# Defina as coordenadas iniciais e finais da linha
line_start = (width // 2, 0)
line_end = (width // 2, height)

# road and edge markers
road1 = (100, 0, road_width, height)
road2 = (500, 0, road_width, height)
left_edge_marker = (100, 0, marker_width, height)
right_edge_marker = (300, 0, marker_width, height)

left_edge_marker2 = (490, 0, marker_width, height)
right_edge_marker2 = (690, 0, marker_width, height)

# for animating movement of the lane markers
lane_marker_move_y1 = 0
lane_marker_move_y2 = 0

# players' starting coordinates
player1_x = lane1 + 50
player2_x = lane2 + 50
player1_y = 400
player2_y = 400

# frame settings
clock = pygame.time.Clock()
fps = 120

class PlayerVehicle(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    def move(self, x, y):
        self.rect.center = [x, y]
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

# create player 1's car
player1 = PlayerVehicle('images/redCar.png', player1_x, player1_y)

# create player 2's car
player2 = PlayerVehicle('images/yellowCar.png', player2_x, player2_y)

# Carregamento da imagem 'chegada'
chegada_image = pygame.image.load('images/finish.png')
chegada_image = pygame.transform.scale(chegada_image, (width, 100))

# game loop
running = True
gameover = False

# Defina as velocidades de forma aleatória para speed1 e speed2
speed1 = 0
speed2 = 0

# Variáveis de tempo e distância
tempo = 0
distancia1 = 0
distancia2 = 0
valor_final = 100
cont1 = 0
cont2 = 0
ticks = 0

time_interval = np.arange(0, TOTAL_TIME + 1/fps, 1/fps)

trans_cont_user = clt.tf(subprocess_data["ft_carro"][0], subprocess_data["ft_carro"][1])
trans_disc_user = clt.sample_system(trans_cont_user, 1/fps, method='zoh')
yout_user, xout_user = clt.step(trans_disc_user, time_interval)
speed_user = yout_user.tolist()

trans_cont_cpu = clt.tf(subprocess_data["ft_taxi"][0], subprocess_data["ft_taxi"][1])
trans_disc_cpu = clt.sample_system(trans_cont_cpu, 1/fps, method='zoh')
yout_cpu, xout_cpu = clt.step(trans_disc_cpu, time_interval)
speed_cpu = yout_cpu.tolist()

explodiu1 = False
explodiu2 = False

while running:
    
    clock.tick(fps)

    if speed1 <= subprocess_data["max_value"]:
        if distancia1 > valor_final:
            speed1 = 0
            cont1 = 1
        elif ticks < len(speed_user):
            speed1 = speed_user[ticks]
    else:
        pygame.mixer.Sound("songs/explosion.mp3").play()
        explodiu1 = True
        cont2 = True
        speed1 = 0
        player1 = PlayerVehicle('images/crash.png', player1_x, player1_y)
    
    if speed2 <= subprocess_data["max_value"]:
        if distancia2 > valor_final:
            speed2 = 0
            cont2 = 1
        elif ticks < len(speed_user):
            speed2 = speed_cpu[ticks]
    else:
        pygame.mixer.Sound("songs/explosion.mp3").play()
        explodiu2 = True
        cont1 = True
        speed2 = 0
        player2 = PlayerVehicle('images/crash.png', player2_x, player2_y)

    ticks += 1
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    # draw the grass
    screen.fill(green)
    
    # draw the road
    pygame.draw.rect(screen, gray, road1)
    pygame.draw.rect(screen, gray, road2)
    
    # draw the edge markers
    pygame.draw.rect(screen, red, left_edge_marker)
    pygame.draw.rect(screen, red, right_edge_marker)
    
    pygame.draw.rect(screen, yellow, left_edge_marker2)
    pygame.draw.rect(screen, yellow, right_edge_marker2)
    
    # draw the lane markers on road 1
    lane_marker_move_y1 += speed1 * 1
    if lane_marker_move_y1 >= marker_height * 2:
        lane_marker_move_y1 = 0
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (lane1, y + lane_marker_move_y1, marker_width, marker_height))
        
    
    # draw the lane markers on road 2
    lane_marker_move_y2 += speed2 * 1
    if lane_marker_move_y2 >= marker_height * 2:
        lane_marker_move_y2 = 0
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (lane2, y + lane_marker_move_y2, marker_width, marker_height))
    
    player1.move(player1_x, player1_y)
    player2.move(player2_x, player2_y)
    player1.draw(screen)
    player2.draw(screen)
    
    # Atualize o tempo
    tempo += 1 / fps

    # Calcule a distância percorrida para cada jogador
    distancia1 += speed1 * (1/fps)
    distancia2 += speed2 * (1/fps)
    
    # Desenhe a linha no meio da tela
    pygame.draw.line(screen, black, line_start, line_end, 2)
    
    # display the test
    pygame.draw.rect(screen, red, (115, 550, 180, 50))
    pygame.draw.rect(screen, black, (115, 550, 180, 50),2)
    font = pygame.font.Font(None, 30)
    text = font.render('Distância: {:.2f}'.format(distancia1), True, black)
    text_rect = text.get_rect()
    text_rect.center = (200, 590)
    screen.blit(text, text_rect)
    text3 = font.render('Velocidade: {:.2f}'.format(speed1), True, black)
    text_rect3 = text3.get_rect()
    text_rect3.center = (205, 570)
    screen.blit(text3, text_rect3)
    
    pygame.draw.rect(screen, yellow, (505, 550, 180, 50))
    pygame.draw.rect(screen, black, (505, 550, 180, 50),2)
    text2 = font.render('Distância: {:.2f}'.format(distancia2), True, black)
    text_rect2 = text2.get_rect()
    text_rect2.center = (590, 590)
    screen.blit(text2, text_rect2)
    text4 = font.render('Velocidade: {:.2f}'.format(speed2), True, black)
    text_rect4 = text4.get_rect()
    text_rect4.center = (595, 570)
    screen.blit(text4, text_rect4)
    
    # Título dos Jogadores
    pygame.draw.rect(screen, yellow, (402, 0, 398, 50))
    pygame.draw.rect(screen, black, (402, 0, 398, 50),2)
    font = pygame.font.Font(pygame.font.get_default_font(), 32)
    cpu_text = font.render("CPU", True, black)
    screen.blit(cpu_text, (560, 10))
    pygame.draw.rect(screen, red, (0, 0, 400, 50))
    pygame.draw.rect(screen, black, (0, 0, 400, 50),2)
    player_text = font.render("PLAYER 1", True, black)
    screen.blit(player_text, (125, 10))
    
    # Crie uma superfície de texto para exibir o tempo
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text_tempo = font.render('TEMPO\n  {:.2f} s'.format(tempo), True, white)
    text_rect_tempo = text_tempo.get_rect()
    text_rect_tempo.center = (width // 2, 190)
    pygame.draw.rect(screen, gray, (width // 2 - 50, 165, 100, 50))
    pygame.draw.rect(screen, black, (width // 2 - 50, 165, 100, 50),2)

    # Desenhe a superfície de texto na tela
    screen.blit(text_tempo, text_rect_tempo)
    
    pygame.display.update()
        
    if cont1 == 1 or cont2 == 1:
        gameover = True
            
    # display game over
    if gameover:
        if explodiu1 and explodiu2:
            vencedor = False
        else:
            vencedor = True 
        while vencedor:
            if cont1 == 1 and cont2 == 0:
                player1_y -= 2
                player1.move(player1_x, player1_y)
                
                font = pygame.font.Font(pygame.font.get_default_font(), 32)
                
                pygame.draw.rect(screen, gray, road1)
                pygame.draw.rect(screen, red, left_edge_marker)
                pygame.draw.rect(screen, red, right_edge_marker)
                for y in range(marker_height * -2, height, marker_height * 2):
                    pygame.draw.rect(screen, white, (lane1, y + lane_marker_move_y1, marker_width, marker_height))
                player1.draw(screen)
                
                pygame.draw.rect(screen, red, (0, 0, 400, 50))
                pygame.draw.rect(screen, black, (0, 0, 400, 50),2)
                player_text = font.render("PLAYER 1", True, black)
                screen.blit(player_text, (125, 10))
                
                if player1_y < -180:
                    vencedor = False
                       
            if cont1 == 1 and cont2 == 1:
                player1_y -= 2
                player1.move(player1_x, player1_y)
                
                font = pygame.font.Font(pygame.font.get_default_font(), 32)
                
                pygame.draw.rect(screen, gray, road1)
                pygame.draw.rect(screen, red, left_edge_marker)
                pygame.draw.rect(screen, red, right_edge_marker)
                for y in range(marker_height * -2, height, marker_height * 2):
                    pygame.draw.rect(screen, white, (lane1, y + lane_marker_move_y1, marker_width, marker_height))
                player1.draw(screen)
                
                player2_y -= 2
                player2.move(player2_x, player2_y)
                pygame.draw.rect(screen, gray, road2)
                pygame.draw.rect(screen, yellow, left_edge_marker2)
                pygame.draw.rect(screen, yellow, right_edge_marker2)
                for y in range(marker_height * -2, height, marker_height * 2):
                    pygame.draw.rect(screen, white, (lane2, y + lane_marker_move_y2, marker_width, marker_height))
                player2.draw(screen)
                
                pygame.draw.rect(screen, yellow, (402, 0, 398, 50))
                pygame.draw.rect(screen, black, (402, 0, 398, 50),2)
                cpu_text = font.render("CPU", True, black)
                screen.blit(cpu_text, (560, 10))
                
                pygame.draw.rect(screen, red, (0, 0, 400, 50))
                pygame.draw.rect(screen, black, (0, 0, 400, 50),2)
                player_text = font.render("PLAYER 1", True, black)
                screen.blit(player_text, (125, 10))
                
                if player2_y < -180:
                    vencedor = False
                
            if cont1 == 0 and cont2 == 1:
                player2_y -= 2
                player2.move(player2_x, player2_y)
                
                font = pygame.font.Font(pygame.font.get_default_font(), 32)
                
                pygame.draw.rect(screen, gray, road2)
                pygame.draw.rect(screen, yellow, left_edge_marker2)
                pygame.draw.rect(screen, yellow, right_edge_marker2)
                for y in range(marker_height * -2, height, marker_height * 2):
                    pygame.draw.rect(screen, white, (lane2, y + lane_marker_move_y2, marker_width, marker_height))
                player2.draw(screen)
                
                pygame.draw.rect(screen, yellow, (402, 0, 398, 50))
                pygame.draw.rect(screen, black, (402, 0, 398, 50),2)
                cpu_text = font.render("CPU", True, black)
                screen.blit(cpu_text, (560, 10))
                
                if player2_y < -180:
                    vencedor = False
                
            pygame.display.update()
        
        if cont1 == 1 and cont2 == 0:
            # Desenha a imagem 'chegada'
            pygame.mixer.music.pause()
            pygame.mixer.Sound("songs/win.mp3").play()
            screen.blit(chegada_image, (0, 50))
            font = pygame.font.Font(None, 32)
            pygame.draw.rect(screen, white, (0, 63, width, 70))
            text = font.render('                 Player 1 Venceu!\nAperte espaço para jogar de novo', True, black)
            text_rect = text.get_rect()
            text_rect.center = (width / 2, 100)
            screen.blit(text, text_rect)
            
        if cont1 == 1 and cont2 == 1 or (explodiu1 and explodiu2):
            # Desenha a imagem 'chegada'
            pygame.mixer.music.pause()
            pygame.mixer.Sound("songs/fail.mp3").play()
            screen.blit(chegada_image, (0, 50))
            font = pygame.font.Font(None, 32)
            pygame.draw.rect(screen, white, (0, 63, width, 70))
            text = font.render('                   Empatou!\nAperte espaço para jogar de novo', True, black)
            text_rect = text.get_rect()
            text_rect.center = (width / 2, 100)
            screen.blit(text, text_rect)
            
        if cont1 == 0 and cont2 == 1:
            # Desenha a imagem 'chegada'
            pygame.mixer.music.pause()
            pygame.mixer.Sound("songs/fail.mp3").play()
            screen.blit(chegada_image, (0, 50))
            font = pygame.font.Font(None, 32)
            pygame.draw.rect(screen, white, (0, 63, width, 70))
            text = font.render('                   CPU Venceu!\nAperte espaço para jogar de novo', True, black)
            text_rect = text.get_rect()
            text_rect.center = (width / 2, 100)
            screen.blit(text, text_rect)
            
    pygame.display.update()

    # wait for user's input to play again or exit
    while gameover:
        
        clock.tick(fps)
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                gameover = False
                running = False
                
            # get the user's input (y or n)
            if event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # reset the game
                    gameover = False
                    
                    # Fechar a janela antes de abrir o subprocesso
                    pygame.quit()

                    # Adicionar um pequeno atraso para garantir que a janela seja fechada antes de abrir o subprocesso
                    time.sleep(0.01)
                    
                    subprocess.run(["python", "forms.py"])  # Executar o script 'jogo.py'
                elif event.key == K_n:
                    # exit the loops
                    gameover = False
                    running = False
                    

pygame.quit()
