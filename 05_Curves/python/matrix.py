from screen import *
import math

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

def draw_circle(matrix, cx, cy, r, STEPS = 500):
    for n in range(STEPS + 1):
        t0 = n / STEPS
        t1 = (n + 1) / STEPS
        [x0, y0] = [cx + r * math.cos(math.pi * 2 * t0), cy + r * math.sin(math.pi * 2 * t0)]
        [x1, y1] = [cx + r * math.cos(math.pi * 2 * t1), cy + r * math.sin(math.pi * 2 * t1)]
        add_edge_to_matrix(matrix, x0, y0, 0, x1, y1, 0)

def draw_hermite_curve(matrix, x0, y0, z0, x1, y1, z1, x2, y2, z2, x3, y3, z3 STEPS = 500):
    for n in range(STEPS):
        t0 = n / STEPS
        t1 = (n + 1) / STEPS
        [[ax, bx, cx, dx], [ay, by, cy, dy], [az, bz, cz, dz]] = matrix_multiply([[3, -2, 0, 1], [-2, 3, 0, 0], [1, -2, 1, 0], [1, 1, 0, 0]], [[x0, x2, x1 - x0, x3 - x2], [y0, y2, y1 - y0, y3 - y2], [z0, z2, z1 - z0, z3 - z2]])
        x0 = ax * t0 * t0 * t0 + bx * t0 * t0 + cx * t0 + dx
        y0 = ay * t0 * t0 * t0 + by * t0 * t0 + cy * t0 + dy
        z0 = az * t0 * t0 * t0 + bz * t0 * t0 + cz * t0 + dz
        x1 = ax * t1 * t1 * t1 + bx * t1 * t1 + cx * t1 + dx
        y1 = ay * t1 * t1 * t1 + by * t1 * t1 + cy * t1 + dy
        z1 = az * t1 * t1 * t1 + bz * t1 * t1 + cz * t1 + dz
        add_edge_to_matrix(matrix, x0, y0, z0, x1, y1, z1)

def draw_bezier_curve(matrix, x0, y0, z0, x1, y1, z1, x2, y2, z2, x3, y3, z3 STEPS = 500):
    for n in range(STEPS):
        t0 = n / STEPS
        t1 = (n + 1) / STEPS
        [[ax, bx, cx, dx], [ay, by, cy, dy], [az, bz, cz, dz]] = matrix_multiply([[1, -3, 3, -1], [0, 3, -6, 3], [0, 0, 3, -3], [0, 0, 0, 1]], [[x0, x1, x2, x3], [y0, y1, y2, y3], [z0, z1, z2, z3]])
        x0 = ax * t0 * t0 * t0 + bx * t0 * t0 + cx * t0 + dx
        y0 = ay * t0 * t0 * t0 + by * t0 * t0 + cy * t0 + dy
        z0 = az * t0 * t0 * t0 + bz * t0 * t0 + cz * t0 + dz
        x1 = ax * t1 * t1 * t1 + bx * t1 * t1 + cx * t1 + dx
        y1 = ay * t1 * t1 * t1 + by * t1 * t1 + cy * t1 + dy
        z1 = az * t1 * t1 * t1 + bz * t1 * t1 + cz * t1 + dz
        add_edge_to_matrix(matrix, x0, y0, z0, x1, y1, z1)
