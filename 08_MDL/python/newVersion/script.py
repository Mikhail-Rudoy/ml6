import mdl, matrix, screen

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
    knobs = {}
    for s in symbols:
        if s[0] == "knob":
            knobs[s[1]] = 0.0
    knobs = getKnobValues(knobs)
    stack = [matrix.ident()]
    view = screen.Screen()
    for command in commands:
        if command[0] == "pop":
            stack.pop()
            if not stack:
                stack = [matrix.ident()]
        if command[0] == "push":
            stack.append(stack[-1].clone())
        if command[0] == "screen":
            view = screen.screen(command[1], command[2])
        if command[0] == "save":
            view.save(command[1])
        if command[0] == "display":
            if len(command) == 2:
                screen.display(command[1])
            else:
                screen.display(view)
        if command[0] == "set":
            knobs[command[1]] = command[2]
        if command[0] == "set_knobs":
            for name in knobs.keys():
                knobs[name] = command[1]
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
            m.add_box(*commands[1:])
            m.apply(stack[-1])
            view.draw_FaceMatrix(m, [255, 255, 255])
        if command[0] == "line":
            m = matrix.EdgeMatrix()
            m.add_edge(*commands[1:])
            m.apply(stack[-1])
            view.draw_EdgeMatrix(m, [255, 255, 255)]
        if command[0] == "bezier":
            m = matrix.EdgeMatrix()
            m.add_bezier_curve(*commands[1:])
            m.apply(stack[-1])
            view.draw_EdgeMatrix(m, [255, 255, 255])
        if command[0] == "hermite":
            m = matrix.EdgeMatrix()
            m.add_hermite_curve(*commands[1:])
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
            if commands[4]:
                val = knobs[commands[4]]
            else:
                val = 1
            stack[-1] *= matrix.move(commands[1] * val, \
                                     commands[2] * val, \
                                     commands[3] * val)
        if command[0] == "scale":
            if commands[4]:
                val = knobs[commands[4]]
            else:
                val = 1
            stack[-1] *= matrix.scale(commands[1] * val, \
                                      commands[2] * val, \
                                      commands[3] * val)
        if command[0] == "rotate":
            if commands[3]:
                val = knobs[commands[3]]
            else:
                val = 1
            stack[-1] *= matrix.rotate(commands[1], commands[2] * val)

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

