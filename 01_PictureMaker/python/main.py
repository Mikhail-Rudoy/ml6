from screen import *

sc = new_screen(256, 256)
for x in range(256):
    for y in range(256):
        tmp = [x, y, 0]
        if x > 128:
            tmp[2] = tmp[2] + x - 128
        else:
            tmp[2] = tmp[2] + 128 - x
        if y > 128:
            tmp[2] = tmp[2] + y - 128
        else:
            tmp[2] = tmp[2] + 128 - y
        draw_pixel(sc, x, y, tmp)

save_screen(sc, "pic.ppm")
