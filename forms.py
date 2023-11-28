import pygame
import sys
import subprocess
import time

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab
from pygame.locals import *
import control.matlab as clt
import random

LOWER_LIMIT = 1.0
UPPER_LIMIT = 15.0
TOTAL_TIME = 20.0
STEP_VALUE = 10
LIMIT = 6
MAX_VALUE = STEP_VALUE * LIMIT

# Cores
white = (255, 255, 255)
black = (0, 0, 0)
grey = (220,220,220)
red = (255, 0, 0)

time_interval = np.arange(0, TOTAL_TIME + 0.001, 0.001)

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

def update_data():
    # Function to update data
    global yout
    global xout
    global tf_original
    global tf_player

    option = "P" if selected_option["P"] else ""
    option += "I" if selected_option["I"] else ""
    option += "D" if selected_option["D"] else ""

    match option:
        case "P":
            gain = clt.tf([kp], [1])
            new_tf_cont = gain * tf_original
            yout, xout = clt.step(new_tf_cont, time_interval)
            tf_player = new_tf_cont
        case "I":
            gain = clt.tf([ki], [1, 0])
            new_tf_cont = gain * tf_original
            yout, xout = clt.step(new_tf_cont, time_interval)
            tf_player = new_tf_cont
        case "PI":
            gain = (clt.tf([kp], [1]) + clt.tf([ki], [1, 0]))
            new_tf_cont = gain * tf_original
            yout, xout = clt.step(new_tf_cont, time_interval)
            tf_player = new_tf_cont
        case "PD":
            gain = (clt.tf([kp], [1]) + clt.tf([kd, 0], [1]))
            new_tf_cont = gain * tf_original
            yout, xout = clt.step(new_tf_cont, time_interval)
            tf_player = new_tf_cont
        case "PID":
            gain = (clt.tf([kp], [1]) + clt.tf([ki], [1, 0]) + clt.tf([kd, 0], [1]))
            new_tf_cont = gain * tf_original
            yout, xout = clt.step(new_tf_cont, time_interval)
            tf_player = new_tf_cont
        case "":
            yout, xout = clt.step(tf_original, time_interval)
            tf_player = tf_original
        

choice = random.choice(['1', '2'])

if choice == '1':
    rd_num_c1 = round(random.uniform(LOWER_LIMIT, UPPER_LIMIT), 1)
    num = np.array([rd_num_c1])
    rd_den_c1 = round(random.uniform(LOWER_LIMIT, UPPER_LIMIT), 1)
    den = np.array([1, rd_den_c1])

    upper_text = f"{rd_num_c1}"
    lower_text = f"s + {rd_den_c1}"

elif choice == '2':
    rd_num_c1 = round(random.uniform(LOWER_LIMIT, UPPER_LIMIT), 1)
    num = np.array([1, rd_num_c1])
    rd_den_c1 = round(random.uniform(LOWER_LIMIT, UPPER_LIMIT), 1)
    rd_den_c2 = round(random.uniform(LOWER_LIMIT, UPPER_LIMIT), 1)
    den = np.array([1, rd_den_c1, rd_den_c2])

    upper_text = f"s + {rd_num_c1}"
    lower_text = f"s^2 + {rd_den_c1}s + {rd_den_c2}"

tf_original = STEP_VALUE * clt.tf(num, den)
tf_player = tf_original
yout, xout = clt.step(tf_original, time_interval)
max_line, max_out = clt.step(MAX_VALUE, time_interval)

fig = pylab.figure(figsize=[4, 4], dpi=100)
ax = fig.gca()
ax.plot(xout, yout, max_out, max_line)  # Use stem instead of plot 
ax.set_title('Resposta ao Degrau de Amplitude 10')  # Set the title for the stem plot
ax.set_xlabel('Tempo')  # Set the label for the x-axis
ax.set_ylabel('Velocidade')  # Set the label for the y-axis
ax.legend(['Reposta Degrau', 'Velocidade Limite'])
# Adjust the spacing around the subplots
fig.subplots_adjust(left=0.20, right=0.97, bottom=0.11, top=0.9)

canvas = agg.FigureCanvasAgg(fig)
canvas.draw()
renderer = canvas.get_renderer()
raw_data = renderer.tostring_argb()

size = canvas.get_width_height()

# Convert ARGB to RGBA
raw_data_rgba = bytearray(size[0] * size[1] * 4)
raw_data_rgba[0::4] = raw_data[1::4]  # Red channel
raw_data_rgba[1::4] = raw_data[2::4]  # Green channel
raw_data_rgba[2::4] = raw_data[3::4]  # Blue channel
raw_data_rgba[3::4] = raw_data[0::4]  # Alpha channel

graph = pygame.image.fromstring(bytes(raw_data_rgba), size, "RGBA")

# Iniciar o Pygame
pygame.init()

# Música de fundo
pygame.mixer.music.load("songs/formSound.mp3")
pygame.mixer.music.play(-1)

# Configurações da tela do Pygame
width = 800
height = 600
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Pygame Form")

# Fonte
font = pygame.font.Font(None, 36)

# Função para desenhar botão de rádio
def draw_radio_button(surface, x, y, text, selected):
    radio_button_rect = pygame.Rect(x, y, 20, 20)
    pygame.draw.rect(surface, black, radio_button_rect, 2)

    if selected:
        pygame.draw.circle(surface, black, (x + 10, y + 10), 8)

    text_surface = font.render(text, True, black)
    surface.blit(text_surface, (x + 30, y))

button_graph = Button(532, 125, 200, 30, red, "Gerar Resposta", action=lambda: update_data())

text_num_surface = font.render(f"{STEP_VALUE}({upper_text})", True, black)
text_den_surface = font.render(lower_text, True, black)

y_trans = 90

text_num_pos = (530, y_trans - text_num_surface.get_height() - 5)
text_den_pos = (530, y_trans + text_den_surface.get_height() - 15)

line_width = max(text_num_surface.get_width(), text_den_surface.get_width())
line_start = (530, y_trans)
line_end = (530 + line_width, y_trans)

# Texto
text_start = font.render('Aperte espaço para iniciar o jogo', True, grey)
text_start_rect = text_start.get_rect(center=(width / 2, 575))

text_start1 = font.render('Player 1', True, black)
text_start_rect1 = text_start1.get_rect(center=(width / 2, 25))

# Loop principal do Pygame
running = True

selected_option = {
    "P" : False,
    "I" : False,
    "D" : False
}

# Number variables
kp = 0.0
ki = 0.0
kd = 0.0

# Icon variables
icon_size = 30
icon_spacing = 20
icon_spacing_x = 150
icon_spacing_y = 270

icons_options = [
    {
        "group" : 1,
        "icons" : [
            {"rect": pygame.Rect(icon_spacing_x, icon_spacing_y, icon_size, icon_size), "text": "+1"},
            {"rect": pygame.Rect(icon_spacing_x + icon_size + icon_spacing, icon_spacing_y, icon_size, icon_size), "text": "-1"},
            {"rect": pygame.Rect(icon_spacing_x + 2 * (icon_size + icon_spacing), icon_spacing_y, icon_size, icon_size), "text": "+0.1"},
            {"rect": pygame.Rect(icon_spacing_x + 3 * (icon_size + icon_spacing) + icon_spacing/2, icon_spacing_y, icon_size, icon_size), "text": "-0.1"}
        ]
    },
    {   
        "group" : 2,
        "icons" : [
            {"rect": pygame.Rect(icon_spacing_x, icon_spacing_y + 50, icon_size, icon_size), "text": "+0.1"},
            {"rect": pygame.Rect(icon_spacing_x + icon_size + icon_spacing, icon_spacing_y + 50, icon_size, icon_size), "text": "-0.1"},
            {"rect": pygame.Rect(icon_spacing_x + 2 * (icon_size + icon_spacing), icon_spacing_y + 50, icon_size, icon_size), "text": "+0.01"},
            {"rect": pygame.Rect(icon_spacing_x + 3 * (icon_size + icon_spacing) + icon_spacing/2, icon_spacing_y + 50, icon_size, icon_size), "text": "-0.01"}
        ]
    },
    {   
        "group" : 3,
        "icons" : [
            {"rect": pygame.Rect(icon_spacing_x, icon_spacing_y + 100, icon_size, icon_size), "text": "+1"},
            {"rect": pygame.Rect(icon_spacing_x + icon_size + icon_spacing, icon_spacing_y + 100, icon_size, icon_size), "text": "-1"},
            {"rect": pygame.Rect(icon_spacing_x + 2 * (icon_size + icon_spacing), icon_spacing_y + 100, icon_size, icon_size), "text": "+0.1"},
            {"rect": pygame.Rect(icon_spacing_x + 3 * (icon_size + icon_spacing) + icon_spacing/2, icon_spacing_y + 100, icon_size, icon_size), "text": "-0.1"}
        ]
    }
]

def handle_icon_press(mouse_pos, icons_list):
    for icon in icons_list:
        if icon["rect"].collidepoint(mouse_pos):
            return icon["text"]
    return None

text_kp_surface = font.render("Kp = {:.1f}".format(kp), True, black)
text_ki_surface = font.render("Ki  = {:.2f}".format(ki), True, black)
text_kd_surface = font.render("Kd = {:.1f}".format(kd), True, black)

text_kp_pos = (25, 275)
text_ki_pos = (25, 325)
text_kd_pos = (25, 375)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 25 <= mouse_x <= 225 and 75 <= mouse_y <= 105:
                if(selected_option["P"]):
                    pygame.mixer.Sound("songs/wrong.mp3").play()
                    selected_option["P"] = False
                    if(selected_option["D"]):
                        pygame.mixer.Sound("songs/wrong.mp3").play()
                        selected_option["D"] = False
                else:
                    pygame.mixer.Sound("songs/check.mp3").play()
                    selected_option["P"] = True
                    
            elif 25 <= mouse_x <= 225 and 125 <= mouse_y <= 155:
                if(selected_option["I"]):
                    pygame.mixer.Sound("songs/wrong.mp3").play()
                    selected_option["I"] = False
                else:
                    pygame.mixer.Sound("songs/check.mp3").play()
                    selected_option["I"] = True
            elif 25 <= mouse_x <= 225 and 175 <= mouse_y <= 205:
                if(selected_option["D"]):
                    pygame.mixer.Sound("songs/wrong.mp3").play()
                    selected_option["D"] = False
                    
                else:
                    pygame.mixer.Sound("songs/check.mp3").play()
                    selected_option["D"] = True
                    selected_option["P"] = True

            if button_graph.is_clicked(pygame.mouse.get_pos()):
                # If the mouse click is within the button area, update data
                button_graph.action()

                # Redraw the graph
                ax.clear()
                ax.plot(xout, yout, max_out, max_line)  # Use stem instead of plot
                #ax.stem(xout, yout, linefmt='b-', markerfmt='bo', basefmt='r-')  # Use stem instead of plot
                ax.set_title('Resposta ao Degrau de Amplitude 10')  # Set the title for the stem plot
                ax.set_xlabel('Tempo')  # Set the label for the x-axis
                ax.set_ylabel('Velocidade')  # Set the label for the y-axis
                ax.legend(['Reposta Degrau', 'Velocidade Limite'])

                # Adjust the spacing around the subplots
                fig.subplots_adjust(left=0.20, right=0.97, bottom=0.11, top=0.9)

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

                text_num_surface = font.render(f"{STEP_VALUE}({upper_text})", True, black)
                text_den_surface = font.render(lower_text, True, black)

                line_width = max(text_num_surface.get_width(), text_den_surface.get_width())
                line_start = (530, y_trans)
                line_end = (530 + line_width, y_trans)
                
            # Função para limitar o valor entre 0 e 5 para P ou D
            def limit_value_PD(value):
                return max(0, min(value, 5))
            # Função para limitar o valor entre 0 e 1 para I
            def limit_value_I(value):
                return max(0, min(value, 1))

            for icons in icons_options:
                pressed_icon = handle_icon_press(event.pos, icons["icons"])
                if pressed_icon is not None:
                    if pressed_icon == "+1":
                        match icons["group"]:
                            case 1:
                                if selected_option["P"]:
                                    pygame.mixer.Sound("songs/check.mp3").play()
                                    kp += 1
                                    kp = limit_value_PD(kp)
                                    text_kp_surface = font.render("Kp = {:.1f}".format(kp), True, black)
                            case 3:
                                if selected_option["D"]:
                                    pygame.mixer.Sound("songs/check.mp3").play()
                                    kd += 1
                                    kd = limit_value_PD(kd)
                                    text_kd_surface = font.render("Kd = {:.1f}".format(kd), True, black)
                    elif pressed_icon == "-1":
                        match icons["group"]:
                            case 1:
                                if selected_option["P"]:
                                    pygame.mixer.Sound("songs/wrong.mp3").play()
                                    kp += -1
                                    kp = limit_value_PD(kp)
                                    text_kp_surface = font.render("Kp = {:.1f}".format(kp), True, black)
                            case 3:
                                if selected_option["D"]:
                                    pygame.mixer.Sound("songs/wrong.mp3").play()
                                    kd += -1
                                    kd = limit_value_PD(kd)
                                    text_kd_surface = font.render("Kd = {:.1f}".format(kd), True, black)
                    elif pressed_icon == "+0.1":
                        match icons["group"]:
                            case 1:
                                if selected_option["P"]:
                                    pygame.mixer.Sound("songs/check.mp3").play()
                                    kp += 0.1
                                    kp = limit_value_PD(kp)
                                    text_kp_surface = font.render("Kp = {:.1f}".format(kp), True, black)
                            case 2:
                                if selected_option["I"]:
                                    pygame.mixer.Sound("songs/check.mp3").play()
                                    ki += 0.1
                                    ki = limit_value_I(ki)
                                    text_ki_surface = font.render("Ki  = {:.2f}".format(ki), True, black)
                            case 3:
                                if selected_option["D"]:
                                    pygame.mixer.Sound("songs/check.mp3").play()
                                    kd += 0.1
                                    kd = limit_value_PD(kd)
                                    text_kd_surface = font.render("Kd = {:.1f}".format(kd), True, black)
                    elif pressed_icon == "-0.1":
                        match icons["group"]:
                            case 1:
                                if selected_option["P"]:
                                    pygame.mixer.Sound("songs/wrong.mp3").play()
                                    kp += -0.1
                                    kp = limit_value_PD(kp)
                                    text_kp_surface = font.render("Kp = {:.1f}".format(kp), True, black)
                            case 2:
                                if selected_option["I"]:
                                    pygame.mixer.Sound("songs/wrong.mp3").play()
                                    ki += -0.1
                                    ki = limit_value_I(ki)
                                    text_ki_surface = font.render("Ki  = {:.2f}".format(ki), True, black)
                            case 3:
                                if selected_option["D"]:
                                    pygame.mixer.Sound("songs/wrong.mp3").play()
                                    kd += -0.1
                                    kd = limit_value_PD(kd)
                                    text_kd_surface = font.render("Kd = {:.1f}".format(kd), True, black)
                    elif pressed_icon == "+0.01":
                        match icons["group"]:
                            case 2:
                                if selected_option["I"]:
                                    pygame.mixer.Sound("songs/wrong.mp3").play()
                                    ki += 0.01
                                    ki = limit_value_I(ki)
                                    text_ki_surface = font.render("Ki  = {:.2f}".format(ki), True, black)
                    elif pressed_icon == "-0.01":
                        match icons["group"]:
                            case 2:
                                if selected_option["I"]:
                                    pygame.mixer.Sound("songs/wrong.mp3").play()
                                    ki += -0.01
                                    ki = limit_value_I(ki)
                                    text_ki_surface = font.render("Ki  = {:.2f}".format(ki), True, black)
                    break
                    
    # Verificar se a tecla de espaço foi pressionada
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        pygame.mixer.Sound("songs/confirm.mp3").play()
        time.sleep(0.5)
        running = False
        # Fechar a janela antes de abrir o subprocesso
        pygame.quit()

        data1 = clt.tfdata(tf_original)
        data2 = clt.tfdata(tf_player)
        # Transformation to lists
        list_data1 = [[float(item) for sublist in nested_list for array_item in sublist for item in array_item] for nested_list in data1]
        list_data2 = [[float(item) for sublist in nested_list for array_item in sublist for item in array_item] for nested_list in data2]

        subprocess_data = {
            "ft_original" : list_data1,
            "ft_player" : list_data2,
            "max_value" : (MAX_VALUE)
        }

        # Adicionar um pequeno atraso para ga rantir que a janela seja fechada antes de abrir o subprocesso
        time.sleep(0.01)
        subprocess.run(["python", "game.py", str(subprocess_data)])  # Executar o script 'jogo.py'
        # Finalizar o Pygame
        pygame.quit()
        sys.exit()


    # Limpar a tela
    screen.fill(white)

    screen.blit(graph, (400, 150))
    button_graph.draw(screen, black)
    screen.blit(text_num_surface, text_num_pos)
    screen.blit(text_den_surface, text_den_pos)
    pygame.draw.line(screen, black, line_start, line_end, 2)

    # Desenhar botões de rádio
    draw_radio_button(screen, 25, 75, "Proporcional", selected_option["P"])
    draw_radio_button(screen, 25, 125, "Integral", selected_option["I"])
    draw_radio_button(screen, 25, 175, "Derivativo", selected_option["D"])

    screen.blit(text_kp_surface, text_kp_pos)
    screen.blit(text_ki_surface, text_ki_pos)
    screen.blit(text_kd_surface, text_kd_pos)

    for group in icons_options:
        for icon in group["icons"]:
            text = font.render(icon["text"], True, black)
            text_rect = text.get_rect(center=icon["rect"].center)
            screen.blit(text, text_rect)

    # Desenhar retângulo preto de fundo
    pygame.draw.rect(screen, black, (0, 550, width , 50))
    pygame.draw.rect(screen, red, (0, 0, width , 50))
    # Desenhar o texto no centro da tela
    screen.blit(text_start, text_start_rect)
    screen.blit(text_start1, text_start_rect1)

    # Atualizar a tela
    pygame.display.flip()

# Finalizar o Pygame
pygame.quit()
sys.exit()
