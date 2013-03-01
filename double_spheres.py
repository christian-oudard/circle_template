from volume import draw_layers, Sphere

a = Sphere((0, 0, 0), 10)
b = Sphere((5, 5, 5), 10)

points = set(a.render()) | set(b.render())

sep = '-' * 80
print(sep)
for layer in draw_layers(points):
    print(layer)
    print(sep)

print(len(points))
