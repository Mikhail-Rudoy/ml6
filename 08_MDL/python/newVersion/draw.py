from screen import *
from matrix import *
from vect import *

def draw_edge_matrix(matrix, screen, c):
    i = 0
    while i < get_width(matrix) - 1:
        x0 = get_element(matrix, 0, i)
        y0 = get_element(matrix, 1, i)
        x1 = get_element(matrix, 0, i + 1)
        y1 = get_element(matrix, 1, i + 1)
        draw_line(screen, int(x0), int(y0), int(x1), int(y1), c)
        i = i + 2


def draw_face_matrix(matrix, screen, c, view = [0, 0, -1]):
    i = 0
    while i < get_width(matrix) - 2:
        x0 = get_element(matrix, 0, i)
        y0 = get_element(matrix, 1, i)
        z0 = get_element(matrix, 2, i)
        x1 = get_element(matrix, 0, i + 1)
        y1 = get_element(matrix, 1, i + 1)
        z1 = get_element(matrix, 2, i + 1)
        x2 = get_element(matrix, 0, i + 2)
        y2 = get_element(matrix, 1, i + 2)
        z2 = get_element(matrix, 2, i + 2)
        if dot(cross(vec([x0, y0, z0], [x1, y1, z1]), vec([x0, y0, z0], [x2, y2, z2])), view) > 0:
            draw_line(screen, int(x0), int(y0), int(x1), int(y1), c)
            draw_line(screen, int(x0), int(y0), int(x2), int(y2), c)
            draw_line(screen, int(x2), int(y2), int(x1), int(y1), c)
        i = i + 3
