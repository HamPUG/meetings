# Use 16 gray values.

from PIL import Image
import numpy as np

cx = [-2.5, 1.5]
cy = [-1.5, 1.5]
points_x = 800
points_y = 600
dx = (cx[1] - cx[0]) / points_x
dy = (cy[1] - cy[0]) / points_y
max_iter = 1000

mandelbrot = np.zeros((points_y, points_x), dtype=np.uint8)

for y in range(points_y):
    for x in range(points_x):
        z = 0+0j
        c = complex((cx[0] + x*dx), (cy[0] + y*dy))
        escaped = False
        for i in range(max_iter):
            zn = z**2 + c
            if abs(zn) > 2:
                escaped = True
                mandelbrot[y][x] = (i % 16) * 16 + 15
                break
            z = zn

img = Image.fromarray(mandelbrot)
img.show()