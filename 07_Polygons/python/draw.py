from screen import *
from matrix import *

def draw_line(screen, x0, y0, x1, y1, c):
    dx = x1 - x0
    dy = y1 - y0
    if dx + dy < 0:
        dx = 0 - dx
        dy = 0 - dy
        tmp = x0
        x0 = x1
        x1 = tmp
        tmp = y0
        y0 = y1
        y1 = tmp
    
    if dx == 0:
        y = y0
        while y <= y1:
            draw_pixel(screen, x0, y, c)
            y = y + 1
    elif dy == 0:
        x = x0
        while x <= x1:
            draw_pixel(screen, x, y0, c)
            x = x + 1
    elif dy < 0:
        d = 0
        x = x0
        y = y0
        while x <= x1:
            draw_pixel(screen, x, y, c)
            if d > 0:
                y = y - 1
                d = d - dx
            x = x + 1
            d = d - dy
    elif dx < 0:
        d = 0
        x = x0
        y = y0
        while y <= y1:
            draw_pixel(screen, x, y, c)
            if d > 0:
                x = x - 1
                d = d - dy
            y = y + 1
            d = d - dx
    elif dx > dy:
        d = 0
        x = x0
        y = y0
        while x <= x1:
            draw_pixel(screen, x, y, c)
            if d > 0:
                y = y + 1
                d = d - dx
            x = x + 1
            d = d + dy
    else:
        d = 0
        x = x0
        y = y0
        while y <= y1:
            draw_pixel(screen, x, y, c)
            if d > 0:
                x = x + 1
                d = d - dy
            y = y + 1
            d = d + dx

def draw_edge_matrix(matrix, screen, c):
    i = 0
    while i < get_width(matrix) - 1:
        x0 = get_element(matrix, 0, i)
        y0 = get_element(matrix, 1, i)
        x1 = get_element(matrix, 0, i + 1)
        y1 = get_element(matrix, 1, i + 1)
        draw_line(screen, int(x0), int(y0), int(x1), int(y1), c)
        i = i + 2


def draw_face_matrix(matrix, screen, c):
    i = 0
    while i < get_width(matrix) - 2:
        x0 = get_element(matrix, 0, i)
        y0 = get_element(matrix, 1, i)
        x1 = get_element(matrix, 0, i + 1)
        y1 = get_element(matrix, 1, i + 1)
        x2 = get_element(matrix, 0, i + 2)
        y2 = get_element(matrix, 1, i + 2)
        draw_line(screen, int(x0), int(y0), int(x1), int(y1), c)
        draw_line(screen, int(x0), int(y0), int(x2), int(y2), c)
        draw_line(screen, int(x2), int(y2), int(x1), int(y1), c)
        i = i + 3
