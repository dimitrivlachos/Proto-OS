import numpy as np
import libraries.graphics.unicorn_graphics as ug
import pygame

# Initialize pygame
pygame.init()
pygame.joystick.init()

# Initialize the joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Initialize display
d = ug.Display()

# Draw a circle
sclera = ug.Circle(8, 8, 6, rgb=(255, 192, 203))

# Draw a quad for the eyebrow
eyebrow = ug.Polygon([(0, 0), (0, 15), (6, 15), (12, 0)], filled=True, rgb=(255, 0, 0))

# Set the initial display
d.set(sclera.pixels)
d.draw_on_top(eyebrow.pixels)

def map_range(value, low1, high1, low2, high2):
    return low2 + (high2 - low2) * (value - low1) / (high1 - low1)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYAXISMOTION:
            tilt = joystick.get_axis(0)  # Left and right motion
            open_close = joystick.get_axis(1)  # Up and down motion

            print("tilt: " + str(tilt))
            print("open_close: " + str(open_close))

            vertical_delta = map_range(open_close, -1, 1, -15, 15)

            eyerow_left = map_range(tilt, -1, 1, 0, 15 + vertical_delta)
            eyerow_right = map_range(tilt, -1, 1, 15 + vertical_delta, 0)

            eyebrow = ug.Polygon([(0, 0), (0, 15), (eyerow_left, 15), (eyerow_right, 0)], filled=True, rgb=(255, 0, 0))

            d.clear()
            d.set(sclera.pixels)
            d.draw_on_top(eyebrow.pixels)

# Quit pygame
pygame.quit()

