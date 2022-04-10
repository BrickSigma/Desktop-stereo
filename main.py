from analyser import analyse
from recorder import record

import win32api
import win32con
import win32gui

import pygame, sys, os
from pygame.locals import *
import numpy as np

from threading import Thread

x = 0
y = 0

# This provides support for screen sharing
# Note: Does not work yet
# TO-DO: Enable it to detect multiple shared screens and draw to them
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"

WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)

# Colors
BLACK = 0, 0, 0
PURPLE = (26, 1, 71)
PINK = (232, 0, 101)

# This is used for making the window transparent
# Create layered window
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*BLACK), 0, win32con.LWA_COLORKEY)


# The data array contains the amplitudes of each frequency range
data = np.array([0, 0, 0, 0, 0, 0, 0], np.float64)
running = True  # Used to stop the threaded function when the user closes the program

# Canvas for the stereo
sWIDTH, sHEIGHT = 254, 212
stereo = pygame.Surface((254, 212))
BAR = pygame.image.load("bar.png")

# A list of pygame.Rect objects for drawing the stereo analyser
base = [pygame.Rect(x, sHEIGHT-7, 25, 7) for x in range(0, 229, 38)]
dots = [pygame.Rect(x, sHEIGHT-7, 7, 7) for x in range(28, 256, 38)]
bars = [pygame.Rect(x, sHEIGHT-212, 25, 200) for x in range(0, 229, 38)]


def test():
    """
    Continuously loop over the record and analyse function.
    This will overwrite the data variable to produce real-time results
    """

    global data
    while running:
        data = analyse(record())


thread = Thread(target=test)


def rect_surface(rect):
    """
    Used for creating a fade effect for the bars.
    NOTE: Does not work yet.
    TO-DO: Create fade effect
    """
    surf = pygame.Surface((rect.width, 20))
    surf.fill(BLACK)
    surf.set_alpha(255)
    return surf

def main():
    global running

    thread.start()
    run = True
    while run:

        # Basic pygame.event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        """
        Draw the individual bars to the stereo surface
        """
        stereo.fill(BLACK)
        for b in base:
            pygame.draw.rect(stereo, PINK, b)
        for d in dots:
            pygame.draw.rect(stereo, PURPLE, d)
        for i in range(len(data)):
            stereo.blit(pygame.transform.scale(BAR, (25, 200)), (bars[i].x, bars[i].y))
            bars[i].height = 200 - (200 * data[i]) - 20  # Multiply the bar height by the amplitude percentage to generate varying heights.
            pygame.draw.rect(stereo, BLACK, bars[i])
            stereo.blit(rect_surface(bars[i]), (bars[i].x, bars[i].y+200-(200 * data[i])-20))

        WIN.fill(BLACK)
        WIN.blit(stereo, (WIDTH//2 - sWIDTH//2, HEIGHT//2 + sHEIGHT//2-20))
        
        pygame.display.update()

if __name__=='__main__':
    main()