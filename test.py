from nose.tools import assert_equal

import math
from textwrap import dedent

from volume import Sphere, draw_layers

def test_volume():
    # Draw connected spheres, which are small enough to just be 8 points in a 2x2x2 cube.
    volumes = [
        Sphere((0.5, 0.5, 0.5), 1),
        Sphere((-0.5, -0.5, -0.5), 1),
    ]
    layers = draw_layers(volumes, on='#', off='-')

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
