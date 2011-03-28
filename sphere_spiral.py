import math
import vec
from shape_template import interpolate, circle, radial_slice, format_points

sphere_radius = 15.4
inner_sphere_radius = sphere_radius - 1.2
half_num_steps = math.floor(sphere_radius)
min_z = -half_num_steps
max_z = half_num_steps

min_angle = -360
max_angle = 0
slice_angle = 90

c = math.floor(sphere_radius)
center = (c + 0.5, c + 0.5)

def slice_radius(sphere_radius, z):
    return math.sqrt(max(sphere_radius**2 - z**2, 0))

for z in range(-half_num_steps, half_num_steps + 1):
    print('z', z)

    mu = z / (max_z - min_z)

    r1 = slice_radius(sphere_radius, z)
    points = circle(center, r1)
    r2 = slice_radius(inner_sphere_radius, z)
    points -= circle(center, r2)

    start_angle = interpolate(min_angle, max_angle, mu)
    end_angle = start_angle + slice_angle
    slice_1 = radial_slice(points, center, start_angle, end_angle)

    start_angle = start_angle + 180
    end_angle = start_angle + slice_angle
    slice_2 = radial_slice(points, center, start_angle, end_angle)

    points = slice_1 | slice_2

    print('-'*c*2)
    print(format_points(points, max_x=c*2, max_y=c*2, off='.'))
