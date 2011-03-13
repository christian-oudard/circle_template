import math
import vec
from shape_template import interpolate, circle, format_points

sphere_radius = 5.3
num_steps = 10

c = math.floor(sphere_radius)
center = (c, c)

for step in range(num_steps + 1):
    mu = step / num_steps
    z = step / 2
    print('z', z)

    slice_radius_squared = max(sphere_radius**2 - z**2, 0)
    slice_radius = math.sqrt(slice_radius_squared)
    points = circle(center, slice_radius)

    print('-'*c*2)
    print(format_points(points, max_x=c*2, max_y=c*2, off='.'))
