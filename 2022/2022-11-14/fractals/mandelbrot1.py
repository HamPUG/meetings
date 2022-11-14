# Output "." if escaped otherwise blank

cx = [-2.5, 1.5]
cy = [-1.5, 1.5]
points_x = 80
points_y = 60
dx = (cx[1] - cx[0]) / points_x
dy = (cy[1] - cy[0]) / points_y
max_iter = 100

for y in range(points_y):
    for x in range(points_x):
        z = 0+0j
        c = complex((cx[0] + x*dx), (cy[0] + y*dy))
        escaped = False
        for i in range(max_iter):
            zn = z**2 + c
            if abs(zn) > 2:
                escaped = True
                print(".", end="")
                break
            z = zn
        if not escaped:
            print(" ", end="")
    print()
