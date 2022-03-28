from geometry.point import Point
import math
import geometry.linalg as linalg

class Polygon:
    def __init__(self, points: [Point]):
        self.points = points

    def contains(self, point: Point) -> bool:
        intercepts = 0
        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = self.points[i + 1] if i != len(self.points) - 1 else self.points[0]
            
            slope = (p2.y-p1.y)/((p2.x-p1.x + .01))
            if slope != 0:
                y = point.y

                mag = linalg.get_magnitude(p1,p2)
                x = (y - p1.y) / (slope) + p1.x
                if x >= min(p1.x,p2.x) and x <= max(p1.x, p2.x) and (p1.x > point.x or p2.x > point.x):
                    intercepts += 1
        
#                print(f"{p1} {p2}: {x} {intercepts}")
        return intercepts % 2 == 1
