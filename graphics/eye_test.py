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
unicornhathd.brightness(0.6)

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
    x_axis = round(joystick.get_axis(0), 1)
    y_axis = round(joystick.get_axis(1), 1)

    print("x_axis: " + str(x_axis))
    print("y_axis: " + str(y_axis))

    # Map the joystick axes to a dot position with 0 being the center
    x_short = int(constrain((x_axis + 1) * 8, 1, 15))
    y_short = int(constrain((y_axis + 1) * 8, 1, 15))

    x_actual = []
    y_actual = []

    x_actual.append(x_short)
    x_actual.append(x_short - 1)
    y_actual.append(y_short)
    y_actual.append(y_short - 1)

    print("x: " + str(x_actual))
    print("y: " + str(y_actual))

    # Clear the unicorn hat
    unicornhathd.clear()

    # Set the dots color
    for x in range(0, 16):
        for y in range(0, 16):
            if x in x_actual and y in y_actual:
                unicornhathd.set_pixel(x, y, r, g, b)
            else:
                unicornhathd.set_pixel(x, y, 0, 0, 0)

    # Show the dot
    unicornhathd.show()

    # Wait 0.1 seconds
    time.sleep(0.1)