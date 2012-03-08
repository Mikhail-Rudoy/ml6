from screen import *

sc = new_screen(600, 600)
for x in range(75):
    for y in range(75):
        draw_line(sc, 300, 300, 4 + 8 * x, 4 + 8 * y, [255, 0, 0])
draw_line(sc, 50, 50, 550, 50, [0, 255, 0])
save_screen(sc, "pic.ppm")
