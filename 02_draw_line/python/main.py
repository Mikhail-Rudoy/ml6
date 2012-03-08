from screen import *

sc = new_screen(256, 256)
for x in range(32):
    for y in range(32):
        draw_line(sc, 128, 128, 8 * x, 8 * y, [255, 0, 0])

save_screen(sc, "pic.ppm")
