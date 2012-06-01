import mdl, matrix, screen, os, sys

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
    arc["set"] = []
    arc["set_knobs"] = []
    arc["vary"] = []
    arc["basename"] = []
    arc["frames"] = []
    
    for command in commands:
        if arc.has_key(command[0]):
            arc[command[0]].append(command)
    if not arc["basename"] and not arc["vary"] and not arc["frames"]:
        knobs = {}
        for s in symbols:
            if s[0] == "knob":
                knobs[s[1]] = 1.0
        while 1:
            knobs = getKnobValues(knobs)
            runCommands(commands, knobs)
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
        
    for command in arc["set"]:
        command[0] = "ignore"
        
    for command in arc["set_knobs"]:
        command[0] = "ignore"
    
    basenames = []
    for command in arc["basename"]:
        basenames.append(command[1])
        command[0] = "ignore"
    if not basenames:
        basenames.append("image")
    
    frames = 1
    for command in arc["frames"]:
        if command[1] > frames:
            frames = command[1]
        command[0] = "ignore"
    for command in arc["vary"]:
        if command[3] + 1 > frames:
            frames = command[3] + 1
    
    knobs = {}
    for s in symbols:
        if s[0] == "knob" and not knobs.has_key(s[1]):
            knobs[s[1]] = []
    
    for command in arc["vary"]:
        (varyliteral, knobname, start, end, f) = command
        command[0] = "ignore"
        i = start
        if start <= end:
            if not knobs[knobname]:
                knobs[knobname] = [None] * frames
        while i <= end:
            knobs[knobname][i] = float(f(float(i - start)))
            i = i + 1
    
    for knobname in knobs:
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
        view = runCommands(commands, K)
        for name in basenames:
            name = (name + "%0" + str(len(str(frames - 1))) + "d.ppm") % i
            view.save(name)
        print "DONE"
    
    print "converting to gif format ...", 
    sys.stdout.flush()
    for name in basenames:
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

def runCommands(commands, knobs):
    """
    Runs the given commands and returns the resulting screen
    """
    stack = [matrix.ident()]
    view = screen.Screen()
    for command in commands:
        if command[0] == "ignore":
            pass
        if command[0] == "pop":
            stack.pop()
            if not stack:
                stack = [matrix.ident()]
        if command[0] == "push":
            stack.append(stack[-1].clone())
        if command[0] == "screen":
            view = screen.Screen(command[1], command[2])
        if command[0] == "save":
            view.save(command[1])
        if command[0] == "display":
            if len(command) == 2:
                screen.display(command[1])
            else:
                screen.display(view)
        if command[0] == "set":
            knobs[command[1]] = float(command[2])
        if command[0] == "set_knobs":
            for name in knobs.keys():
                knobs[name] = float(command[1])
        if command[0] == "sphere":
            m = matrix.FaceMatrix()
            m.add_sphere(*command[1:])
            m.apply(stack[-1])
            view.draw_FaceMatrix(m, [255, 255, 255])
        if command[0] == "torus":
            m = matrix.FaceMatrix()
            m.add_torus(*command[1:])
            m.apply(stack[-1])
            view.draw_FaceMatrix(m, [255, 255, 255])
        if command[0] == "box":
            m = matrix.FaceMatrix()
            m.add_box(*command[1:])
            m.apply(stack[-1])
            view.draw_FaceMatrix(m, [255, 255, 255])
        if command[0] == "line":
            m = matrix.EdgeMatrix()
            m.add_edge(*command[1:])
            m.apply(stack[-1])
            view.draw_EdgeMatrix(m, [255, 255, 255])
        if command[0] == "bezier":
            m = matrix.EdgeMatrix()
            m.add_bezier_curve(*command[1:])
            m.apply(stack[-1])
            view.draw_EdgeMatrix(m, [255, 255, 255])
        if command[0] == "hermite":
            m = matrix.EdgeMatrix()
            m.add_hermite_curve(*command[1:])
            m.apply(stack[-1])
            view.draw_EdgeMatrix(m, [255, 255, 255])
        if command[0] == "circle":
            m = matrix.EdgeMatrix()
            m.add_circle(command[1], command[2], command[3], command[4])
            stack.append(stack[-1].clone())
            #
            #
            #
            #
            #
            m.apply(stack[-1])
            stack.pop()
            view.draw_EdgeMatrix(m, [255, 255, 255])
        if command[0] == "move":
            if command[4]:
                val = float(knobs[command[4]])
            else:
                val = 1.0
            stack[-1] *= matrix.move(command[1] * val, command[2] * val, command[3] * val)
        if command[0] == "scale":
            if command[4]:
                val = float(knobs[command[4]])
            else:
                val = 1.0
            stack[-1] *= matrix.scale(command[1] * val, command[2] * val, command[3] * val)
        if command[0] == "rotate":
            if command[3]:
                val = float(knobs[command[3]])
            else:
                val = 1.0
            stack[-1] *= matrix.rotate(command[1], command[2] * val)
    return view
