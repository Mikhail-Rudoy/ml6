def new_screen(w, h):
    black = [0, 0, 0]
    result = []
    for x in range(w):
        result = result + [[]]
        for y in range(h):
            result[x] = result[x] + [black[:]]
    return result

def save_screen(screen, filename):
    FILE = open(filename, "w")
    lines = ["P3"]
    lines.append("" + str(len(screen)) + " " + str(len(screen[0])) + " 255")
    for x in range(len(screen)):
        next = ""
        for y in range(len(screen[x])):
            next = next + str(screen[x][y][0]) + " "
            next = next + str(screen[x][y][1]) + " "
            next = next + str(screen[x][y][2]) + " "
        lines.append(next)
    for i in range(len(lines)):
        lines[i] = lines[i] + "\n"
    FILE.writelines(lines)
    FILE.close()

def draw_pixel(screen, x, y, c):
    screen[-1-y][x] = c
