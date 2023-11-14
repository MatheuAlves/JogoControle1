import numpy as np
import matplotlib
matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg

import pylab
import pygame
import sys
from pygame.locals import *
import control.matlab as clt
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

LOWER_LIMIT = 0.0
UPPER_LIMIT = 10.0

SAMPLE_TIME = 0.1
TOTAL_TIME = 20.0

STEP_VALUE = 1

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
            font_surface = font.render(self.text, True, BLACK)
            font_rect = font_surface.get_rect(center=self.rect.center)
            screen.blit(font_surface, font_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    

def update_data():
    # Function to update data
    global yout
    global xout
    global upper_text
    global lower_text
    choice = random.choice(['1', '2'])

    if choice == '1':
        rd_num_c1 = round(random.uniform(LOWER_LIMIT, UPPER_LIMIT), 3)
        num = np.array([rd_num_c1])
        rd_den_c1 = round(random.uniform(LOWER_LIMIT, UPPER_LIMIT), 3)
        den = np.array([1, rd_den_c1])

        upper_text = f"{rd_num_c1}"
        lower_text = f"s + {rd_den_c1}"
    elif choice == '2':
        rd_num_c1 = round(random.uniform(LOWER_LIMIT, UPPER_LIMIT), 3)
        rd_num_c2 = round(random.uniform(LOWER_LIMIT, UPPER_LIMIT), 3)
        num = np.array([rd_num_c1, rd_num_c2])
        rd_den_c1 = round(random.uniform(LOWER_LIMIT, UPPER_LIMIT), 3)
        rd_den_c2 = round(random.uniform(LOWER_LIMIT, UPPER_LIMIT), 3)
        den = np.array([1, rd_den_c1, rd_den_c2])

        upper_text = f"{rd_num_c1}s + {rd_num_c2}"
        lower_text = f"s^2 + {rd_den_c1}s + {rd_den_c2}"


    trans_cont = STEP_VALUE * clt.tf(num, den)
    #trans_disc = clt.sample_system(trans_cont, SAMPLE_TIME, method='zoh')
    #time_interval = np.arange(0, TOTAL_TIME + SAMPLE_TIME, SAMPLE_TIME)
    yout, xout = clt.step(trans_cont, time_interval)
    #yout, xout = clt.step(trans_disc, time_interval)

choice = random.choice(['1', '2'])

if choice == '1':
    rd_num_c1 = round(random.uniform(LOWER_LIMIT, UPPER_LIMIT), 3)
    num = np.array([rd_num_c1])
    rd_den_c1 = round(random.uniform(LOWER_LIMIT, UPPER_LIMIT), 3)
    den = np.array([1, rd_den_c1])

    upper_text = f"{rd_num_c1}"
    lower_text = f"s + {rd_den_c1}"
elif choice == '2':
    rd_num_c1 = round(random.uniform(LOWER_LIMIT, UPPER_LIMIT), 3)
    rd_num_c2 = round(random.uniform(LOWER_LIMIT, UPPER_LIMIT), 3)
    num = np.array([rd_num_c1, rd_num_c2])
    rd_den_c1 = round(random.uniform(LOWER_LIMIT, UPPER_LIMIT), 3)
    rd_den_c2 = round(random.uniform(LOWER_LIMIT, UPPER_LIMIT), 3)
    den = np.array([1, rd_den_c1, rd_den_c2])

    upper_text = f"{rd_num_c1}s + {rd_num_c2}"
    lower_text = f"s^2 + {rd_den_c1}s + {rd_den_c2}"

trans_cont = STEP_VALUE * clt.tf(num, den)
#trans_disc = clt.sample_system(trans_cont, SAMPLE_TIME, method='zoh')
time_interval = np.arange(0, TOTAL_TIME + SAMPLE_TIME, SAMPLE_TIME)
yout, xout = clt.step(trans_cont, time_interval)
#yout, xout = clt.step(trans_disc, time_interval)

fig = pylab.figure(figsize=[4, 4], dpi=100)
ax = fig.gca()
ax.plot(xout, yout)  # Use stem instead of plot
#ax.stem(xout, yout, linefmt='b-', markerfmt='bo', basefmt='r-')  # Use stem instead of plot
ax.set_title('Resposta ao Degrau')  # Set the title for the stem plot
ax.set_xlabel('Tempo')  # Set the label for the x-axis
ax.set_ylabel('Velocidade')  # Set the label for the y-axis

# Adjust the spacing around the subplots
fig.subplots_adjust(left=0.20, right=0.95, bottom=0.11, top=0.9)

canvas = agg.FigureCanvasAgg(fig)
canvas.draw()
renderer = canvas.get_renderer()
raw_data = renderer.tostring_argb()

pygame.init()
# Set up fonts
font = pygame.font.Font(None, 24)

window = pygame.display.set_mode((600, 400), DOUBLEBUF)
screen = pygame.display.get_surface()

size = canvas.get_width_height()

# Convert ARGB to RGBA
raw_data_rgba = bytearray(size[0] * size[1] * 4)
raw_data_rgba[0::4] = raw_data[1::4]  # Red channel
raw_data_rgba[1::4] = raw_data[2::4]  # Green channel
raw_data_rgba[2::4] = raw_data[3::4]  # Blue channel
raw_data_rgba[3::4] = raw_data[0::4]  # Alpha channel

graph = pygame.image.fromstring(bytes(raw_data_rgba), size, "RGBA")
button_graph = Button(430, 350, 150, 30, RED, "Nova Função", action=lambda: update_data())

text_step_value_surface = font.render(f"Valor Degrau: {STEP_VALUE}", True, BLACK)

text_num_surface = font.render(upper_text, True, BLACK)
text_den_surface = font.render(lower_text, True, BLACK)

text_step_value_pos = (430, 50)

text_num_pos = (430, 100 - text_num_surface.get_height() - 5)
text_den_pos = (430, 100 + text_den_surface.get_height() - 10)

line_width = max(text_num_surface.get_width(), text_den_surface.get_width())
line_start = (430, 100)
line_end = (430 + line_width, 100)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_graph.is_clicked(pygame.mouse.get_pos()):
                # If the mouse click is within the button area, update data
                button_graph.action()
                # Redraw the graph
                ax.clear()
                ax.plot(xout, yout)  # Use stem instead of plot
                #ax.stem(xout, yout, linefmt='b-', markerfmt='bo', basefmt='r-')  # Use stem instead of plot
                ax.set_title('Resposta ao Degrau')  # Set the title for the stem plot
                ax.set_xlabel('Tempo')  # Set the label for the x-axis
                ax.set_ylabel('Velocidade')  # Set the label for the y-axis

                # Adjust the spacing around the subplots
                fig.subplots_adjust(left=0.20, right=0.95, bottom=0.11, top=0.9)

                # Redraw the canvas
                canvas.draw()
                renderer = canvas.get_renderer()
                raw_data = renderer.tostring_argb()
                raw_data_rgba = bytearray(size[0] * size[1] * 4)
                raw_data_rgba[0::4] = raw_data[1::4]
                raw_data_rgba[1::4] = raw_data[2::4]
                raw_data_rgba[2::4] = raw_data[3::4]
                raw_data_rgba[3::4] = raw_data[0::4]
                graph = pygame.image.fromstring(bytes(raw_data_rgba), size, "RGBA")

                text_num_surface = font.render(upper_text, True, BLACK)
                text_den_surface = font.render(lower_text, True, BLACK)

                line_width = max(text_num_surface.get_width(), text_den_surface.get_width())
                line_start = (430, 100)
                line_end = (430 + line_width, 100)



    # Fill the screen with the background color
    screen.fill(WHITE)

    # Draw the graph on the filled screen
    screen.blit(graph, (0, 0))
    screen.blit(text_step_value_surface, text_step_value_pos)
    screen.blit(text_num_surface, text_num_pos)
    screen.blit(text_den_surface, text_den_pos)
    pygame.draw.line(screen, BLACK, line_start,
                     line_end, 2)
    button_graph.draw(screen, BLACK)
    
    pygame.display.flip()

pygame.quit()