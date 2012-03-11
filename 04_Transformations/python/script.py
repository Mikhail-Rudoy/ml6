from matrix import *
from screen import *

def run_scripts(filenames):
    edges = []
    transformations = new_ident_matrix(4)
    while filenames:
        commands = open(filenames[0]).readlines()
        for i in range(len(commands)):
            commands[i] = commands[i].strip()
        filenames = filenames[1:]
        while commands:
            if commands[0] in "lstxyzg":
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
                commands = commands[2:]
            elif commands[0] == "q":
                edges = []
                transformations = new_ident_matrix(4)
                commands = []
            else:
                if commands[0] == "i":
                    transformations = new_ident_matrix(4)
                elif commands[0] == "a":
                    edges = matrix_multiply(transformations, edges)
                commands = commands[1:]
