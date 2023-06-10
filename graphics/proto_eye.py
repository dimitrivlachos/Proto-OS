
import unicornhathd
from enum import Enum
from graphics.unicorn_graphics import Unicorn_Graphics

# Enum for the chirality of the eye
class Chirality(Enum):
    Left = 0
    Right = 1

class Proto_Eye():
    def __init__(self, chirality, x=4, y=4, r=255, g=255, b=255):
        self.chirality = chirality # Chirality of the eye
        self.x = x # X position of the eye
        self.y = y # Y position of the eye
        self.r = r # Red value of the eye
        self.g = g # Green value of the eye
        self.b = b # Blue value of the eye
        # Create 16 x 16 array of pixels
        self.pixels = [[(0, 0, 0) for x in range(16)] for y in range(16)]
        self.graphics = Unicorn_Graphics()

        self.draw_eye()

    def set_chirality(self, chirality):
        '''Sets the chirality of the eye'''
        self.chirality = chirality

    def update(self):
        '''Updates the eye to the Unicorn Hat HD'''
        # Cycle through the pixels and set them to the correct colour
        for x in range(16):
            for y in range(16):
                # Pulls the RGB values from the tuples in the array
                r, g, b = self.pixels[x][y]
                unicornhathd.set_pixel(x, y, r, g, b)

        # Show the eye
        unicornhathd.show()

    def set_position(self, x, y):
        '''Sets the position of the eye'''
        self.x = x
        self.y = y

    def set_colour(self, r, g, b):
        '''Sets the colour of the eye'''
        self.r = r
        self.g = g
        self.b = b

    def clear_pixels(self):
        '''Clears the pixels in the array'''
        for x in range(16):
            for y in range(16):
                self.pixels[x][y] = (0, 0, 0)

    def draw_eye(self):
        '''Draws the eye'''
        # Clear the pixels
        self.clear_pixels()

        # Draw the eye
        self.pixels = self.graphics.draw_circle(self.pixels, self.x, self.y, 4, self.r, self.g, self.b)

        # Draw the pupil
        self.pixels = self.graphics.draw_circle(self.x, self.y, 2, 0, 0, 0)

        # Draw the iris
        self.pixels = self.graphics.draw_circle(self.x, self.y, 1, 255, 255, 255)

        # Draw the eyelid
        self.pixels = self.graphics.draw_square(self.pixels, self.x - 4, self.y - 4, 8, 8, 0, 0, 0)

        self.update()