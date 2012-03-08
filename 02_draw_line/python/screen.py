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
    screen[y][x] = c

def get_pixel(screen, x, y):
    return screen[y][x]

def draw_line(screen, x0, y0, x1, y1, c):
    dx = x1 - x0
    dy = y1 - y0
    if dx + dy < 0:
        dx = 0 - dx
        dy = 0 - dy
        tmp = x0
        x0 = x1
        x1 = tmp
        tmp = y0
        y0 = y1
        y1 = tmp
    
    if dx == 0:
        y = y0
        while y <= y1:
            draw_pixel(screen, x0, y, c)
            y = y + 1
    elif dy == 0:
        x = x0
        while x <= x1:
            draw_pixel(screen, x, y0, c)
            x = x + 1
    elif dy < 0:
        d = 0
        x = x0
        y = y0
        while x <= x1:
            draw_pixel(screen, x, y, c)
            if d > 0:
                y = y - 1
                d = d - dx
            x = x + 1
            d = d - dy
    elif dx < 0:
        d = 0
        x = x0
        y = y0
        while y <= y1:
            draw_pixel(screen, x, y, c)
            if d > 0:
                x = x - 1
                d = d - dy
            y = y + 1
            d = d - dx
    elif dx > dy:
        d = 0
        x = x0
        y = y0
        while x <= x1:
            draw_pixel(screen, x, y, c)
            if d > 0:
                y = y + 1
                d = d - dx
            x = x + 1
            d = d + dy
    else:
        d = 0
        x = x0
        y = y0
        while y <= y1:
            draw_pixel(screen, x, y, c)
            if d > 0:
                x = x + 1
                d = d - dy
            y = y + 1
            d = d + dx
