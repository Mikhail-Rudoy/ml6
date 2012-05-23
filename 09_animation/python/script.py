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
    while 1:
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
        while 1:
            text = raw_input("Continue?\n> ")
            if not text in ["yes", "no", "n", "y"]:
                print "I don't understand."
            elif text in ["yes", "y"]:
                print
                break
            else:
                return
        knobs = getKnobValues(knobs)

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

