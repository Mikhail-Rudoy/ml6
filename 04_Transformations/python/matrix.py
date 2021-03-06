from screen import *

def new_matrix(w, h):
    result = []
    for i in range(w):
        result.append([])
        for j in range(h):
            result[i].append(0)
    return result

def get_element(matrix, r, c):
    return matrix[c][r]

def set_element(matrix, r, c, v):
    matrix[c][r] = v

def get_width(matrix):
    return len(matrix)

def get_height(matrix):
    return len(matrix[0])

def copy_matrix(matrix):
    result = []
    for col in matrix:
        result.append(col[:])
    return result

def print_matrix(matrix):
    l = ""
    for r in range(get_height(matrix)):
        for c in range(get_width(matrix)):
            l = l + str(get_element(matrix, r, c)) + " "
        l = l + "\n"
    print l

def new_ident_matrix(d):
    result = []
    for i in range(d):
        result.append([])
        for j in range(d):
            if i == j:
                result[i].append(1.0)
            else:
                result[i].append(0.0)
    return result

def scalar_multiply(matrix, n):
    matrix = copy_matrix(matrix)
    for c in range(get_width(matrix)):
        for r in range(get_height(matrix)):
            set_element(matrix, r, c, n * get_element(matrix, r, c))
    return matrix

def matrix_multiply(A, B):
    C = new_matrix(get_width(B), get_height(A))
    for r in range(get_height(C)):
        for c in range(get_width(C)):
            v = 0
            i = 0
            while i < get_width(A) and i < get_height(B):
                v = v + get_element(A, r, i) * get_element(B, i, c)
                i = i + 1
            set_element(C, r, c, v)
    return C

def add_point_to_matrix(matrix, x, y, z):
    matrix.append([x, y, z, 1])
    return matrix

def add_edge_to_matrix(matrix, x0, y0, z0, x1, y1, z1):
    return add_point_to_matrix(add_point_to_matrix(matrix, x0, y0, z0), x1, y1, z1)

def draw_edge_matrix(matrix, screen, c):
    i = 0
    while i < get_width(matrix) - 1:
        x0 = get_element(matrix, 0, i)
        y0 = get_element(matrix, 1, i)
        x1 = get_element(matrix, 0, i + 1)
        y1 = get_element(matrix, 1, i + 1)
        draw_line(screen, x0, y0, x1, y1, c)
        i = i + 2

def new_translation_matrix(a, b, c):
    return [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [a, b, c, 1.0]]

def new_scale_matrix(a, b, c):
    return [[a, 0.0, 0.0, 0.0], [0.0, b, 0.0, 0.0], [0.0, 0.0, c, 0.0], [0.0, 0.0, 0.0, 1.0]]

def new_rotationX_matrix(theta):
    r = theta * 3.14159265358979323 / 180
    return [[1.0, 0.0, 0.0, 0.0], [0.0, math.cos(r), math.sin(r), 0.0], [0.0, 0.0 - math.sin(r), math.cos(r), 0.0], [0.0, 0.0, 0.0, 1.0]]

def new_rotationY_matrix(theta):
    r = theta * 3.14159265358979323 / 180
    return [[math.cos(r), 0.0, math.sin(r), 0.0], [0.0, 1.0, 0.0, 0.0], [0.0 - math.sin(r), 0.0, math.cos(r), 0.0], [0.0, 0.0, 0.0, 1.0]]

def new_rotationZ_matrix(theta):
    r = theta * 3.14159265358979323 / 180
    return [[math.cos(r), math.sin(r), 0.0, 0.0], [0.0 - math.sin(r), math.cos(r), 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]

