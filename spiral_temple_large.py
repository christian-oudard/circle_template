import math
from shape_template import interpolate, ring, radial_slice, format_points

ring_width = 1.3
slice_width = 4.8

min_radius = 16.5
max_radius = 0

min_angle = -360 * 2.0
max_angle = 0

num_steps = 60

c = math.floor(max(min_radius, max_radius))
center = (c, c)

layers = []
for step in range(num_steps + 1):
    mu = step / num_steps

    outer = interpolate(min_radius, max_radius, mu)
    if outer <= 0:
        break

    inner = outer - ring_width

    start_angle = interpolate(min_angle, max_angle, mu)
    slice_angle = (slice_width / (outer * 2 * math.pi)) * 360

    end_angle = start_angle + slice_angle


    points = ring(center, outer, inner)
    points = radial_slice(points, center, start_angle, end_angle)
    layers.append(points)

def by_twos(iterable):
    iterable = iter(iterable)
    while True:
        yield next(iterable), next(iterable)

for z, (a, b) in enumerate(by_twos(layers)):
    a_lines = format_points(a, on='_', off='.', max_x=c*2, max_y=c*2, raw=True)
    b_lines = format_points(b, on='#', max_x=c*2, max_y=c*2, raw=True)
    for y, line in enumerate(b_lines):
        for x, character in enumerate(line):
            if character == '#':
                a_lines[y][x] = '#'

    if a_lines[c][c] != '#':
        a_lines[c][c] = 'X'

    print('-'*c*2)
    print('z', z)
    print('\n'.join(''.join(line).rstrip() for line in a_lines))
