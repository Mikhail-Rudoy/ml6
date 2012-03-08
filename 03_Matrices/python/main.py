from matrix import *
from screen import *

sc = new_screen(500, 500)

edges = []
edges = add_edge_to_matrix(edges, 100, 200, 0, 200, 200, 0)
draw_edge_matrix(edges, sc, [0, 255, 0])

save_screen(sc, "pic.ppm")
