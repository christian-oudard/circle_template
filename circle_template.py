import math

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
            points.append((x, y))

    circle_points = []
    for x, y in points:
        dist2 = (x - cx)**2 + (y - cy)**2
        if dist2 <= radius2:
            circle_points.append((x, y))

    return set(circle_points)

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

def offset_points(points):
    """
    Move points to fit nicely in the +x, +y quadrant.
    >>> points = circle((0, 0), 2.3)
    >>> print(format_points(points))
    ###
    ###
    ##
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

def format_points(points):
    """
    >>> points = circle((1.5, 1.5), 2)
    >>> print(format_points(points))
     ##
    ####
    ####
     ##
    """
    max_x = max(x for x, y in points)
    max_y = max(y for x, y in points)

    lines = []
    for x in range(max_x + 1):
        line = []
        for y in range(max_y + 1):
            if (x, y) in points:
                line.append('#')
            else:
                line.append(' ')
        lines.append(''.join(line).rstrip())
    return '\n'.join(lines)

if __name__ == '__main__':
    pass
