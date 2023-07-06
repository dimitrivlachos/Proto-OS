import unicornhathd

class Unicorn_Graphics():
    '''Custom graphics class for the Unicorn HAT HD'''
    def __init__(self, rotation=0, brightness=0.5):
        unicornhathd.rotation(rotation)
        unicornhathd.brightness(brightness)
        unicornhathd.clear()

    def draw(self, pixels):
        '''Draws the pixels to the Unicorn HAT HD'''
        for x in range(16):
            for y in range(16):
                r, g, b = pixels[x][y]
                unicornhathd.set_pixel(x, y, r, g, b)

        unicornhathd.show()
    
class Circle():
    '''Circle object for drawing on the Unicorn HAT HD'''
    def __init__(self, center_x, center_y, radius, rgb=(255,255,255), pixels=None, filled=True, display_x=16, display_y=16):
        # Center coordinates of the circle
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius # Radius of the circle

        # RGB values of the circle
        self.r = rgb[0]
        self.g = rgb[1]
        self.b = rgb[2]

        # If filled is True, the circle will be filled in
        self.filled = filled
        # Assuming 16x16 display, these will stay None
        self.display_x = display_x
        self.display_y = display_y

        if pixels is None:
            self.pixels = [[(0, 0, 0) for x in range(self.display_x)] for y in range(self.display_y)]
        else:
            self.pixels = pixels

    def draw(self):
        '''Draws the circle on the 16x16 pixel array'''
        if self.filled:
            # If filled is True, draw the circle and return the pixels
            return self.draw_circle(self.pixels, self.center_x, self.center_y, self.radius, self.r, self.g, self.b)
        else:
            # If filled is False, draw the circle and then draw a smaller circle on top of it
            self.pixels = self.draw_circle(self.pixels, self.center_x, self.center_y, self.radius, self.r, self.g, self.b)
            return self.draw_circle(self.pixels, self.center_x, self.center_y, self.radius - 1, 0, 0, 0)

    def draw_circle(self, pixels, center_x, center_y, radius, r, g, b):
        '''Draws a circle on the 16x16 pixel array'''
        for x in range(16):
            for y in range(16):
                if (x - center_x)**2 + (y - center_y)**2 <= radius**2:
                    pixels[x][y] = (r, g, b)

        return pixels
    
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

class Square():
    def __init__(self, c1, c2, c3, c4, rgb=(255,255,255), pixels=None, filled=True, display_x=16, display_y=16):
        # Center coordinates of the square
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.c4 = c4

        # RGB values of the square
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

        # Draw the square into the 16x16 pixel array
        self.draw_square(self.pixels, self.c1, self.c2, self.c3, self.c4, self.r, self.g, self.b, self.filled)
        
    def draw_square(self, pixels, c1, c2, c3, c4, r, g, b, filled):
        '''Draws a square on the 16x16 pixel array'''
        # Draw the square
        pixels = Line(c1[0], c1[1], c2[0], c2[1], r, g, b, pixels=pixels).pixels
        pixels = Line(c2[0], c2[1], c3[0], c3[1], r, g, b, pixels=pixels).pixels
        pixels = Line(c3[0], c3[1], c4[0], c4[1], r, g, b, pixels=pixels).pixels
        pixels = Line(c4[0], c4[1], c1[0], c1[1], r, g, b, pixels=pixels).pixels

        # Fill in the square
        if filled:
            for x in range(c1[0], c3[0]):
                for y in range(c1[1], c3[1]):
                    pixels[x][y] = (r, g, b)

        return pixels