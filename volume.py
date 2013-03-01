import math
from collections import namedtuple

import vec
from shape_template import format_points

Point3 = namedtuple('Point', 'x, y, z')

## Types of volumes ##

def dist2(a, b):
    return (b.x - a.x)**2 + (b.y - a.y)**2 + (b.z - a.z)**2

class Sphere:
    def __init__(self, center, radius):
        self.center = Point3._make(center)
        self.radius = radius
        self.radius2 = radius**2

    def contains(self, point):
        point = Point3._make(point)
        return dist2(self.center, point) < self.radius2

    def bounds(self):
        c = self.center
        r = self.radius
        return integer_bounds([
            (c.x - r, c.x + r),
            (c.y - r, c.y + r),
            (c.z - r, c.z + r),
        ])

    def shifted(offset):
        return Sphere(
            vec.add(self.center, offset),
            self.radius,
        )

class PlaneBoundary:
    """
    Create a plane boundary shape, to intersect with other shapes.

    The direction of the normal vector determines which is the "on" side.
    """
    def __init__(self, center, normal):
        self.center = Point3._make(center)
        self.normal = normal

    def contains(self, point):
        raise NotImplementedError()

    def bounds(self):
        c = self.center
        return integer_bounds([
            (c.x, c.x),
            (c.y, c.y),
            (c.z, c.z),
        ])

## Bounding box math ##

#TODO Refactor bounds into a class or namedtuple.

def integer_bounds(bounds):
    result = []
    for lo, hi in bounds:
        result.append((
            int(math.floor(lo)),
            int(math.ceil(hi)),
        ))
    return result

def volume_list_bounds(volumes):
    # Get a bounding box for the whole collection of volumes.
    return union_bounds(v.bounds() for v in volumes)

def union_bounds(bounds_list):
    """
    Get the bounding box that surrounds all the bounding boxes passed in.

    Bounds are specified as lists of ranges, one range for each of the x, y, and z dimensions.
    Each range is a (lo, hi) pair.
    """
    bounds_iter = iter(bounds_list)

    first = next(bounds_iter)
    (
        (xmin, xmax),
        (ymin, ymax),
        (zmin, zmax),
    ) = first

    for b in bounds_iter:
        (
            (xlo, xhi),
            (ylo, yhi),
            (zlo, zhi),
        ) = b
        xmin = min(xmin, xlo)
        xmax = max(xmax, xhi)
        ymin = min(ymin, ylo)
        ymax = max(ymax, yhi)
        zmin = min(zmin, zlo)
        zmax = max(zmax, zhi)
    return [
        (xmin, xmax),
        (ymin, ymax),
        (zmin, zmax),
    ]

def normalize_range(r):
    """
    Shift a range so it starts with zero, but keeps the same size.
    """
    lo, hi = r
    return (0, hi - lo)

def points_in_bounds(bounds):
    (
        (xlo, xhi),
        (ylo, yhi),
        (zlo, zhi),
    ) = bounds
    for x in range(xlo, xhi + 1):
        for y in range(ylo, yhi + 1):
            for z in range(zlo, zhi + 1):
                yield Point3(x, y, z)

## Geometry calculations ##

def render(volume):
    for p in points_in_bounds(volume.bounds()):
        if volume.contains(p):
            yield p

def translate(points, offset):
    return [
        Point3._make(vec.add(p, offset))
        for p in points
    ]

def split_layers(points):
    zmin = min(p.z for p in points)
    zmax = max(p.z for p in points)

    for z in range(zmin, zmax + 1):
        layer_points = []
        for p in points:
            if p.z == z:
                layer_points.append(p)
        yield layer_points


## Drawing logic ##

def draw_layers(points, on='[]', off='  '):
    # Shift the geometry so that every point has (x, y, z) all greater than 0
    xmax = max(p.x for p in points)
    xmin = min(p.x for p in points)
    ymax = max(p.y for p in points)
    ymin = min(p.y for p in points)
    zmax = max(p.z for p in points)
    zmin = min(p.z for p in points)

    offset = (-xmin, -ymin, -zmin)
    points = translate(points, offset)

    # Update the max and min values.
    xmax -= xmin
    xmin = 0
    ymax -= ymin
    ymin = 0
    zmax -= zmin
    zmin = 0

    # Split the points into layers.
    diagrams = []
    for layer in split_layers(points):
        # Restrict to 2D points only for drawing.
        layer = [(p.x, p.y) for p in layer]
        # Draw the current layer.
        diagrams.append(
            format_points(
                layer,
                max_x=xmax,
                max_y=ymax,
                on=on,
                off=off,
            )
        )
    return diagrams
