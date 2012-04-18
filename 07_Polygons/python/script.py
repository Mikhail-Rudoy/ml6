from matrix import *
from screen import *
from draw import *

def run_scripts(filenames):
    edges = []
    transformations = new_ident_matrix(4)
    while filenames:
        commands = open(filenames[0]).readlines()
        for i in range(len(commands)):
            commands[i] = commands[i].strip()
        filenames = filenames[1:]
        while commands:
            if commands[0] in "lstxyzgchbmdp":
                args = commands[1].split(" ")
                if commands[0] == "l":
                    add_edge_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]))
                elif commands[0] == "s":
                    transformations = matrix_multiply(new_scale_matrix(float(args[0]), float(args[1]), float(args[2])), transformations)
                elif commands[0] == "t":
                    transformations = matrix_multiply(new_translation_matrix(float(args[0]), float(args[1]), float(args[2])), transformations)
                elif commands[0] == "x":
                    transformations = matrix_multiply(new_rotationX_matrix(float(args[0])), transformations)
                elif commands[0] == "y":
                    transformations = matrix_multiply(new_rotationY_matrix(float(args[0])), transformations)
                elif commands[0] == "z":
                    transformations = matrix_multiply(new_rotationZ_matrix(float(args[0])), transformations)
                elif commands[0] == "g":
                    w, h = get_default_dimensions()
                    if len(args) == 3:
                        w = int(args[1])
                        h = int(args[2])
                    sc = new_screen(w, h)
                    draw_edge_matrix(edges, sc, [255, 255, 255])
                    save_screen(sc, args[0])
                    sc = []
                elif commands[0] == "c":
                    if len(args) == 3:
                        add_circle_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]))
                    else:
                        add_circle_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), int(args[3]))
                elif commands[0] == "h":
                    if len(args) == 13:
                        add_hermite_curve_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]), float(args[6]), float(args[7]), float(args[8]), float(args[9]), float(args[10]), float(args[11]), int(args[12]))
                    elif len(args) == 12:
                        add_hermite_curve_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]), float(args[6]), float(args[7]), float(args[8]), float(args[9]), float(args[10]), float(args[11]))
                    elif len(args) == 9:
                        add_hermite_curve_to_matrix(edges, float(args[0]), float(args[1]), 0, float(args[2]), float(args[3]), 0, float(args[4]), float(args[5]), 0, float(args[6]), float(args[7]), 0,  int(args[8]))
                    else:
                        add_hermite_curve_to_matrix(edges, float(args[0]), float(args[1]), 0, float(args[2]), float(args[3]), 0, float(args[4]), float(args[5]), 0, float(args[6]), float(args[7]), 0)
                elif commands[0] == "b":
                    if len(args) == 13:
                        add_bezier_curve_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]), float(args[6]), float(args[7]), float(args[8]), float(args[9]), float(args[10]), float(args[11]), int(args[12]))
                    elif len(args) == 12:
                        add_bezier_curve_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]), float(args[6]), float(args[7]), float(args[8]), float(args[9]), float(args[10]), float(args[11]))
                    elif len(args) == 9:
                        add_bezier_curve_to_matrix(edges, float(args[0]), float(args[1]), 0, float(args[2]), float(args[3]), 0, float(args[4]), float(args[5]), 0, float(args[6]), float(args[7]), 0,  int(args[8]))
                    else:
                        add_bezier_curve_to_matrix(edges, float(args[0]), float(args[1]), 0, float(args[2]), float(args[3]), 0, float(args[4]), float(args[5]), 0, float(args[6]), float(args[7]), 0)
                elif commands[0] == "m":
                    if len(args) == 4:
                        add_sphere_mesh_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]))
                    elif len(args) == 5:
                        add_sphere_mesh_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), args[4])
                    elif len(args) == 6:
                        add_sphere_mesh_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), "d", [int(args[4]), int(args[5])])
                    else:
                        add_sphere_mesh_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), args[4], [int(args[5]), int(args[6])])
                elif commands[0] == "d":
                    if len(args) == 5:
                        add_torus_mesh_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]))
                    elif len(args) == 6:
                        add_torus_mesh_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), args[5])
                    elif len(args) == 7:
                        add_torus_mesh_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), "d", [int(args[5]), int(args[6])])
                    else:
                        add_torus_mesh_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), args[5], [int(args[6]), int(args[7])])
                elif commands[0] == "p":
                    if len(args) == 6:
                        add_box_mesh_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]))
                    else:
                        add_box_mesh_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]), [int(args[6]), int(args[7]), int(args[8])])
                commands = commands[2:]
            elif commands[0] == "q":
                edges = []
                transformations = new_ident_matrix(4)
                commands = []
            else:
                if commands[0] == "i":
                    transformations = new_ident_matrix(4)
                elif commands[0] == "w":
                    edges = []
                elif commands[0] == "a":
                    edges = matrix_multiply(transformations, edges)
                commands = commands[1:]
