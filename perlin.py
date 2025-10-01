# Simple Perlin noise implementation for terrain generation
import math
import random

def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

def lerp(a, b, t):
    return a + t * (b - a)

def grad(hash, x, y):
    h = hash & 3
    u = x if h < 2 else y
    v = y if h < 2 else x
    return (u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v)

class PerlinNoise:
    def __init__(self, seed=None):
        self.p = list(range(256))
        if seed is not None:
            random.seed(seed)
        random.shuffle(self.p)
        self.p += self.p

    def noise(self, x, y=0):
        X = int(math.floor(x)) & 255
        Y = int(math.floor(y)) & 255
        x -= math.floor(x)
        y -= math.floor(y)
        u = fade(x)
        v = fade(y)
        A = self.p[X] + Y
        B = self.p[X + 1] + Y
        return lerp(
            lerp(grad(self.p[A], x, y), grad(self.p[B], x - 1, y), u),
            lerp(grad(self.p[A + 1], x, y - 1), grad(self.p[B + 1], x - 1, y - 1), u),
            v
        )

# perlin = PerlinNoise(seed=42)
# value = perlin.noise(x, y)
