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
        print command

def getKnobValues(knobs):
    """
    This function takes user input to set knob values
    """
    for k in sorted(knobs.keys()):
        print k, "\tis currently\t", knobs[k]
    pass
    return knobs

