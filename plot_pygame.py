import numpy as np
import matplotlib
matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg

import pylab
import pygame
from pygame.locals import *

x = np.arange(0, 1.0, 0.01)
y1 = np.sin(2*np.pi*x)

fig = pylab.figure(figsize=[4, 4], dpi=100)
ax = fig.gca()
ax.plot(x, y1, color='blue')

canvas = agg.FigureCanvasAgg(fig)
canvas.draw()
renderer = canvas.get_renderer()
raw_data = renderer.tostring_argb()

pygame.init()

window = pygame.display.set_mode((600, 400), DOUBLEBUF)
screen = pygame.display.get_surface()

size = canvas.get_width_height()

# Convert ARGB to RGBA
raw_data_rgba = bytearray(size[0] * size[1] * 4)
raw_data_rgba[0::4] = raw_data[1::4]  # Red channel
raw_data_rgba[1::4] = raw_data[2::4]  # Green channel
raw_data_rgba[2::4] = raw_data[3::4]  # Blue channel
raw_data_rgba[3::4] = raw_data[0::4]  # Alpha channel

surf = pygame.image.fromstring(bytes(raw_data_rgba), size, "RGBA")
screen.blit(surf, (0, 0))
pygame.display.flip()

crashed = False
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True