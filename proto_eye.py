import numpy as np
import matplotlib.pyplot as plt
import libraries.graphics.unicorn_graphics as ug

u = ug.Unicorn_Graphics()

# Draw a circle
sclera = ug.Circle(8, 8, 4, rgb=(255, 192, 203))

# Draw a quad for the eyebrow
eyebrow = ug.Quad((1, 1), (1, 16), (8, 1), (9, 16), rgb=(0, 0, 0), pixels=sclera.pixels)



u.draw(eyebrow.pixels)