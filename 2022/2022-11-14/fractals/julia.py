import numpy as np
from PIL import Image


def calculate(c, max_iter=100):
    zx = [-2.0, 2.0]
    zy = [-1.5, 1.5]
    points_x = 800
    points_y = 600
    dx = (zx[1] - zx[0]) / points_x
    dy = (zy[1] - zy[0]) / points_y

    julia = np.zeros((points_y, points_x), dtype=np.uint8)

    for y in range(points_y):
        for x in range(points_x):
            z = complex((zx[0] + x*dx), (zy[0] + y*dy))
            for i in range(max_iter):
                zn = z**2 + c
                if abs(zn) > 2:
                    julia[y][x] = (i % 16) * 16 + 15
                    break
                z = zn

    img = Image.fromarray(julia)
    img.show()


calculate(0+1j, max_iter=1000)
