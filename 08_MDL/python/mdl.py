import lex, yacc

tokens = (
    "STRING", 
    "ID", 
    "XYZ", 
    "DOUBLE", 
    "INT", 
    "COMMENT", 
    "LIGHT", 
    "CONSTANTS", 
    "SAVE_COORDS", 
    "CAMERA", 
    "AMBIENT", 
    "TORUS", 
    "SPHERE", 
    "BOX", 
    "LINE", 
    "BEZIER", 
    "HERMITE", 
    "MESH", 
    "TEXTURE", 
    "SET", 
    "MOVE", 
    "SCALE", 
    "ROTATE", 
    "BASENAME", 
    "SAVE_KNOBS", 
    "TWEEN", 
    "FRAMES", 
    "VARY", 
    "PUSH", 
    "POP", 
    "SAVE", 
    "GENERATE_RAYFILES", 
    "SHADING", 
    "SHADING_TYPE", 
    "SET_KNOBS", 
    "FOCAL", 
    "DISPLAY", 
    "WEB", 
    "CO"
)

reserved = {
    "x" : "XYZ", 
    "y" : "XYZ", 
    "z" : "XYZ", 
    "light" : "LIGHT",
    "constants" : "CONSTANTS",
    "save_coord_system" : "SAVE_COORDS", 
    "camera" : "CAMERA", 
    "ambient" : "AMBIENT", 
    "torus" : "TORUS", 
    "sphere" : "SPHERE", 
    "box" : "BOX", 
    "line" : "LINE", 
    "bezier" : "BEZIER", 
    "hermite" : "HERMITE", 
    "mesh" : "MESH", 
    "texture" : "TEXTURE", 
    "set" : "SET", 
    "move" : "MOVE", 
    "scale" : "SCALE", 
    "rotate" : "ROTATE", 
    "basename" : "BASENAME", 
    "save_knobs" : "SAVE_KNOBS", 
    "tween" : "TWEEN", 
    "frames" : "FRAMES", 
    "vary" : "VARY", 
    "push" : "PUSH", 
    "pop" : "POP", 
    "save" : "SAVE", 
    "generate_rayfiles" : "GENERATE_RAYFILES", 
    "shading" : "SHADING", 
    "phong" : "SHADING_TYPE", 
    "flat" : "SHADING_TYPE", 
    "ground" : "SHADING_TYPE", 
    "raytrace" : "SHADING_TYPE", 
    "wireframe" : "SHADING_TYPE", 
    "set_knobs" : "SET_KNOBS", 
    "focal" : "FOCAL", 
    "display" : "DISPLAY", 
    "web" : "WEB"
}

t_ignore = " \t"

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if reserved.has_key(t.value):
        t.type = reserved.get(t.value)
    return t

def t_STRING(t):
    r"[a-zA-Z_0-9\.]+"
    return t

def t_INT(t):
    r"\-?\d+"
    t.value = int(t.value)

def t_DOUBLE(t):
    r"\-?\d+\.?\d*|\-?\.\d*"
    t.value = float(t.value)
    return t

def t_COMMENT(t):
    r"//.*"
    return t

def t_CO(t):
    r":"
    return t

lex.lex()

#----------------------------------------------------------

commands = []
symbols = {}

def p_line(p):
    """line : 
            | statement line
            | statement"""
    pass

def p_SYMBOL(p):
    """SYMBOL : XYZ
              | ID"""
    p[0] = p[1]

def p_TEXT(p):
    """TEXT : SYMBOL
            | STRING"""
    p[0] = p[1]

def p_NUMBER(p):
    """NUMBER : DOUBLE
              | INT"""
    p[0] = p[1]

def p_statement_comment(p):
    'statement : COMMENT'
    print len(p)

def p_statement_stack(p):
    """statement : POP
                 | PUSH"""
    commmands.append((p[1]))

def p_satement_save(p):
    """statement : SAVE TEXT
                 | SAVE TEXT INT INT"""
    if len(p) == 3:
        commands.append((p[1], p[2], 500, 500))
    else:
        commands.append((p[1], p[2], p[3], p[4]))

def p_statement_show(p):
    "statement : DISPLAY TEXT"
    commands.append((p[1], p[2]))

def p_statement_knobs(p):
    """statement : SET SYMBOL NUMBER
                 | SET_KNOBS NUMBER"""
    commands.append(tuple(p[1:]))

def p_statement_sphere(p):
    """statement : SPHERE NUMBER NUMBER NUMBER NUMBER
                 | SPHERE NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER"""
    if len(p) == 6:
        commands.append((p[1], p[2], p[3], p[4], p[5], None))
    else:
        commands.append((p[1], p[2], p[3], p[4], p[5], [p[6], p[7]]))

def p_statement_torus(p):
    """statement : TORUS NUMBER NUMBER NUMBER NUMBER NUMBER
                 | TORUS NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER"""
    if len(p) == 6:
        commands.append((p[1], p[2], p[3], p[4], p[5], p[6], None))
    else:
        commands.append((p[1], p[2], p[3], p[4], p[5], p[6], [p[7], p[8]]))

def p_statement_box(p):
    "statement : BOX NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER"
    commands.append(tuple(p[1:]))

def p_statement_line(p):
    "statement : LINE NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER"
    commands.append(tuple(p[1:]))

def p_statement_curve(p):
    """statement : BEZIER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER
                 | BEZIER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER
                 | HERMITE NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER
                 | HERMITE NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER"""
    if len(p) == 14:
        commands.append(tuple(p[1:] + [80]))
    else:
        commands.append(tuple(p[1:]))

def p_statement_move(p):
    """statement : MOVE NUMBER NUMBER NUMBER
                 | MOVE NUMBER NUMBER NUMBER SYMBOL"""
    if len(p) == 5:
        commands.append(tuple(p[1:] + [None]))
    else:
        commands.append(tuple(p[1:]))
        symbols[p[5]] = 0

def p_statement_scale(p):
    """statement : SCALE NUMBER NUMBER NUMBER
                 | SCALE NUMBER NUMBER NUMBER SYMBOL"""
    if len(p) == 5:
        commands.append(tuple(p[1:] + [None]))
    else:
        commands.append(tuple(p[1:]))
        symbols[p[5]] = 0

def p_statement_rotate(p):
    """statement : ROTATE XYZ NUMBER
                 | ROTATE XYZ NUMBER SYMBOL"""
    if len(p) == 4:
        commands.append(tuple(p[1:] + [None]))
    else:
        commands.append(tuple(p[1:]))
        symbols[p[5]] = 0

yacc.yacc()

def parseFile(filename):
    try:
        f = open(filename, "r")
        for line in f.readlines():
            yacc.parse(line)
        f.close()
    except IOError:
        return -1
