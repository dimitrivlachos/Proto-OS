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

# Initialize the dot color
r = 255
g = 255
b = 255

def constrain(value, min, max):
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value

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
    x_axis = round(joystick.get_axis(0), 2)
    y_axis = round(joystick.get_axis(1), 2)

    print("x_axis: " + str(x_axis))
    print("y_axis: " + str(y_axis))

    # Map the joystick axes to a dot position with 0 being the center
    x = int(constrain((x_axis + 1) * 8, 0, 14))
    y = int(constrain((y_axis + 1) * 8, 0, 14))

    x_actual = []
    y_actual = []

    x_actual.append(x)
    x_actual.append(x + 1)
    y_actual.append(y)
    y_actual.append(y + 1)

    # Clear the unicorn hat
    unicornhathd.clear()

    # Set the dots color
    for x in x_actual:
        for y in y_actual:
            unicornhathd.set_pixel(x, y, r, g, b)

    # Show the dot
    unicornhathd.show()

    # Wait 0.1 seconds
    time.sleep(0.1)