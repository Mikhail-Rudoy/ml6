def new_screen(w, h):
    black = [0, 0, 0]
    result = []
    for x in range(w):
        result = result + [[]]
        for y in range(h):
            result[x] = result[x] + [black[:]]
    return result

def save_screen(screen, filename):
    file = open(