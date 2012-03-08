from screen import *

sc = new_screen(600, 600)
for x in range(75):
    for y in range(75):
        draw_line(sc, 128, 128, 4 + 8 * x, 4 + 8 * y, [255, 0, 0])

save_screen(sc, "pic.ppm")
