import unicornhathd

class Unicorn_Graphics():
    '''Custom graphics class for the Unicorn HAT HD'''
    def __init__(self, rotation=0, brightness=0.5):
        unicornhathd.rotation(rotation)
        unicornhathd.brightness(brightness)

    def draw_circle(self, pixels, center_x, center_y, radius, r, g, b):
        '''Draws a circle on the 16x16 pixel array'''
        for x in range(16):
            for y in range(16):
                if (x - center_x)**2 + (y - center_y)**2 <= radius**2:
                    pixels[x][y] = (r, g, b)

        return pixels
        
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
    
    def draw_square(self, pixels, c1, c2, c3, c4, r, g, b):
        '''Draws a square on the 16x16 pixel array'''
        pixels = self.draw_line(pixels, c1[0], c1[1], c2[0], c2[1], r, g, b)
        pixels = self.draw_line(pixels, c2[0], c2[1], c3[0], c3[1], r, g, b)
        pixels = self.draw_line(pixels, c3[0], c3[1], c4[0], c4[1], r, g, b)
        pixels = self.draw_line(pixels, c4[0], c4[1], c1[0], c1[1], r, g, b)

        # Fill in the square
        for x in range(c1[0], c3[0]):
            for y in range(c1[1], c3[1]):
                pixels[x][y] = (r, g, b)

        return pixels