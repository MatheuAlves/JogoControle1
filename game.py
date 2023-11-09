import pygame
from pygame.locals import *
import random

pygame.init()

# create the window
width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Car Game')

# colors
gray = (100, 100, 100)
green = (76, 208, 56)
white = (255, 255, 255)
yellow = (255, 232, 0)

# road and marker sizes
road_width = 200
marker_width = 10
marker_height = 50

# lane coordinates
lane1 = 100
lane2 = 390

# road and edge markers
road1 = (0, 0, road_width, height)
road2 = (300, 0, road_width, height)
left_edge_marker = (0, 0, marker_width, height)
right_edge_marker = (200, 0, marker_width, height)

left_edge_marker2 = (290, 0, marker_width, height)
right_edge_marker2 = (490, 0, marker_width, height)

# for animating movement of the lane markers
lane_marker_move_y1 = 0
lane_marker_move_y2 = 0

# players' starting coordinates
player1_x = lane1 + 50
player2_x = lane2 + 50
player_y = 400

# frame settings
clock = pygame.time.Clock()
fps = 120

class PlayerVehicle(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

# sprite group for players
player_group = pygame.sprite.Group()

# create player 1's car
player1 = PlayerVehicle('images/car.png', player1_x, player_y)
player_group.add(player1)

# create player 2's car
player2 = PlayerVehicle('images/taxi.png', player2_x, player_y)
player_group.add(player2)

# game loop
running = True
gameover = False

# Defina as velocidades de forma aleatória para speed1 e speed2
speed1 = random.randint(1, 4)
speed2 = random.randint(6, 10)

# Variáveis de tempo e distância
tempo = 0
distancia1 = 0
distancia2 = 0
valor_final = 7
cont1 = 0
cont2 = 0

while running:
    
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    # draw the grass
    screen.fill(green)
    
    # draw the road
    pygame.draw.rect(screen, gray, road1)
    pygame.draw.rect(screen, gray, road2)
    
    # draw the edge markers
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)
    
    pygame.draw.rect(screen, yellow, left_edge_marker2)
    pygame.draw.rect(screen, yellow, right_edge_marker2)
    
    # draw the lane markers on road 1
    lane_marker_move_y1 += speed1 * 1
    if lane_marker_move_y1 >= marker_height * 2:
        lane_marker_move_y1 = 0
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (lane1, y + lane_marker_move_y1, marker_width, marker_height))
        
    # draw the lane markers on road 2
    lane_marker_move_y2 += speed2 
    if lane_marker_move_y2 >= marker_height * 2:
        lane_marker_move_y2 = 0
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (lane2, y + lane_marker_move_y2, marker_width, marker_height))
    
    # draw the players' cars
    player_group.draw(screen)
    
    # Atualize o tempo
    tempo += 1 / fps

    # Calcule a distância percorrida para cada jogador
    distancia1 = speed1 * tempo
    distancia2 = speed2 * tempo
        
    # display the test
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Distância 1: {:.2f}'.format(distancia1), True, white)
    text_rect = text.get_rect()
    text_rect.center = (55, 380)
    screen.blit(text, text_rect)
    
    text2 = font.render('Distância 2: {:.2f}'.format(distancia2), True, white)
    text_rect2 = text2.get_rect()
    text_rect2.center = (350, 380)
    screen.blit(text2, text_rect2)
    
    # Crie uma superfície de texto para exibir o tempo
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text_tempo = font.render('Tempo: {:.2f} s'.format(tempo), True, white)
    text_rect_tempo = text_tempo.get_rect()
    text_rect_tempo.center = (width // 2, 20)

    # Desenhe a superfície de texto na tela
    screen.blit(text_tempo, text_rect_tempo)

    
    pygame.display.update()
    
    if distancia1 > valor_final:
        speed1 = 0
        cont1 = 1
    if distancia2 > valor_final:
        speed2 = 0
        cont2 = 1
        
    if cont1 == 1 and cont2 == 1:
        gameover = True
            
    # display game over
    if gameover:
        pygame.draw.rect(screen, gray, (0, 50, width, 100))
        
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Game over. Play again? (Enter Y or N)', True, white)
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
                if event.key == K_y:
                    # reset the game
                    gameover = False
                    tempo = 0
                    distancia1 = 0
                    distancia2 = 0
                    cont1 = 0
                    cont2 = 0
                    speed1 = random.randint(1, 4)
                    speed2 = random.randint(6, 10)
                    player1.rect.center = [player1_x, player_y]
                    player2.rect.center = [player2_x, player_y]
                elif event.key == K_n:
                    # exit the loops
                    gameover = False
                    running = False

pygame.quit()
