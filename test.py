import libraries.graphics.unicorn_graphics as unicorn_graphics
import numpy as np

u = unicorn_graphics.Unicorn_Graphics()

# Draw a circle
circle1 = unicorn_graphics.Circle(8, 8, 8, rgb=(255, 0, 0))

# Draw a smaller circle on top of the first circle
circle2 = unicorn_graphics.Circle(8, 8, 6, rgb=(0, 0, 255), filled=False)

#Draw a square
square = unicorn_graphics.Quad((1,1), (1,5), (5,5), (5,1), rgb=(0, 255, 0))

#print(type(square.pixels))

pixels = unicorn_graphics.overlay(circle2.pixels, circle1.pixels)
pixels = unicorn_graphics.overlay(square.pixels, pixels)

u.draw(pixels)
