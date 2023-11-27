import unittest
from libraries.graphics import unicorn_graphics

class TestGraphics(unittest.TestCase):

    def set_pixel(pixels, mask):
        for x in range(16):
            for y in range(16):
                if mask[x][y]:
                    pixels[x][y].set(1, 2, 3)
        

    def test_pixel(self):
        pixel = unicorn_graphics.Pixel()
        self.assertFalse(pixel.is_set)

        pixel.set(1, 2, 3)
        self.assertEqual(pixel.r, 1)
        self.assertEqual(pixel.g, 2)
        self.assertEqual(pixel.b, 3)
        self.assertTrue(pixel.is_set)

    def test_circle(self):
        circle = unicorn_graphics.Circle(5, 5, 3)

        mock_pixels = [[unicorn_graphics.Pixel() for x in range(16)] for y in range(16)]

        # Filled circle in a 16x16 list of 1s and 0s
        circle_mask = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,0,0,x,0,0,1,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        

if __name__ == '__main__':
    unittest.main()