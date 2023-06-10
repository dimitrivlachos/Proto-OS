
import unicornhathd
from enum import Enum

# Enum for the chirality of the eye
class Chirality(Enum):
    Left = 0
    Right = 1

class Proto_Eye():
    def __init__(self, chirality, x, y, r, g, b):
        self.chirality = chirality
        # Create 16 x 16 array of pixels
        self.pixels = [[0 for x in range(16)] for y in range(16)]