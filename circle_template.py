import math

radius = 2
radius2 = radius**2
center = (1.5, 1.5)

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
print(circle_points)
