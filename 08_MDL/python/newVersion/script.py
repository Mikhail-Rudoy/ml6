import mdl

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
    for s in symbols.keys():
        if symbols[s][0] == "knob":
            knobs[s] = symbols[s][1]
    knobs = getKnobValues(knobs)
    for s in knobs.keys():
        symbols[s] = ("knob", knobs[s])
    for command in commands:
        if command[0] == "pop":
            pass
        if command[0] == "push":
            pass
        if command[0] == "save":
            pass
        if command[0] == "display":
            pass
        if command[0] == "set":
            pass
        if command[0] == "set_knobs":
            pass
        if command[0] == "sphere":
            pass
        if command[0] == "torus":
            pass
        if command[0] == "box":
            pass
        if command[0] == "line":
            pass
        if command[0] == "bezier":
            pass
        if command[0] == "hermite":
            pass
        if command[0] == "circle":
            pass
        if command[0] == "move":
            pass
        if command[0] == "scale":
            pass
        if command[0] == "rotate":
            pass

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

