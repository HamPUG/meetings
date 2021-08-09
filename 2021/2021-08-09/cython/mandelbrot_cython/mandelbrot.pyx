from datetime import datetime
import numpy as np
from PIL import Image
from colour import Color


def calculate(cx, cy, max_iter):
    zx = 0
    zy = 0
    i = 0
    while (i < max_iter):
        i += 1
        zx_new = zx*zx - zy*zy + cx
        zy_new = 2*zx*zy + cy
        zx = zx_new
        zy = zy_new
        if (zx*zx + zy*zy > max_value):
            break
    return i


start = datetime.now()

colors = list(Color("white").range_to(Color("blue"), 255))
palette = [0, 0, 0]
for color in colors:
    palette.append(int(color.red * 255))
    palette.append(int(color.green * 255))
    palette.append(int(color.blue * 255))

width = 800
height = 600
max_iter = 100
max_value = 16*16
mat = np.zeros((height, width))

xmin = -2.5
xmax = +1.5
ymin = -1.5
ymax = +1.5

xinc = (xmax - xmin) / (width - 1)
yinc = (ymax - ymin) / (height - 1)

for y in range(height):
    cy = ymin + y * yinc

    for x in range(width):
        cx = xmin + x * xinc
        i = calculate(cx, cy, max_iter)
        if i == max_iter:
            mat[y][x] = 0
        else:
            mat[y][x] = i % 255 + 1

img = Image.fromarray(np.uint8(mat * 255), 'P')
img.putpalette(palette)
img.save("mandelbrot.png")

end = datetime.now()
print(end.timestamp() - start.timestamp())

