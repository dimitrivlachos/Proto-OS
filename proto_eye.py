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

# Initial position of the eyebrow
eyebrow_position = 0

# Set the initial display
d.set(sclera.pixels)
d.draw_on_top(eyebrow.pixels)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYAXISMOTION:
            d.clear()
            # Check joystick axes for tilt and open/close
            tilt = joystick.get_axis(0)  # Left and right motion
            open_close = joystick.get_axis(1)  # Up and down motion

            # Adjust the position of the eyebrow based on joystick input
            eyebrow_position += tilt * 2  # Adjust the factor as needed
            eyebrow_position = max(0, min(15, eyebrow_position))  # Ensure position is within bounds

            # Set the new position of the eyebrow
            eyebrow.vertices = [(0, eyebrow_position), (0, 15), (6, 15), (12, eyebrow_position)]
            eyebrow.draw_filled()

            # Update the display
            d.set(sclera.pixels)
            d.draw_on_top(eyebrow.pixels)

    pygame.display.flip()

# Quit pygame
pygame.quit()