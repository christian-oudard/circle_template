from nose.tools import assert_equal

import math
from textwrap import dedent

from volume import Sphere, render, draw_layers

def test_volume():
    # Draw connected spheres, which are small enough to just be 8 points in a 2x2x2 cube.
    a = Sphere((0.5, 0.5, 0.5), 1)
    b = Sphere((-0.5, -0.5, -0.5), 1)
    points = set(render(a)) | set(render(b))
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
