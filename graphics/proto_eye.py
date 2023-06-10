
import unicornhathd
from enum import Enum

# Enum for the chirality of the eye
class Chirality(Enum):
    Left = 0
    Right = 1

class Proto_Eye():
    def __init__(self, chirality):
        self.chirality = chirality

    