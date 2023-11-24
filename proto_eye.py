import numpy as np
import matplotlib.pyplot as plt
import libraries.graphics.unicorn_graphics as ug

d = ug.Display()

# Draw a circle
sclera = ug.Circle(8, 8, 6, rgb=(255, 192, 203))

# Draw a quad for the eyebrow
eyebrow = ug.Polygon([(0, 0), (0, 15), (6, 15), (12, 0)], filled=True, rgb=(255, 0, 0))

d.set(sclera.pixels)
import time
time.sleep(1)
d.draw_on_top(eyebrow.pixels)