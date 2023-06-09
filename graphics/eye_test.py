'''Control a 4x4 dot on a 16x16 pimoroni unicorn hd hat using a xbox 360 joystick'''\
# Path: graphics\unicorn_test.py
import unicornhathd
import pygame
import time
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

    # Map the joystick axes to a dot position with 0 being the center
    x = int((x_axis + 1) * 7)
    y = int((y_axis + 1) * 7)

    # Clear the unicorn hat
    unicornhathd.clear()

    # Draw the dot on the updated position
    for x in range(x, x + 2):
        for y in range(y, y + 2):
            unicornhathd.set_pixel(x, y, 255, 255, 255)  # White color

    # Show the dot
    unicornhathd.show()

    # Wait 0.1 seconds
    time.sleep(0.1)