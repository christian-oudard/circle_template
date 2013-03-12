from nose.tools import assert_equal

import math
from textwrap import dedent

from volume import (
    Box,
    Sphere,
    Plane,
    Path,
    Point3,
    draw_layers,
    lerp,
)


def test_box_from_volumes():
    volumes = [
        Sphere((1, 1, 1), 3),
        Sphere((-1, -1, -1), 3),
    ]
    bounds = Box.from_volumes(volumes)
    assert_equal(
        bounds,
        Box([(-4, 4), (-4, 4), (-4, 4)]),
    )


def test_sphere():
    # Draw connected spheres, which are small enough to just be 8 points in a
    # 2x2x2 cube.
    a = Sphere((0.5, 0.5, 0.5), 1)
    b = Sphere((-0.5, -0.5, -0.5), 1)
    points = set(a.render()) | set(b.render())

    layers = draw_layers(points, on='#', off='-')

    assert_equal(
        '\n\n'.join(layers),
        dedent('''
            ---
            ##-
            ##-

            -##
            ###
            ##-

            -##
            -##
            ---
        ''').strip(),
    )


def test_plane():
    bounds = Box([(0, 3), (0, 3), (0, 3)])
    plane = Plane((1.5, 1.5, 1.5), (1, 1, 1), bounds)
    field = set(bounds.render())
    points = field - set(plane.render())

    layers = draw_layers(points, on='#', off='-')

    assert_equal(
        '\n\n'.join(layers),
        dedent('''
            ##--
            ###-
            ####
            ####

            #---
            ##--
            ###-
            ####

            ----
            #---
            ##--
            ###-

            ----
            ----
            #---
            ##--
        ''').strip(),
    )


def test_plane_sphere_boolean():
    # Draw a sphere and slice off the top half.
    sphere = Sphere((0, 0, 0), 3)
    plane = Plane((0, 0, 0), (0, 0, 1), sphere.bounds())
    points = set(sphere.render()) - set(plane.render())

    layers = draw_layers(points, on='#', off='-')

    assert_equal(
        '\n\n'.join(layers),
        dedent('''
            --#--
            -###-
            #####
            -###-
            --#--

            -###-
            #####
            #####
            #####
            -###-
        ''').strip(),
    )


def test_parametric_torus():
    # Draw a torus using a parametric path.
    def circle(t):
        r = 1.9
        x = r * math.sin(t)
        y = r * math.cos(t)
        z = 0
        return (x, y, z)

    def radius_func(t):
        return 0.9

    torus = Path(
        circle,
        radius_func,
        tmin=0,
        tmax=(2 * math.pi),
    )

    points = torus.render()
    layers = draw_layers(points, on='#', off='-')

    assert_equal(
        '\n\n'.join(layers),
        dedent('''
            -###-
            ##-##
            #---#
            ##-##
            -###-
        ''').strip(),
    )


def test_parametric_changing_radius():
    # Draw a variable width line.
    start = Point3(0.5, 0, 0)
    end = Point3(19.5, 0, 0)

    def line(t):
        x = lerp(start.x, end.x, t)
        y = lerp(start.y, end.y, t)
        z = lerp(start.z, end.z, t)
        return (x, y, z)

    def radius_func(t):
        # Get larger until the middle, then get smaller again.
        if t < 0.5:
            return lerp(0, 3.5, t)
        else:
            return lerp(3.5, 0, t)

    path = Path(
        line,
        radius_func,
        tmin=0,
        tmax=1,
    )

    points = path.render()
    layers = draw_layers(points, on='#', off='-')

    assert_equal(
        '\n\n'.join(layers),
        dedent('''
            --------###--------
            -----#########-----
            --------###--------

            -----#########-----
            ###################
            -----#########-----

            --------###--------
            -----#########-----
            --------###--------
        ''').strip(),
    )
