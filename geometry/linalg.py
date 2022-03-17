from geometry.point import Point
import math


def get_magnitude(p1: Point, p2: Point):
    return math.sqrt((p2.y - p1.y)**2 + (p2.x - p1.x)**2)

def dot(s1: [Point, Point], s2: [Point, Point]) -> float:
    x1 = s1[0].x - s1[1].x
    y1 = s1[0].y - s1[1].y 
    x2 = s2[0].x - s2[1].x
    y2 = s2[0].y - s2[1].y
    
    return x1 * x2 + y1 * y2

def is_parallel(s1: [Point, Point], s2: [Point, Point]) -> bool:
    return dot(s1,s2) == 1
