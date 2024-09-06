import math


class Vector2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, outro_vetor):
        return Vector2D(self.x + outro_vetor.x, self.y + outro_vetor.y)

    def __sub__(self, outro_vetor):
        return Vector2D(self.x - outro_vetor.x, self.y - outro_vetor.y)

    def __str__(self):
        return f"(x={self.x:.2f}, y={self.y:.2f})"

    def tamanho(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def angulo(self):
        return math.atan2(self.y, self.x)

    def as_tuple(self):
        return (self.x, self.y)