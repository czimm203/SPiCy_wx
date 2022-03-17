import math



class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"({self.x},{self.y})"
    def create_segment_endpoint(self, theta: float, magnitude: float = 180):
        return Point(self.x + math.cos(math.radians(theta)), self.y + math.sin(math.radians(theta))) 


               
