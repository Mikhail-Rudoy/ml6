import sys, re, math, os

namein = sys.argv[1]
nameout = sys.argv[2]
print "This could take a minute..."

if os.fork():
    os.wait()
else:
    os.system("convert %s -compress none %stmp.ppm" % (namein, namein))
    exit()

f = open("%stmp.ppm" % (namein,))
w = 0
h = 0
i = 0
buff = []
while i < 3 * w * h + 4:
    start = True
    while start or tok == "":
        if buff == []:
            buff = re.split("[ \t]+", f.readline().strip())
            for j in range(len(buff) / 2):
                buff[j], buff[-1 - j] = buff[-1 - j], buff[j]
        tok = buff.pop().strip()
        if len(tok) and tok[0] == "#":
            buff = []
            tok = ""
        start = False
    if i == 0:
        pass
    elif i == 1:
        w = int(tok)
    elif i == 2:
        h = int(tok)
        board = [[[0, 0, 0] for j in range(w)] for k in range(h)]
    elif i == 3:
        maxcol = int(tok)
    else:
        row = (i - 4) / (3 * w)
        col = (i - 4) % (3 * w)
        board[row][col / 3][col % 3] = int(tok) * 1.0 / maxcol
        if col % 3 == 2:
            board[row][col / 3] = sum(board[row][col / 3]) / 3.0
    i = i + 1
f.close()
os.system("rm %stmp.ppm" % (namein,))




newboard = []
for rnum in range(len(board) - 4):
    newboard.append([])
    for cnum in range(len(board[0]) - 4):
        val = 0
        for i in range(5):
            for j in range(5):
                loc = ((i - 2) ** 2 + (j - 2) ** 2) ** 0.5
                mul = {0:15, 1:12, 2:5, 2**0.5:9, 5**0.5:4, 8**0.5:2}[loc]
                val += mul / 159.0 * board[rnum + i][cnum + j]
        newboard[rnum].append(val)
board = newboard
   
gs = []
gthetas = []
for rnum in range(len(board) - 2):
    gs.append([])
    gthetas.append([])
    for cnum in range(len(board[0]) - 2):
        gy = board[rnum][cnum] + 2 * board[rnum][cnum + 1] + board[rnum][cnum + 2] - board[rnum + 2][cnum] - 2 * board[rnum + 2][cnum + 1] - board[rnum + 2][cnum + 2]
        gx = board[rnum][cnum + 2] + 2 * board[rnum + 1][cnum + 2] + board[rnum + 2][cnum + 2] - board[rnum][cnum] - 2 * board[rnum + 1][cnum] - board[rnum + 2][cnum]
        gs[rnum].append((gy ** 2 + gx ** 2) ** 0.5)
        gthetas[rnum].append(int((4.5 + 4 * math.atan2(gy, gx) / 3.141592653589) % 4))
        gthetas[rnum][cnum] = [(0, 1), (-1, 1), (-1, 0), (-1, -1)][gthetas[rnum][cnum]]

T1 = .3
T2 = .1
newboard = [[0] * len(gs[0]) for i in range(len(gs))]
for rnum in range(len(gs)):
    for cnum in range(len(gs[0])):
        if gs[rnum][cnum] > T1 and not newboard[rnum][cnum]:
            i = 0
            while rnum + i * gthetas[rnum][cnum][0] >= 0 and rnum + i * gthetas[rnum][cnum][0] < len(gs) and cnum + i * gthetas[rnum][cnum][1] >= 0 and cnum + i * gthetas[rnum][cnum][1] < len(gs[0]) and gthetas[rnum + gthetas[rnum][cnum][0] * i][cnum + gthetas[rnum][cnum][1] * i] == gthetas[rnum][cnum] and gs[rnum + gthetas[rnum][cnum][0] * i][cnum + gthetas[rnum][cnum][1] * i] > T2:
                newboard[rnum + gthetas[rnum][cnum][0] * i][cnum + gthetas[rnum][cnum][1] * i] = 0.1
                i = i - 1
            i = 1
            while rnum + i * gthetas[rnum][cnum][0] >= 0 and rnum + i * gthetas[rnum][cnum][0] < len(gs) and cnum + i * gthetas[rnum][cnum][1] >= 0 and cnum + i * gthetas[rnum][cnum][1] < len(gs[0]) and gthetas[rnum + gthetas[rnum][cnum][0] * i][cnum + gthetas[rnum][cnum][1] * i] == gthetas[rnum][cnum] and gs[rnum + gthetas[rnum][cnum][0] * i][cnum + gthetas[rnum][cnum][1] * i] > T2:
                newboard[rnum + gthetas[rnum][cnum][0] * i][cnum + gthetas[rnum][cnum][1] * i] = 0.1
                i = i + 1
board = newboard

newboard = []
for rnum in range(len(board)):
    newboard.append([])
    for cnum in range(len(board[0])):
        newboard[rnum].append([])
        newboard[rnum][cnum] = board[rnum][cnum]
        if board[rnum][cnum]:
            count = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i + rnum == -1 or i + rnum == len(board) or j + cnum == -1 or j + cnum == len(board[0]) or board[rnum + i][cnum + j]:
                        count = count + 1
            if count > 7 or count < 2:
                newboard[rnum][cnum] = 0
board = newboard

graph = {}
for rnum in range(len(board)):
    for cnum in range(len(board[0])):
        if board[rnum][cnum]:
            count = 0
            avgx = 0
            avgy = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i + rnum == -1 or i + rnum == len(board) or j + cnum == -1 or j + cnum == len(board[0]) or board[rnum + i][cnum + j]:
                        count = count + 1
                        avgx = avgx + i
                        avgy = avgy + j
            if count != 3 or avgx != 0 or avgy != 0:
                board[rnum][cnum] = 1
                graph[(rnum, cnum)] = []

def isvalid(r, c):
    return r >= 0 and r < len(board) and c >= 0 and c < len(board[0])

def draw_line((x0, y0), (x1, y1)):
    dx = x1 - x0
    dy = y1 - y0
    result = []
    if dx + dy < 0:
        dx = 0 - dx
        dy = 0 - dy
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    if dx == 0:
        y = y0
        while y <= y1:
            result.append((x0, y))
            y = y + 1
    elif dy == 0:
        x = x0
        while x <= x1:
            result.append((x, y0))
            x = x + 1
    elif dy < 0:
        d = 0
        x = x0
        y = y0
        while x <= x1:
            result.append((x, y))
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
            result.append((x, y))
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
            result.append((x, y))
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
            result.append((x, y))
            if d > 0:
                x = x + 1
                d = d - dy
            y = y + 1
            d = d + dx
    return result




for (r, c) in graph.keys():
    for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        i = 1
        if isvalid(r + dr, c + dc) and board[r + dr][c + dc] != 0:
            while board[r + i * dr][c + i * dc] != 1:
                i = i + 1
            graph[(r, c)].append((r + i * dr, c + i * dc))
            
for (r, c) in graph.keys():
    if len(graph[(r, c)]) == 2:
        path = draw_line(graph[(r, c)][0], graph[(r, c)][1])
        count = 0
        for (row, col) in path:
            if board[row][col] != 0:
                count = count + 1
        if count * 1.0 / len(path) > 0.5 or count > 5:
            other1 = graph[(r, c)][0]
            other2 = graph[(r, c)][1]
            graph[other1][graph[other1].index((r, c))] = other2
            graph[other2][graph[other2].index((r, c))] = other1
            del graph[(r, c)]
            board[r][c] = 0.1

f = open(nameout, "w")
f.write("edges\n")
for (r, c) in graph.keys():
    x = c
    y = r
    for (y2, x2) in graph[(r, c)]:
        f.write("%f %f 0 %f %f 0\n" % (x, y, x2, y2))
f.close()

#f = open(nameout, "w")
#f.write("P3 %d %d 255\n" % (len(board[0]), len(board)))
#for row in board:
#    for cell in row:
#        val = int(255 * cell)
#        f.write("%d %d %d  " % (val, val, val))
#f.close()
