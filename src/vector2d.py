import math


class Vector2D:
    def __init__(self, x:float = 0, y:float = 0):
        self.x: float = x
        self.y: float = y

    def __add__(self, outro_vetor):
        return Vector2D(self.x + outro_vetor.x, self.y + outro_vetor.y)

    def __sub__(self, outro_vetor):
        return Vector2D(self.x - outro_vetor.x, self.y - outro_vetor.y)
    
    def __mul__(self, other):
        new_vec = Vector2D(self.x, self.y)
        new_vec.x *= other
        new_vec.y *= other
        return new_vec
    
    def __rmul__(self, other):
        new_vec = Vector2D(self.x, self.y)
        new_vec.x *= other
        new_vec.y *= other
        return new_vec
    
    def __truediv__(self, other):
        new_vec = Vector2D(self.x, self.y)
        new_vec.x = new_vec.x / other
        new_vec.y = new_vec.y / other
        return new_vec
    
    def __neg__(self):
        return Vector2D(-self.x, -self.y)

    def __str__(self):
        return f"(x={self.x:.2f}, y={self.y:.2f})"

    def tamanho(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def angulo(self):
        return math.atan2(self.y, self.x)

    def as_tuple(self):
        return (self.x, self.y)
    
    def normalize(self):
        size = self.tamanho()
        self.x = self.x / size
        self.y = self.y / size

        return self
    
    def dot(self, other_vector):
        return self.x*other_vector.x + self.y*other_vector.y
