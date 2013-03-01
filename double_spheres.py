from volume import draw_layers, Sphere

volumes = [
    Sphere((0, 0, 0), 10),
    Sphere((5, 5, 5), 10),
]

sep = '-' * 80
print(sep)
for layer in draw_layers(volumes):
    print(layer)
    print(sep)
