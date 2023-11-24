import unicornhathd
import numpy as np

class Unicorn_Graphics():
    '''Custom graphics class for the Unicorn HAT HD'''
    def __init__(self, rotation=0, brightness=0.5):
        unicornhathd.rotation(rotation)
        unicornhathd.brightness(brightness)
        unicornhathd.clear()

    def draw(self, pixels):
        '''Draws the pixels to the Unicorn HAT HD
        
        pixels is a 2d array of Pixel objects
        '''
        for x in range(16):
            for y in range(16):
                pixel = pixels[x][y]
                if pixel.is_set:
                    r = pixel.r
                    g = pixel.g
                    b = pixel.b
                else:
                    r = 0
                    g = 0
                    b = 0

                unicornhathd.set_pixel(x, y, r, g, b)

        unicornhathd.show()

class Pixel():
    '''
    Pixel object for drawing on the Unicorn HAT HD

    r, g, b are the RGB values of the pixel
    is_set is a boolean that is True if the pixel has been set and False otherwise
    '''
    def __init__(self):
        '''Initializes an unset pixel'''
        self.r = None
        self.g = None
        self.b = None
        self.is_set = False

    def set(self, r, g, b):
        '''Sets the RGB values of the pixel'''
        # Clamp the RGB values to 0-255 and convert them to ints
        self.r = int(max(0, min(255, r)))
        self.g = int(max(0, min(255, g)))
        self.b = int(max(0, min(255, b)))
        # Set is_set to True
        self.is_set = True

    def unset(self):
        '''Unsets the pixel'''
        self.r = None
        self.g = None
        self.b = None
        self.is_set = False

class Display():
    '''Display object for drawing on the Unicorn HAT HD'''
    def __init__(self, display_x=16, display_y=16):
        self.display_x = display_x
        self.display_y = display_y
        # Create a 16x16 array of pixels
        self.pixels = [[Pixel() for x in range(self.display_x)] for y in range(self.display_y)]

        self.uni_graphics = Unicorn_Graphics()
    
    def update(self):
        '''Updates the display to the Unicorn HAT HD'''
        self.uni_graphics.draw(self.pixels)

    def clear(self):
        '''Clears the pixels in the array'''
        for x in range(self.display_x):
            for y in range(self.display_y):
                self.pixels[x][y] = Pixel()
        
        self.update()

    def set(self, pixels):
        '''Sets the pixels in the array
        
        pixels is a 2d array of Pixel objects'''
        self.pixels = pixels
        self.update()

    def draw_on_top(self, pixels):
        '''Draws the pixels on top of the existing pixels
        
        pixels is a 2d array of Pixel objects'''
        for i, row in enumerate(pixels):
            for j, pixel in enumerate(row):
                if pixel.is_set: # Only set the pixel if it is set
                    self.pixels[i][j].set(pixel.r, pixel.g, pixel.b)

        self.update()

    def draw_on_bottom(self, pixels):
        '''Draws the pixels on the bottom of the existing pixels
        
        pixels is a 2d array of Pixel objects'''
        for i, row in enumerate(pixels):
            for j, pixel in enumerate(row):
                if pixel.is_set and not self.pixels[i][j].is_set: # Only set the pixel if it is not already set
                    self.pixels[i][j].set(pixel.r, pixel.g, pixel.b)

        self.update()

    
class Circle():
    '''Circle object for drawing on the Unicorn HAT HD'''
    def __init__(self, center_x, center_y, radius, rgb=(255,255,255), filled=True, display_x=16, display_y=16):
        # Center coordinates of the circle
        self.center_x = center_x
        self.center_y = center_y

        # RGB values of the circle
        self.r = rgb[0]
        self.g = rgb[1]
        self.b = rgb[2]

        # Radius of the circle
        self.radius = radius

        # Pixel RGB values of the circle
        self.pixels = [[Pixel() for x in range(display_x)] for y in range(display_y)]

        # Whether the circle is filled or not
        self.filled = filled

        # Set the display size
        self.display_x = display_x
        self.display_y = display_y

        # Draw the circle into the 16x16 pixel array
        if filled:
            self.draw_filled()
        else:
            self.draw_outline()
            

    def draw_outline(self):
        '''Draws the outline of the circle using Bresenham's algorithm'''
        x = 0
        y = self.radius
        d = 3 - 2 * self.radius

        while y >= x:
            # Draw the eight symmetric points
            self.draw_circle_points(x, y)
            
            x += 1
            if d > 0:
                y -= 1
                d = d + 4 * (x - y) + 10
            else:
                d = d + 4 * x + 6

    def draw_circle_points(self, x, y):
        # Draw the eight symmetric points
        self.set_pixel(self.center_x + x, self.center_y + y)
        self.set_pixel(self.center_x - x, self.center_y + y)
        self.set_pixel(self.center_x + x, self.center_y - y)
        self.set_pixel(self.center_x - x, self.center_y - y)
        self.set_pixel(self.center_x + y, self.center_y + x)
        self.set_pixel(self.center_x - y, self.center_y + x)
        self.set_pixel(self.center_x + y, self.center_y - x)
        self.set_pixel(self.center_x - y, self.center_y - x)

    def set_pixel(self, x, y):
        # Ensure the pixel is within bounds
        if 0 <= x < len(self.pixels) and 0 <= y < len(self.pixels[0]):
            self.pixels[x][y].set(self.r, self.g, self.b)
       
    def draw_filled(self):
        '''Draws the filled circle using breseham's algorithm'''
        # Bresenham's circle algorithm
        for x in range(self.display_x):
            for y in range(self.display_y):
                if (x - self.center_x)**2 + (y - self.center_y)**2 <= self.radius**2:
                    self.pixels[x][y].set(self.r, self.g, self.b)
    
class Line():
    def __init__(self, x1, y1, x2, y2, rgb=(255,255,255), pixels=None, display_x=16, display_y=16):
        # Coordinates of the line
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        
        # RGB values of the line
        self.r = rgb[0]
        self.g = rgb[1]
        self.b = rgb[2]
        
        # Assuming 16x16 display, these will stay None
        self.display_x = display_x
        self.display_y = display_y
        
        if pixels is None:
            self.pixels = [[(0, 0, 0) for x in range(self.display_x)] for y in range(self.display_y)]
        else:
            self.pixels = pixels

        self.pixels = self.draw_line(self.pixels, self.x1, self.y1, self.x2, self.y2, self.r, self.g, self.b)

    def draw_line(self, pixels, x1, y1, x2, y2, r, g, b):
        '''Draws a line on the 16x16 pixel array'''
        # Bresenham's line algorithm
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = -1 if x1 > x2 else 1
        sy = -1 if y1 > y2 else 1
        err = dx - dy

        while True:
            pixels[x1][y1] = (r, g, b)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

        return pixels

class Quad():
    def __init__(self, c1, c2, c3, c4, rgb=(255,255,255), pixels=None, filled=False, display_x=16, display_y=16):
        # Center coordinates of the Quad
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.c4 = c4

        # RGB values of the Quad
        self.r = rgb[0]
        self.g = rgb[1]
        self.b = rgb[2]

        self.filled = filled
        self.display_x = display_x
        self.display_y = display_y

        if pixels is None:
            self.pixels = [[(0, 0, 0) for x in range(self.display_x)] for y in range(self.display_y)]
        else:
            self.pixels = pixels

        # Draw the Quad into the 16x16 pixel array
        self.pixels = self.draw_quad(self.pixels, self.c1, self.c2, self.c3, self.c4, self.r, self.g, self.b, self.filled)
        
    def draw_quad(self, pixels, c1, c2, c3, c4, r, g, b, filled):
        '''
        Draws a Quad on the 16x16 pixel array
        c1, c2, c3, c4 are the four corners of the Quad and are tuples of (x, y) coordinates
        Lines are drawn between c1 and c2, c2 and c3, c3 and c4, and c4 and c1
        '''

        # Draw the Quad
        s1 = np.array(Line(c1[0], c1[1], c2[0], c2[1], (r, g, b), pixels, self.display_x, self.display_y).pixels)
        s2 = np.array(Line(c2[0], c2[1], c3[0], c3[1], (r, g, b), pixels, self.display_x, self.display_y).pixels)
        s3 = np.array(Line(c3[0], c3[1], c4[0], c4[1], (r, g, b), pixels, self.display_x, self.display_y).pixels)
        s4 = np.array(Line(c4[0], c4[1], c1[0], c1[1], (r, g, b), pixels, self.display_x, self.display_y).pixels)

        # Combine the four matrices
        pixels = s1 + s2 + s3 + s4

        # Fill in the Quad
        if filled:
            for x in range(16):
                fill = False
                for y in range(16):
                    r_, g_, b_ = pixels[x][y]
                    if r_ != 0 and g_ != 0 and b_ != 0:
                        fill = not fill
                    if fill:
                        pixels[x][y] = (r, g, b)

        return pixels
    
# # # # # # # # # # #
# Helper functions  #

def overlay(top, bottom):
    '''
    Combines two pixel arrays
    
    pixels1 and pixels2 are numpy.ndarrays of shape (16, 16, 3)
    '''
    
    # Create a mask of the pixels that are not black
    mask = np.any(top != 0, axis=2)

    # Combine the two pixel arrays
    # np.where(condition, x, y) returns an array with the same shape as condition
    # where the elements are from x if condition is True, and from y otherwise
    # In this case, we are using the mask to determine which pixels to use
    # If the mask is True, use the pixels from the top array
    # If the mask is False, use the pixels from the bottom array
    result = np.where(mask[:,:,None], top, bottom)

    return result

# # # # # # # # # # #
# Test code         #

if __name__ == '__main__':
    d = Display()

    # Draw a circle
    circle = Circle(8, 8, 4, filled=False, rgb=(255, 0, 0))

    d.set(circle.pixels)