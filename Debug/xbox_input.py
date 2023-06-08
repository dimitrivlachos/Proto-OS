import pygame

# Initialize pygame
pygame.init()

# Initialize the joystick module
pygame.joystick.init()

# Check if any joysticks/controllers are connected
if pygame.joystick.get_count() == 0:
    print("No joystick/controllers found.")
    pygame.quit()
    exit()

# Initialize the first joystick/controller
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Get the number of axes and buttons
num_axes = joystick.get_numaxes()
num_buttons = joystick.get_numbuttons()

# Main loop
while True:
    # Check for events
    for event in pygame.event.get():
        # Check if the event is a joystick/button axis motion
        if event.type == pygame.JOYAXISMOTION:
            # Get the axis ID and current value
            axis_id = event.axis
            axis_value = event.value
            print(f"Axis {axis_id}: {axis_value}")

        # Check if the event is a button press/release
        elif event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:
            # Get the button ID and state
            button_id = event.button
            button_state = "pressed" if event.type == pygame.JOYBUTTONDOWN else "released"
            print(f"Button {button_id}: {button_state}")

        # Check if the event is the user closing the window
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()
