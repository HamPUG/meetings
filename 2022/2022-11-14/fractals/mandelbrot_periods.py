# detect loops and use loop for color (16 gray scale)

from PIL import Image
import numpy as np
import matplotlib

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
        v = set()
        v.add(z)
        p = set()
        escaped = False
        for i in range(max_iter):
            zn = z**2 + c
            # encountered value before?
            if zn in v:
                # found a period?
                if zn in p:
                    mandelbrot[y][x] = (len(p) % 16) * 16 + 15
                    break
                else:
                    p.add(zn)
            if abs(zn) > 2:
                escaped = True
                break
            v.add(zn)
            z = zn

img = Image.fromarray(mandelbrot)
img.show()
