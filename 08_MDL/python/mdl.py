import lex

tokens = ("STRING", "ID", "DOUBLE", "COMMENT", "LIGHT", "CONSTANTS", "SAVE_COORDS", "CAMERA", "AMBIENT", "TORUS", "SPHERE", "BOX", "LINE", "MESH", "TEXTURE", "SET", "MOVE", "SCALE", "ROTATE", "BASENAME", "SAVE_KNOBS", "TWEEN", "FRAMES", "VARY", "PUSH", "POP", "SAVE", "GENERATE_RAYFILES", "SHADING", "SHADING_TYPE", "SET_KNOBS", "FOCAL", "WEB", "CO")

reserved = {
    "light" : "LIGHT",
    "constants" : "CONSTANTS",
    "save_coord_system" : "SAVE_COORDS", 
    "camera" : "CAMERA", 
    "ambient" : "AMBIENT", 
    "torus" : "TORUS", 
    "sphere" : "SPHERE", 
    "box" : "BOX", 
    "line" : "LINE", 
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
    "web" : "WEB"
}

t_ignore = " \t"

def t_STRING(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*\.[a-zA-Z_0-9]*"
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if reserved.has_key(t.value):
        t.type = reserved.get(t.value)
    return t

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
lex.input(r"mesh generate_rayfiles thing.ppm //the rest is a comment")
while 1:
    tok = lex.token()
    if not tok:
        break
    print tok

