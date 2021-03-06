import math, mdl, matrix, screen, os, sys

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)
    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return
    
    arc = {}
    arc["display"] = []
    arc["save"] = []
    arc["screen"] = []
    arc["vary"] = []
    arc["basename"] = []
    arc["frames"] = []
    arc["tween"] = []
    arc["save_knobs"] = []
    
    for command in commands:
        if arc.has_key(command[0]):
            arc[command[0]].append(command)
    if not arc["basename"] and not arc["vary"] and not arc["frames"] and not arc["tween"]:
        knobs = {}
        constants = {}
        coord_systems = {}
        meshesE = {}
        meshesF = {}
        for s in symbols:
            if s[0] == "knob":
                knobs[s[1]] = 1.0
            if s[0] == "constants":
                constants[s[1]] = [255, 255, 255, 200, 200, 200, 100, 100, 100, 0, 0, 0]
            if s[0] == "coord_system":
                coord_systems[s[1]] = matrix.ident()
            if s[0] == "mesh":            
                try:
                    meshFile = open(s[1])
                    line1 = meshFile.readline().strip()
                    if line1 not in ["edges", "faces"]:
                        meshFile.close()
                        continue
                    if line1 == "edges" and not meshesE.has_key(s[1]):
                        m = matrix.EdgeMatrix()
                        for line in meshFile.readlines():
                            line = line.strip()
                            vals = [float(x) for x in line.split(" ")]
                            m.add_edge(*vals)
                            meshesE[s[1]] = m
                    elif line1 == "faces" and not meshesF.has_key(s[1]):
                        m = matrix.FaceMatrix()
                        for line in meshFile.readlines():
                            line = line.strip()
                            vals = [float(x) for x in line.split(" ")]
                            m.add_face(*vals)
                            meshesF[s[1]] = m
                    meshFile.close()
                except:
                    pass
        for command in arc["save_knobs"]:
            command[0] = "ignore"
        while 1:
            knobs = getKnobValues(knobs)
            runCommands(commands, knobs, constants, coord_systems, meshesE, meshesF, matrix.ident(), 0)
            while 1:
                text = raw_input("Continue?\n> ")
                if not text in ["yes", "no", "n", "y"]:
                    print "I don't understand."
                elif text in ["yes", "y"]:
                    print
                    break
                else:
                    return
    
    for command in arc["display"]:
        command[0] = "ignore"
        
    for command in arc["save"]:
        command[0] = "ignore"
        
    for command in arc["screen"]:
        command[0] = "ignore"

    knobs = {}
    constants = {}
    coord_systems = {}
    knoblists = {}
    meshesE = {}
    meshesF = {}
    for s in symbols:
        if s[0] == "knob" and not knobs.has_key(s[1]):
            knobs[s[1]] = []
        if s[0] == "constants" and not constants.has_key(s[1]):
            constants[s[1]] = [255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if s[0] == "coord_system" and not coord_systems.has_key(s[1]):
            coord_systems[s[1]] = matrix.ident()
        if s[0] == "mesh":
            try:
                meshFile = open(s[1])
                line1 = meshFile.readline().strip()
                if line1 not in ["edges", "faces"]:
                    meshFile.close()
                    continue
                if line1 == "edges" and not meshesE.has_key(s[1]):
                    m = matrix.EdgeMatrix()
                    for line in meshFile.readlines():
                        line = line.strip()
                        vals = [float(x) for x in line.split(" ")]
                        m.add_edge(*vals)
                        meshesE[s[1]] = m
                elif line1 == "faces" and not meshesF.has_key(s[1]):
                    m = matrix.FaceMatrix()
                    for line in meshFile.readlines():
                        line = line.strip()
                        vals = [float(x) for x in line.split(" ")]
                        m.add_face(*vals)
                        meshesF[s[1]] = m
                meshFile.close()
            except:
                pass

    for s in symbols:
        if s[0] == "knoblist" and not knoblists.has_key(s[1]):
            knoblists[s[1]] = {}
            for k in knobs.keys():
                knoblists[s[1]][k] = 1.0
    
    frames = 1
    for command in arc["frames"]:
        if command[1] > frames:
            frames = command[1]
        command[0] = "ignore"
    for command in arc["vary"]:
        if command[3] + 1 > frames:
            frames = command[3] + 1
    for command in arc["tween"]:
        if command[2] + 1 > frames:
            frames = command[2] + 1
    
    tmpknobs = {}
    for k in knobs.keys():
        tmpknobs[k] = 1.0
    image_requests = []
    base_matrix = matrix.ident()
    focalLength = 0
    for command in commands:
        if command[0] == "set":
            tmpknobs[command[1]] = float(command[2])
            command[0] = "ignore"
        if command[0] == "set_knobs":
            for k in tmpknobs.keys():
                tmpknobs[k] = command[1]
            command[0] = "ignore"
        if command[0] == "save_knobs":
            knoblists[command[1]] = tmpknobs.copy()
            command[0] = "ignore"
        if command[0] == "tween":
            (tweenliteral, start, end, knoblist0, knoblist1, f) = command
            i = start
            if start <= end:
                for k in knobs.keys():
                    if not knobs[k]:
                        knobs[k] = [None] * frames
            while i <= end:
                slider = float(f(float(i - start)))
                for k in knobs.keys():
                    knobs[k][i] = slider * knoblists[knoblist1][k] + (1 - slider) * knoblists[knoblist0][k]
                i = i + 1
            command[0] = "ignore"
        if command[0] == "vary":
            (varyliteral, knobname, start, end, f) = command
            i = start
            if start <= end:
                if not knobs[knobname]:
                    knobs[knobname] = [None] * frames
            while i <= end:
                knobs[knobname][i] = float(f(float(i - start)))
                i = i + 1
            command[0] = "ignore"
        if command[0] == "basename":
            image_requests.append([command[1], base_matrix, focalLength])
            command[0] = "ignore"
        if command[0] == "camera":
            base_matrix = matrix.ident()
            base_matrix *= matrix.move(0 - command[1], 0 - command[2], 0 - command[3])
            xaim = command[4] - command[1]
            yaim = command[5] - command[2]
            zaim = command[6] - command[3]
            if xaim == 0 and zaim == 0:
                if yaim >= 0:
                    base_matrix *= matrix.rotate("x", -90)
                else:
                    base_matrix *= matrix.rotate("x", 90)
            else:
                theta = (math.atan2(yaim, math.sqrt(math.pow(xaim, 2) + math.pow(zaim, 2)))) * -180.0 / 3.14159265358979323
                base_matrix *= matrix.rotate("x", theta)
                theta = ((math.atan2(zaim, xaim) - math.atan2(1, 0)) * 180.0 / 3.14159265358979323)
                base_matrix *= matrix.rotate("y", theta)
            command[0] = "ignore"
        if command[0] == "focal":
            focalLength = command[1]
            command[0] = "ignore"
    
    for knobname in knobs.keys():
        if not knobs[knobname]:
            knobs[knobname] = [1.0] * frames
        values = knobs[knobname]
        for i in range(frames):
            if values[i] != None:
                val = values[i]
                break
        for i in range(frames):
            if values[i] == None:
                values[i] = val
            else:
                val = values[i]
    
    for i in range(frames):
        print "starting frame %d ..." % i,
        sys.stdout.flush()
        K = {}
        for k in knobs:
            K[k] = knobs[k][i]
        for basename, base_matrix, focalLength in image_requests:
            view = runCommands(commands, K, constants, coord_systems, meshesE, meshesF, base_matrix, focalLength)
            name = (basename + "%0" + str(len(str(frames - 1))) + "d.ppm") % i
            view.save(name)
        print "DONE"
    
    print "converting to gif format ...", 
    sys.stdout.flush()
    for name, base_matrix, focalLength in image_requests:
        os.system("mogrify -format gif %s*.ppm" % name)
        os.system("convert -delay 2.5 -loop 0 %s[0-9]*.gif %s.gif" % (name, name))
        os.system("rm %s*.ppm" % name)
    print "DONE"

def getKnobValues(knobs):
    """
    This function takes user input to set knob values
    """
    print
    while 1:
        for k in sorted(knobs.keys()):
            print k, "\tis currently\t", knobs[k]
        text = raw_input("Name the knob you would like to change (or press enter to continue):\n> ")
        if not text:
            break
        if knobs.has_key(text):
            while 1:
                val = raw_input("Please enter a new value for knob " + text + " or type \'cancel\':\n> ")
                if val == "cancel":
                    print
                    break
                try:
                    knobs[text] = float(val)
                    print
                    break
                except ValueError:
                    print "The value you entered is not valid."
                    continue
        else:
            print "No knob of that name found.\n"
    return knobs

def runCommands(commands, knobs, constants, coord_systems, meshesE, meshesF, base_matrix, focalLength):
    """
    Runs the given commands and returns the resulting screen
    """
    stack = [base_matrix.clone()]
    view = screen.Screen()
    constants[None] = [255, 255, 255, 200, 200, 200, 100, 100, 100, 0, 0, 0]
    lights = []
    ambient = [0, 0, 0]
    shading_type = "wireframe"
    for command in commands:
        if command[0] == "ignore":
            pass
        elif command[0] == "pop":
            stack.pop()
            if not stack:
                stack = [base_matrix.clone()]
        elif command[0] == "push":
            stack.append(stack[-1].clone())
        elif command[0] == "screen":
            view = screen.Screen(command[1], command[2])
            stack = [base_matrix.clone()]
        elif command[0] == "save":
            view.save(command[1])
        elif command[0] == "display":
            if len(command) == 2:
                screen.display(command[1])
            else:
                screen.display(view)
        elif command[0] == "camera":
            base_matrix = matrix.ident()
            base_matrix *= matrix.move(0 - command[1], 0 - command[2], 0 - command[3])
            xaim = command[4] - command[1]
            yaim = command[5] - command[2]
            zaim = command[6] - command[3]
            if xaim == 0 and zaim == 0:
                if yaim >= 0:
                    base_matrix *= matrix.rotate("x", -90)
                else:
                    base_matrix *= matrix.rotate("x", 90)
            else:
                theta = (math.atan2(yaim, math.sqrt(math.pow(xaim, 2) + math.pow(zaim, 2)))) * -180.0 / 3.14159265358979323
                base_matrix *= matrix.rotate("x", theta)
                theta = ((math.atan2(zaim, xaim) - math.atan2(1, 0)) * 180.0 / 3.14159265358979323)
                base_matrix *= matrix.rotate("y", theta)
            stack = [base_matrix.clone()]
        elif command[0] == "focal":
            focalLength = command[1]
            view.focalLength = focalLength
        elif command[0] == "set":
            knobs[command[1]] = float(command[2])
        elif command[0] == "set_knobs":
            for name in knobs.keys():
                knobs[name] = float(command[1])
        elif command[0] == "ambient":
            ambient = command[1:]
        elif command[0] == "light":
            lights.append(command[1:])
        elif command[0] == "sphere":
            m = matrix.FaceMatrix()
            m.add_sphere(*[command[i] for i in range(2, 8) if i != 5])
            if command[5]:
                m.apply(coord_systems[command[5]])
            else:
                m.apply(stack[-1])
            view.draw_FaceMatrix(m, [shading_type, constants[command[1]], ambient, lights])
        elif command[0] == "torus":
            m = matrix.FaceMatrix()
            m.add_torus(*[command[i] for i in range(2, 9) if i != 5])
            if command[5]:
                m.apply(coord_systems[command[5]])
            else:
                m.apply(stack[-1])
            view.draw_FaceMatrix(m, [shading_type, constants[command[1]], ambient, lights])
        elif command[0] == "box":
            m = matrix.FaceMatrix()
            m.add_box(*(command[2:8]))
            if command[8]:
                m.apply(coord_systems[command[8]])
            else:
                m.apply(stack[-1])
            view.draw_FaceMatrix(m, [shading_type, constants[command[1]], ambient, lights])
        elif command[0] == "line":
            m = matrix.PointMatrix()
            n = matrix.PointMatrix()
            m.add_point(*command[2:5])
            n.add_point(*command[6:9])
            if command[5]:
                m.apply(coord_systems[command[5]])
            else:
                m.apply(stack[-1])
            if command[9]:
                n.apply(coord_systems[command[9]])
            else:
                n.apply(stack[-1])
            [x0, y0, z0] = [m.get(i, 0) for i in range(3)]
            [x1, y1, z1] = [n.get(i, 0) for i in range(3)]
            m = matrix.EdgeMatrix()
            m.add_edge(x0, y0, z0, x1, y1, z1)
            view.draw_EdgeMatrix(m, [shading_type, constants[command[1]], ambient, lights])
        elif command[0] == "bezier":
            xs = []
            ys = []
            zs = []
            for i in range(4):
                m = matrix.PointMatrix()
                m.add_point(*command[2 + 4 * i:5 + 4 * i])
                if command[5 + 4 * i]:
                    m.apply(coord_systems[command[5 + 4 * i]])
                else:
                    m.apply(stack[-1])
                xs.append(m.get(0, 0))
                ys.append(m.get(1, 0))
                zs.append(m.get(2, 0))
            m = matrix.EdgeMatrix()
            m.add_bezier_curve(xs[0], ys[0], zs[0], xs[1], ys[1], zs[1], xs[2], ys[2], zs[2], xs[3], ys[3], zs[3], command[18])
            view.draw_EdgeMatrix(m, [shading_type, constants[command[1]], ambient, lights])
        elif command[0] == "hermite":
            xs = []
            ys = []
            zs = []
            for i in range(4):
                m = matrix.PointMatrix()
                m.add_point(*command[2 + 4 * i:5 + 4 * i])
                if command[5 + 4 * i]:
                    m.apply(coord_systems[command[5 + 4 * i]])
                else:
                    m.apply(stack[-1])
                xs.append(m.get(0, 0))
                ys.append(m.get(1, 0))
                zs.append(m.get(2, 0))
            m = matrix.EdgeMatrix()
            m.add_hermite_curve(xs[0], ys[0], zs[0], xs[1], ys[1], zs[1], xs[2], ys[2], zs[2], xs[3], ys[3], zs[3], command[18])
            view.draw_EdgeMatrix(m, [shading_type, constants[command[1]], ambient, lights])
        elif command[0] == "mesh":
            if meshesE.has_key(command[2]):
                m = meshesE[command[2]].clone()
                if command[3]:
                    m.apply(coord_systems[command[3]])
                else:
                    m.apply(stack[-1])
                view.draw_EdgeMatrix(m, [shading_type, constants[command[1]], ambient, lights])
            elif meshesF.has_key(command[2]):
                m = meshesF[command[2]].clone()
                if command[3]:
                    m.apply(coord_systems[command[3]])
                else:
                    m.apply(stack[-1])
                view.draw_FaceMatrix(m, [shading_type, constants[command[1]], ambient, lights])
        elif command[0] == "save_coord_system":
            coord_systems[command[1]] = stack[-1].clone()
        elif command[0] == "constants":
            constants[command[1]] = command[2:]
        elif command[0] == "shading":
            shading_type = command[1]
        elif command[0] == "move":
            if command[4]:
                val = float(knobs[command[4]])
            else:
                val = 1.0
            stack[-1] *= matrix.move(command[1] * val, command[2] * val, command[3] * val)
        elif command[0] == "scale":
            if command[4]:
                val = float(knobs[command[4]])
            else:
                val = 1.0
            stack[-1] *= matrix.scale(command[1] * val, command[2] * val, command[3] * val)
        elif command[0] == "scaleXYZ":
            if command[3]:
                val = float(knobs[command[3]])
            else:
                val = 1.0
            if command[1] == "x":
                stack[-1] *= matrix.scale(command[2] * val, 1, 1)
            elif command[1] == "y":
                stack[-1] *= matrix.scale(1, command[2] * val, 1)
            else:
                stack[-1] *= matrix.scale(command[2] * val, 1, 1)
        elif command[0] == "rotate":
            if command[3]:
                val = float(knobs[command[3]])
            else:
                val = 1.0
            stack[-1] *= matrix.rotate(command[1], command[2] * val)
    return view
