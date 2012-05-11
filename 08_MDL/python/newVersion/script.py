import mdl

def run(filename):
    """
    This function runs an mdl script
    """
    (commands, symbols) = mdl.parseFile(filename)
    knobs = {}
    for s in symbols.keys():
        if symbols[s][0] == "knob":
            knobs[s] = symbols[s][1]
    knobs = getKnobValues(knobs)
    for s in knobs.keys():
        symbols[s][1] = knobs[s]
    for command in commands:
        pass

def getKnobValues(knobs):
    """
    This function takes user input to set knob values
    """
    for k in sorted(knobs.keys()):
        print k, "is currently", knobs[k]
    pass
