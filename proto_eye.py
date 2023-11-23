import numpy as np
import matplotlib.pyplot as plt
import libraries.graphics.unicorn_graphics as ug

u = ug.Unicorn_Graphics()

# Draw a circle
sclera = ug.Circle(8, 8, 6, rgb=(255, 192, 203))

# Draw a quad for the eyebrow
eyebrow = ug.Quad((0, 0), (0, 15), (6, 15), (12, 0), filled=True, rgb=(255, 0, 0))

pixels = ug.overlay(eyebrow.pixels, sclera.pixels)

u.draw(pixels)
