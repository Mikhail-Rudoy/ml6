from screen import *

sc = new_screen(256, 256)
for x in range(256):
    for y in range(256):
        sc[x][y][0] = x
        sc[x][y][1] = y
        sc[x][y][2] = 0
        if x > 128:
            sc[x][y][2] = sc[x][y][2] + x - 128
        else:
            sc[x][y][2] = sc[x][y][2] + 128 - x
        if y > 128:
            sc[x][y][2] = sc[x][y][2] + y - 128
        else:
            sc[x][y][2] = sc[x][y][2] + 128 - y

sc[50][50] = [0, 0, 0]

save_screen(sc, "pic.ppm")
