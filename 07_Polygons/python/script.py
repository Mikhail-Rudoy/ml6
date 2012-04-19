from matrix import *
from screen import *
from draw import *

def run_scripts(filenames):
    edges = []
    faces = []
    transformations = new_ident_matrix(4)
    while filenames:
        commands = open(filenames[0]).readlines()
        for i in range(len(commands)):
            commands[i] = commands[i].strip()
        filenames = filenames[1:]
        for i in range(len(commands)):
            if commands[i] in "lstxyzgchbmdpMDP":
                args = commands[i + 1].split(" ")
                if commands[i] == "l":
                    add_edge_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]))
                elif commands[i] == "s":
                    transformations = matrix_multiply(new_scale_matrix(float(args[0]), float(args[1]), float(args[2])), transformations)
                elif commands[i] == "t":
                    transformations = matrix_multiply(new_translation_matrix(float(args[0]), float(args[1]), float(args[2])), transformations)
                elif commands[i] == "x":
                    transformations = matrix_multiply(new_rotationX_matrix(float(args[0])), transformations)
                elif commands[i] == "y":
                    transformations = matrix_multiply(new_rotationY_matrix(float(args[0])), transformations)
                elif commands[i] == "z":
                    transformations = matrix_multiply(new_rotationZ_matrix(float(args[0])), transformations)
                elif commands[i] == "g":
                    w, h = get_default_dimensions()
                    which = "ef"
                    if len(args) == 4:
                        which = args[3]
                    if len(args) == 2:
                        which = args[1]
                    if len(args) >= 3:
                        w = int(args[1])
                        h = int(args[2])
                    sc = new_screen(w, h)
                    facesDone = False
                    edgesDone = False
                    for c in which:
                        if c == "e" and not facesDone:
                            draw_face_matrix(faces, sc, [255, 255, 255])
                            facesDone = True
                        if c == "f" and not edgesDone:
                            draw_edge_matrix(edges, sc, [255, 255, 255])
                            edgesDone = True
                    save_screen(sc, args[0])
                    sc = []
                elif commands[i] == "c":
                    if len(args) == 3:
                        add_circle_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]))
                    else:
                        add_circle_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), int(args[3]))
                elif commands[i] == "h":
                    if len(args) == 13:
                        add_hermite_curve_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]), float(args[6]), float(args[7]), float(args[8]), float(args[9]), float(args[10]), float(args[11]), int(args[12]))
                    elif len(args) == 12:
                        add_hermite_curve_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]), float(args[6]), float(args[7]), float(args[8]), float(args[9]), float(args[10]), float(args[11]))
                    elif len(args) == 9:
                        add_hermite_curve_to_matrix(edges, float(args[0]), float(args[1]), 0, float(args[2]), float(args[3]), 0, float(args[4]), float(args[5]), 0, float(args[6]), float(args[7]), 0,  int(args[8]))
                    else:
                        add_hermite_curve_to_matrix(edges, float(args[0]), float(args[1]), 0, float(args[2]), float(args[3]), 0, float(args[4]), float(args[5]), 0, float(args[6]), float(args[7]), 0)
                elif commands[i] == "b":
                    if len(args) == 13:
                        add_bezier_curve_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]), float(args[6]), float(args[7]), float(args[8]), float(args[9]), float(args[10]), float(args[11]), int(args[12]))
                    elif len(args) == 12:
                        add_bezier_curve_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]), float(args[6]), float(args[7]), float(args[8]), float(args[9]), float(args[10]), float(args[11]))
                    elif len(args) == 9:
                        add_bezier_curve_to_matrix(edges, float(args[0]), float(args[1]), 0, float(args[2]), float(args[3]), 0, float(args[4]), float(args[5]), 0, float(args[6]), float(args[7]), 0,  int(args[8]))
                    else:
                        add_bezier_curve_to_matrix(edges, float(args[0]), float(args[1]), 0, float(args[2]), float(args[3]), 0, float(args[4]), float(args[5]), 0, float(args[6]), float(args[7]), 0)
                elif commands[i] == "m":
                    if len(args) == 4:
                        add_sphere_mesh_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]))
                    elif len(args) == 5:
                        add_sphere_mesh_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), args[4])
                    elif len(args) == 6:
                        add_sphere_mesh_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), "d", [int(args[4]), int(args[5])])
                    else:
                        add_sphere_mesh_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), args[4], [int(args[5]), int(args[6])])
                elif commands[i] == "d":
                    if len(args) == 5:
                        add_torus_mesh_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]))
                    elif len(args) == 6:
                        add_torus_mesh_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), args[5])
                    elif len(args) == 7:
                        add_torus_mesh_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), "d", [int(args[5]), int(args[6])])
                    else:
                        add_torus_mesh_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), args[5], [int(args[6]), int(args[7])])
                elif commands[i] == "p":
                    if len(args) == 6:
                        add_box_mesh_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]))
                    else:
                        add_box_mesh_to_matrix(edges, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]), [int(args[6]), int(args[7]), int(args[8])])
                elif commands[i] == "P":
                    add_polygon_box_to_matrix(faces, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]))
                elif commands[i] == "M":
                    if len(args) == 4:
                        add_polygon_sphere_to_matrix(faces, float(args[0]), float(args[1]), float(args[2]), float(args[3]))
                    else:
                        add_polygon_sphere_to_matrix(faces, float(args[0]), float(args[1]), float(args[2]), float(args[3]), [int(args[4]), int(args[5])])
                i = i + 2
            elif commands[i] == "q":
                edges = []
                faces = []
                transformations = new_ident_matrix(4)
                break;
            else:
                if commands[i] == "i":
                    transformations = new_ident_matrix(4)
                elif commands[i] == "w":
                    edges = []
                    faces = []
                elif commands[i] == "a":
                    edges = matrix_multiply(transformations, edges)
                    faces = matrix_multiply(transformations, faces)
                i = i + 1
