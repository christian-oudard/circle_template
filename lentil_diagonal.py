from volume import Sphere, volume_list_bounds, points_in_bounds, render, draw_layers

a = Sphere((0, 0, 0), 10)
b = Sphere((5, 5, 5), 10)

bounds = volume_list_bounds([a, b])
field = set(points_in_bounds(bounds))

points = set(render(a)) & set(render(b))

sep = '-' * 80
print(sep)
for layer in draw_layers(points):
    print(layer)
    print(sep)
