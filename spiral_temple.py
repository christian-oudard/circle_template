import math
from shape_template import interpolate, ring, radial_slice, format_points

ring_width = 3.2
slice_angle = 45

min_radius = 10.5
max_radius = 0

min_angle = -360 * 1.5
max_angle = 0

num_steps = 40

c = math.floor(max(min_radius, max_radius))
center = (c, c)

for mu in range(num_steps + 1):
    mu = mu / num_steps
    print(mu)

    start_angle = interpolate(min_angle, max_angle, mu)
    end_angle = start_angle + slice_angle

    outer = interpolate(min_radius, max_radius, mu)
    inner = outer - ring_width

    points = ring(center, outer, inner)
    points = radial_slice(points, center, start_angle, end_angle)
    print('-'*c*2)
    print(format_points(points, max_x=c*2, max_y=c*2, off='.'))
