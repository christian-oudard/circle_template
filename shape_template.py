import math
import vec

def even_circle(radius):
    c = math.floor(radius + 0.5) + 0.5
    return circle((c, c), radius)

def circle(center, radius):
    """
    >>> points = circle((1.5, 1.5), 2)
    >>> len(points)
    12
    >>> sorted(points)
    [(0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2)]
    """
    radius2 = radius**2

    cx, cy = center
    min_x = int(math.ceil(cx - radius))
    max_x = int(math.floor(cx + radius))
    min_y = int(math.ceil(cy - radius))
    max_y = int(math.floor(cy + radius))

    points = []
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            dist2 = (x - cx)**2 + (y - cy)**2
            if dist2 <= radius2:
                points.append((x, y))
    return set(points)

def ring(center, outer_radius, inner_radius):
    """
    >>> print(format_points(offset_points(ring((0, 0), 3.5, 1.0))))
      ###
     #####
    ### ###
    ##   ##
    ### ###
     #####
      ###
    """
    return circle(center, outer_radius) - circle(center, inner_radius)

def radial_slice(points, center, start_angle, end_angle):
    """
    >>> points = circle((0, 0), 2.3)
    >>> print(format_points(offset_points(points)))
     ###
    #####
    #####
    #####
     ###
    >>> points = radial_slice(points, (0, 0), -90, 45)
    >>> print(format_points(offset_points(points)))
     ##
    ###
    ###
    ##
    >>> points = radial_slice(points, (0, 0), 0, 30)
    >>> print(format_points(offset_points(points)))
      #
    ###
    """
    start_point = (1, 0)
    start_point = vec.rotate(start_point, math.radians(start_angle))
    start_point = vec.add(center, start_point)
    start_line = (start_point, center) # Pointing inward, so partition goes counter-clockwise.

    end_point = (1, 0)
    end_point = vec.rotate(end_point, math.radians(end_angle))
    end_point = vec.add(center, end_point)
    end_line = (center, end_point) # Pointing outward, so partition goes clockwise.

    return (
        set(partition(points, *start_line)) &
        set(partition(points, *end_line))
    )

def sign_of(x):
    if x == 0:
        return 0
    if x > 0:
        return 1
    if x < 0:
        return -1

def cmp_line(l1, l2, p, epsilon=1e-10):
    """
    Determine where the point p lies with relation to the line l1-l2.
    Return -1 if s is below, +1 if it is above, and 0 if it is on the line.

    >>> cmp_line((-1,-1), (1,1), (1,0))
    -1
    >>> cmp_line((-1,-1), (1,1), (0,1))
    1
    >>> cmp_line((-1,-1), (1,1), (0,0))
    0

    It also works with vertical lines.
    >>> cmp_line((0,-1), (0,1), (1, 0))
    -1
    >>> cmp_line((0,-1), (0,1), (-1, 0))
    1
    >>> cmp_line((0,-1), (0,1), (0, 0))
    0

    Very close points count as on the line.
    >>> cmp_line((0,-1), (0,1), (1e-16, 0))
    0
    """
    x1, y1 = l1
    x2, y2 = l2
    x, y = p
    dy = y2 - y1
    dx = x2 - x1
    c = (y * dx) - (dy * (x - x1) + y1 * dx)
    if abs(c) < epsilon:
        return 0
    return sign_of(c)

def partition(points, l1, l2, s=None):
    """
    Partition a set of points by a line.

    The line is defined by l1, l2. The desired side of the line is given by the
    point s.

    If s is not given, return points to the right of the line.

    If eq is True, also include points on the line.

    >>> sorted(partition([(-1,0), (0,0), (1,0)], (0,1), (0,-1), (2,0)))
    [(0, 0), (1, 0)]
    >>> sorted(partition([(-1,0), (0,0), (1,0)], (0,1), (0,-1), (-2,0)))
    [(-1, 0), (0, 0)]
    >>> points = [(-2,2), (-1,0), (0,0), (1,0)]
    >>> sorted(partition(points, (-1,0), (0,1), (3,0)))
    [(-1, 0), (0, 0), (1, 0)]
    >>> sorted(partition(points, (-1,0), (0,1), (-3,0)))
    [(-2, 2), (-1, 0)]

    You can omit the argument "s" if you don't care.
    >>> sorted(partition([(-1,0), (0,0), (1,0)], (0,1), (0,-1)))
    [(-1, 0), (0, 0)]
    """
    if s is None:
        s = vec.add(l1, vec.perp(vec.vfrom(l1, l2)))

    if l1 == l2:
        raise ValueError('l1 equals l2')
    sign = sign_of(cmp_line(l1, l2, s))
    if sign == 0:
        raise ValueError('s is on the line l1 l2')

    for p in points:
        c = cmp_line(l1, l2, p)
        if c == sign:
            yield p
        elif c == 0:
            yield p

def offset_points(points):
    """
    Move points to fit nicely in the +x, +y quadrant.
    >>> points = circle((0, 0), 2.3)
    >>> print(format_points(points))
    ##
    ###
    ###
    >>> points = offset_points(points)
    >>> print(format_points(points))
     ###
    #####
    #####
    #####
     ###
    """
    min_x = min(x for x, y in points)
    min_y = min(y for x, y in points)
    return set((x - min_x, y - min_y) for x, y in points)

def format_points(points, max_x=None, max_y=None, on='#', off=' '):
    """
    >>> print(format_points([(1, 0), (2, 0), (0, 1), (1, 1)]))
    ##
     ##
    >>> format_points([])
    ''
    """
    if not points:
        return ''
    if max_x is None:
        max_x = max(x for x, y in points)
    if max_y is None:
        max_y = max(y for x, y in points)

    lines = []
    for y in range(max_y + 1):
        line = []
        for x in range(max_x + 1):
            if (x, max_y - y) in points:
                line.append(on)
            else:
                line.append(off)
        lines.append(''.join(line).rstrip())
    return '\n'.join(lines)

def interpolate(low, high, mu):
    """
    >>> [interpolate(0, 20, m/10) for m in range(10 + 1)]
    [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0]
    """
    #return low + (high - low) * mu # Naive version, could exhibit catastrophic cancellation.
    return low * (1 - mu) + high * mu

def polygon(vertices):
    """
    Specify a polygon with the clockwise series of vertices.
    >>> print(format_points(polygon([(0, 0), (0, 2), (2, 2), (4, 0)])))
    ###
    ####
    #####
    >>> print(format_points(polygon([(0, 0), (0, 2.3), (2.7, 0)])))
    #
    ##
    ###
    """
    min_x = math.floor(min(x for x, y in vertices))
    max_x = math.ceil(max(x for x, y in vertices))
    min_y = math.floor(min(y for x, y in vertices))
    max_y = math.ceil(max(y for x, y in vertices))

    points = [(x, y) for x in range(min_x, max_x + 1) for y in range(min_y, max_y + 1)]
    for a, b in zip(vertices, vertices[1:] + [vertices[0]]):
        points = list(partition(points, a, b))
    return set(points)
