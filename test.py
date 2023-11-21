import libraries.graphics.unicorn_graphics as unicorn_graphics

u = unicorn_graphics.Unicorn_Graphics()

# Draw a circle
circle = unicorn_graphics.Circle(8, 8, 8, rgb=(255, 0, 0))

# Draw the circle on the Unicorn HAT HD
u.draw(circle.draw())

# Draw a smaller circle on top of the first circle
circle = unicorn_graphics.Circle(8, 8, 7, rgb=(0, 0, 0), filled=False)

#Draw a square
square = unicorn_graphics.Square(0, 0, 16, rgb=(0, 255, 0))