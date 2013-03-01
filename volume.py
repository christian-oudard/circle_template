import math
from collections import namedtuple

import vec
from shape_template import format_points

#TODO: clean up render(v) vs v.render()
#TODO: Match minecraft-style stairs and half-slabs as well as possible when rendering.

Point3 = namedtuple('Point', 'x, y, z')

## Utility functions ##

def dist2(a, b):
    return (b.x - a.x)**2 + (b.y - a.y)**2 + (b.z - a.z)**2

## Types of volumes ##

class Volume:
    def render(self):
        for p in self.bounds().render():
            if self.contains(p):
                yield p

class Box(Volume):
    """
    Boxes are specified by a list of dimension bounds.
    """
    def __init__(self, bounds):
        self._bounds = bounds

    def contains(self, point):
        (
            (xlo, xhi),
            (ylo, yhi),
            (zlo, zhi),
        ) = self.bounds
        p = point
        return (
            xlo < p.x < xhi and
            ylo < p.y < yhi and
            zlo < p.z < zhi
        )

    def bounds(self):
        return self._bounds

    def render(self):
        (
            (xlo, xhi),
            (ylo, yhi),
            (zlo, zhi),
        ) = self._bounds
        for x in range(xlo, xhi + 1):
            for y in range(ylo, yhi + 1):
                for z in range(zlo, zhi + 1):
                    yield Point3(x, y, z)

    def to_integers(self):
        integer_bounds = []
        for lo, hi in self._bounds:
            integer_bounds.append((
                int(math.floor(lo)),
                int(math.ceil(hi)),
            ))
        return Box(integer_bounds)

    def union(self, other):
        """
        Get the bounding box that surrounds both boxes.
        """
        return Box([
            (
                min(self.xlo, other.xlo),
                max(self.xhi, other.xhi),
            ),
            (
                min(self.ylo, other.ylo),
                max(self.yhi, other.yhi),
            ),
            (
                min(self.zlo, other.zlo),
                max(self.zhi, other.zhi),
            ),
        ])

    @classmethod
    def from_volumes(cls, volumes):
        """
        Get a bounding box which surrounds all the volumes passed in.
        """
        first = volumes[0]
        box = first.bounds()
        for v in volumes[1:]:
            box = box.union(v.bounds())
        return box


class Sphere(Volume):
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
        return Box([
            (c.x - r, c.x + r),
            (c.y - r, c.y + r),
            (c.z - r, c.z + r),
        ]).to_integers()

    def shifted(offset):
        return Sphere(
            vec.add(self.center, offset),
            self.radius,
        )

class Plane(Volume):
    """
    Create a plane boundary shape, to intersect with other shapes.

    The direction of the normal vector determines which is the "on" side.
    """
    def __init__(self, center, normal, bounds):
        self.center = Point3._make(center)
        self.normal = normal
        self._bounds = bounds

    def contains(self, point):
        sign = vec.dot(
            vec.vfrom(self.center, point),
            self.normal,
        )
        return (sign >= 0)

    def bounds(self):
        return self._bounds

#TODO: Polyhedron volume made from Plane objects.
class Polyhedron(Volume):
    def __init__(self, vertices):
        #TODO:
        # Find the convex shell of the vertices.
        # Raise an error if the vertices were not convex.
        # Construct planar boundaries from the convex shell.
            # Calculate the bounding box of the vertices.
            # Initialize the half plane volumes with the bounding box.
        pass

    def contains(self, point):
        #TODO:
        # Check against all of the plane boundaries.
        pass

## Geometry calculations ##

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
