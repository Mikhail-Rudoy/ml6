from matrix import *
from screen import *

sc = new_screen(600, 600)

edges = []
edges = add_edge_to_matrix(edges, 100, 200, 0, 200, 200, 0)
edges = add_edge_to_matrix(edges, 200, 200, 0, 200, 100, 0)
edges = add_edge_to_matrix(edges, 200, 100, 0, 100, 100, 0)
edges = add_edge_to_matrix(edges, 100, 100, 0, 100, 200, 0)
edges = add_edge_to_matrix(edges, 500, 500, 0, 400, 400, 0)
edges = add_edge_to_matrix(edges, 400, 500, 0, 500, 400, 0)

draw_edge_matrix(edges, sc, [0, 255, 0])

A = new_ident_matrix(4)
B = new_matrix(4, 4)
C = copy_matrix(B)
D = copy_matrix(B)
E = copy_matrix(B)

for i in range(4):
    for j in range(4):
        set_element(B, i, j, ((i - 2.5) * (i - 2.5) * (3 * j * j * j - 1)))
        set_element(C, i, j, (i + j + 3))
        set_element(D, i, j, (100 - i * j / 0.3))
        set_element(E, i, j, (4 * i + j))

print "Matrix A set as an identity matrix"
print_matrix(A)
print "Matrix B set by hand"
print_matrix(B)
print "A*B="
print_matrix(matrix_multiply(A, B))
print "B*A="
print_matrix(matrix_multiply(B, A))
print "Matrix C set by hand"
print_matrix(C)
print "Matrix D set by hand"
print_matrix(D)
print "C*D="
print_matrix(matrix_multiply(C, D))
print "Matrix E set by hand"
print_matrix(E)
print "2*E="
print_matrix(scalar_multiply(E, 2))


save_screen(sc, "pic.ppm")
