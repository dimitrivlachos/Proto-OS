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

    def clear(self, update=False):
        '''Clears the pixels in the array'''
        for x in range(self.display_x):
            for y in range(self.display_y):
                self.pixels[x][y] = Pixel()
        
        if update:
            self.update()

    def set(self, pixels, update=False):
        '''Sets the pixels in the array
        
        pixels is a 2d array of Pixel objects'''
        self.pixels = pixels

        if update:
            self.update()

    def draw_on_top(self, pixels, update=False):
        '''Draws the pixels on top of the existing pixels
        
        pixels is a 2d array of Pixel objects'''
        for i, row in enumerate(pixels):
            for j, pixel in enumerate(row):
                if pixel.is_set: # Only set the pixel if it is set
                    self.pixels[i][j].set(pixel.r, pixel.g, pixel.b)

        if update:
            self.update()

    def draw_on_bottom(self, pixels, update=False):
        '''Draws the pixels on the bottom of the existing pixels
        
        pixels is a 2d array of Pixel objects'''
        for i, row in enumerate(pixels):
            for j, pixel in enumerate(row):
                if pixel.is_set and not self.pixels[i][j].is_set: # Only set the pixel if it is not already set
                    self.pixels[i][j].set(pixel.r, pixel.g, pixel.b)

        if update:
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
    def __init__(self, start, end, rgb=(255,255,255), display_x=16, display_y=16):
        '''Initializes a line object
        
        start and end are tuples of (x, y) coordinates
        rgb is a tuple of (r, g, b) values
        '''
        # Start and end coordinates of the line
        self.start = start
        self.end = end

        # RGB values of the line
        self.r = rgb[0]
        self.g = rgb[1]
        self.b = rgb[2]

        # Pixel RGB values of the line
        self.pixels = [[Pixel() for x in range(display_x)] for y in range(display_y)]

        # Set the display size
        self.display_x = display_x
        self.display_y = display_y

        # Draw the line into the 16x16 pixel array
        self.draw_line()


    def draw_line(self):
        '''Draws a line on the 16x16 pixel array'''
        # Unpack the start and end coordinates
        x1, y1 = self.start
        x2, y2 = self.end

        # Bresenham's line algorithm
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = -1 if x1 > x2 else 1
        sy = -1 if y1 > y2 else 1
        err = dx - dy

        while True:
            self.pixels[x1][y1].set(self.r, self.g, self.b)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

class Polygon():
    def __init__(self, vertices, rgb=(255,255,255), filled=False, display_x=16, display_y=16):
        '''Initializes a polygon object
        
        vertices is a list of tuples of (x, y) coordinates
        rgb is a tuple of (r, g, b) values
        '''
        # Vertices of the polygon
        self.vertices = vertices

        # RGB values of the polygon
        self.r = rgb[0]
        self.g = rgb[1]
        self.b = rgb[2]

        # Pixel RGB values of the polygon
        self.pixels = [[Pixel() for x in range(display_x)] for y in range(display_y)]

        # Whether the polygon is filled or not
        self.filled = filled

        # Set the display size
        self.display_x = display_x
        self.display_y = display_y

        # Draw the polygon into the 16x16 pixel array
        if filled:
            self.draw_filled()
        else:
            self.draw_outline()

    def draw_outline(self):
        '''Draws the outline of the polygon'''
        # Draw a line between each pair of vertices
        for i in range(len(self.vertices)):
            start = self.vertices[i]
            end = self.vertices[(i+1) % len(self.vertices)]
            line = Line(start, end, rgb=(self.r, self.g, self.b))
            
            # Draw the line on top of the existing pixels
            for x in range(self.display_x):
                for y in range(self.display_y):
                    if line.pixels[x][y].is_set:
                        self.pixels[x][y].set(line.r, line.g, line.b)

    def find_intersections(self, y):
        intersections = []
        for i in range(len(self.vertices)):
            start = self.vertices[i]
            end = self.vertices[(i + 1) % len(self.vertices)]

            # Check if the line segment crosses the scanline
            if min(start[1], end[1]) <= y < max(start[1], end[1]):
                # Calculate the x-coordinate of the intersection
                x_intersection = int(start[0] + (y - start[1]) / (end[1] - start[1]) * (end[0] - start[0]))
                intersections.append(x_intersection)

        return intersections

    def draw_filled(self):
        min_y = min([vertex[1] for vertex in self.vertices])
        max_y = max([vertex[1] for vertex in self.vertices])

        # Iterate through scanlines
        for y in range(min_y, max_y + 1):
            intersections = self.find_intersections(y)
            intersections.sort()

            # Fill in the pixels between intersections
            for i in range(0, len(intersections), 2):
                start = max(0, intersections[i])
                end = min(self.display_x - 1, intersections[i + 1])

                for x in range(start, end + 1):
                    self.pixels[x][y].set(self.r, self.g, self.b)
        
    
# # # # # # # # # # #
# Helper functions  #


# # # # # # # # # # #
# Test code         #

if __name__ == '__main__':
    import time
    d = Display()

    # Draw a circle
    circle1 = Circle(8, 8, 5, filled=False, rgb=(255, 0, 0))
    d.set(circle1.pixels)
    # delay
    
    time.sleep(1)

    circle2 = Circle(8, 8, 3, filled=True, rgb=(0, 255, 0))
    d.draw_on_top(circle2.pixels)

    time.sleep(1)

    # Draw a line
    line1 = Line((0, 0), (15, 15), rgb=(0, 0, 255))
    d.draw_on_top(line1.pixels)

    time.sleep(1)

    # Draw a polygon
    polygon1 = Polygon([(2, 2), (13, 2), (2, 13)], filled=False, rgb=(255, 0, 255))
    d.draw_on_top(polygon1.pixels)

    time.sleep(1)

    polygon2 = Polygon([(0, 0), (12, 2), (14, 15)], filled=True, rgb=(255, 255, 0))
    d.draw_on_bottom(polygon2.pixels)