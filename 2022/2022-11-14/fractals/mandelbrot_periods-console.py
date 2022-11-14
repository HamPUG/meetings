# Output modulo 10 of iteration that marked escaped.

cx = [-2.5, 1.5]
cy = [-1.5, 1.5]
points_x = 80
points_y = 60
dx = (cx[1] - cx[0]) / points_x
dy = (cy[1] - cy[0]) / points_y
max_iter = 1000

for y in range(points_y):
    for x in range(points_x):
        z = 0+0j
        c = complex((cx[0] + x*dx), (cy[0] + y*dy))
        v = set()
        v.add(z)
        p = set()
        escaped = False
        period = False
        for i in range(max_iter):
            zn = z**2 + c
            if zn in v:
                if zn in p:
                    period = True
                    print(str(len(p) % 10), end="")
                    break
                else:
                    p.add(zn)
            if abs(zn) > 2:
                escaped = True
                break
            v.add(zn)
            z = zn
        if not period:
            print(" ", end="")
    print()
