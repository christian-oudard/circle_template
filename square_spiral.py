import math
import vec
from shape_template import interpolate, polygon, format_points

radius = 5 * math.sqrt(2)
start_angle = 45
end_angle = 90 + 45

c = math.floor(radius)
center = (c, c)

num_steps = 20

def regular_polygon(radius, num_sides, start_angle):
    for i in range(num_sides):
        angle = start_angle - (i * 360) / num_sides
        point = (0, radius)
        yield vec.rotate(point, math.radians(angle))

for i in range(num_steps + 1):
    print(i)
    mu = i / num_steps
    angle = interpolate(start_angle, end_angle, mu)

    vertices = list(regular_polygon(radius, 4, angle))
    vertices = [vec.add(center, v) for v in vertices]
    points = polygon(vertices)

    print('-'*c*2)
    print(format_points(points, max_x=c*2, max_y=c*2, off='.'))
