'''Control a 4x4 dot on a 16x16 pimoroni unicorn hd hat using a xbox 360 joystick'''\
# Path: graphics\unicorn_test.py
import unicornhathd
import time
import numpy as np
import pygame
import pygame.joystick
import sys

# Initialize pygame
pygame.init()
pygame.joystick.init()

# Initialize the joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Initialize the unicorn hat
unicornhathd.rotation(0)
unicornhathd.brightness(0.5)

# Initialize the dot position
x = 0
y = 0

# Initialize the dot color
r = 255
g = 255
b = 255

# Initialize the dot speed
speed = 1

# Initialize the dot size
size = 1

# Main loop
while True:
    # Get the events
    for event in pygame.event.get():
        # If the event is a quit event
        if event.type == pygame.QUIT:
            # Quit the program
            pygame.quit()
            sys.exit()

    # Get the joystick axes
    x_axis = joystick.get_axis(0)
    y_axis = joystick.get_axis(1)

    # Get the joystick buttons
    a_button = joystick.get_button(0)
    b_button = joystick.get_button(1)
    x_button = joystick.get_button(2)
    y_button = joystick.get_button(3)

    # Get the joystick hat
    hat = joystick.get_hat(0)

    # If the joystick is moved left
    if x_axis < -0.5:
        # Move the dot left
        x -= speed

    # If the joystick is moved right
    if x_axis > 0.5:
        # Move the dot right
        x += speed

    # If the joystick is moved up
    if y_axis < -0.5:
        # Move the dot up
        y -= speed

    # If the joystick is moved down
    if y_axis > 0.5:
        # Move the dot down
        y += speed

    # If the joystick hat is moved left
    if hat[0] == -1:
        # Move the dot left
        x -= speed

    # If the joystick hat is moved right
    if hat[0] == 1:
        # Move the dot right
        x += speed

    # If the joystick hat is moved up
    if hat[1] == -1:
        # Move the dot up
        y -= speed

    # If the joystick hat is moved down
    if hat[1] == 1:
        # Move the dot down
        y += speed

    # If the A button is pressed
    if a_button == 1:
        # Increase the dot size
        size += 1

    # If the B button is pressed
    if b_button == 1:
        # Decrease the dot size
        size -= 1

    # If the X button is pressed
    if x_button == 1:
        # Increase the dot speed
        speed += 1

    # If the Y button is pressed
    if y_button == 1:
        # Decrease the dot speed
        speed -= 1

    # If the dot is out of bounds
    if x < 0 or x > 15 or y < 0 or y > 15:
        # Reset the dot position
        x = 0
        y = 0

    # If the dot size is out of bounds
    if size < 1 or size > 4:
        # Reset the dot size
        size = 1

    # If the dot speed is out of bounds
    if speed < 1 or speed > 4:
        # Reset the dot speed
        speed = 1

    # If the dot color is out of bounds
    if r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or b > 255:
        # Reset the dot color
        r = 255
        g = 255
        b = 255

    # Clear the unicorn hat
    unicornhathd.clear()

    # Set the dot color
    unicornhathd.set_pixel(x, y, r, g, b)

    # Show the dot
    unicornhathd.show()

    # Wait 0.1 seconds
    time.sleep(0.1)

'''Control a 4x4 dot on a 16x16 pimoroni unicorn hd hat using a xbox 360 joystick'''\