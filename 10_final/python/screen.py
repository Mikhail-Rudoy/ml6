import math, os, vector, matrix, random

class Screen():
    """
    This class stores the color data associated with an image.
    """
    
    def __init__(self, w = 500, h = 500):
        """
        This constructor stores the pixel data for a screen of resolution 
        w by h.
        Every pixel is initialized to black.
        """
        black = [0, 0, 0]
        self.focalLength = 0
        self.__pixels__ = []
        self.__zbuffer__ = []
        for r in range(h):
            self.__pixels__.append([])
            self.__zbuffer__.append([])
            for c in range(w):
                self.__pixels__[r].append(black[:])
                self.__zbuffer__[r].append(float("inf"))
    
    def save(self, filename = None):
        """
        This method saves the screen to a filename.
        If no filename is specified, the ultimate filename used 
        by the screen object is used.
        """
        if filename == None:
            filename = self._filename
            if filename == None:
                raise TypeError("no file specified")
        self._filename = filename
        FILE = open(filename, "w")
        lines = ["P3"]
        lines.append(str(len(self.__pixels__[0])) + " ")
        lines.append(str(len(self.__pixels__)) + " 255")
        for r in range(len(self.__pixels__)):
            line = ""
            for c in range(len(self.__pixels__[r])):
                line += str(self.__pixels__[r][c][0]) + " "
                line += str(self.__pixels__[r][c][1]) + " "
                line += str(self.__pixels__[r][c][2]) + " "
            lines.append(line)
        for i in range(len(lines)):
            lines[i] = lines[i] + "\n"
        FILE.writelines(lines)
        FILE.close()
    
    def set(self, x, y, z, col):
        """
        This method draws a color to a particular pixel of the 
        screen.
        """
        c, r = int(x), int(y)
        if r < len(self.__pixels__) and r >= 0 and \
                c >= 0 and c < len(self.__pixels__[r]) and \
                self.__zbuffer__[r][c] > z:
            self.__pixels__[r][c] = col
            self.__zbuffer__[r][c] = z
    
    def get(self, x, y):
        """
        This method returns the color currently occupying the given
        pixel.
        """
        c, r = int(x), int(y)
        if r < len(self.__pixels__) and r >= 0 and \
                c >= 0 and c < len(self.__pixels__[r]):
            return self.__pixels__[r][c]
    
    def draw_line(self, x0, y0, z0, x1, y1, z1, shading_info):
        """
        This method draws a line between two points on the screen.
        """
        if shading_info[0] == "color":
            col = shading_info[1]
        if shading_info[0] == "colors":
            col0 = shading_info[1]
            col1 = shading_info[2]
            R, G, B = col0
            dR, dG, dB = col1
            dR, dG, dB = dR - R, dG - G, dB - B
        x0 = int(x0)
        y0 = int(y0)
        z0 = float(z0)
        x1 = int(x1)
        y1 = int(y1)
        z1 = float(z1)
        dx = x1 - x0
        dy = y1 - y0
        dz = z1 - z0
        if dx + dy < 0:
            dx = 0 - dx
            dy = 0 - dy
            dz = 0 - dz
            x0, x1 = x1, x0
            y0, y1 = y1, y0
            z0, z1 = z1, z0
        if dx == 0 and dy == 0:
            self.set(x0, y0, max([z0, z1]), col)
        elif dx == 0:
            y = y0
            z = z0
            while y <= y1:
                self.set(x0, y, z, col)
                y = y + 1
                z = z + dz / dy
        elif dy == 0:
            x = x0
            z = z0
            while x <= x1:
                self.set(x, y0, z, col)
                x = x + 1
                z = z + dz / dx
        elif dy < 0:
            d = 0
            x = x0
            y = y0
            z = z0
            while x <= x1:
                self.set(x, y, z, col)
                if d > 0:
                    y = y - 1
                    d = d - dx
                x = x + 1
                z = z + dz / dx
                d = d - dy
        elif dx < 0:
            d = 0
            z = z0
            x = x0
            y = y0
            while y <= y1:
                self.set(x, y, z, col)
                if d > 0:
                    x = x - 1
                    d = d - dy
                y = y + 1
                z = z + dz / dy
                d = d - dx
        elif dx > dy:
            d = 0
            x = x0
            y = y0
            z = z0
            while x <= x1:
                self.set(x, y, z, col)
                if d > 0:
                    y = y + 1
                    d = d - dx
                x = x + 1
                z = z + dz / dx
                d = d + dy
        else:
            d = 0
            x = x0
            y = y0
            z = z0
            while y <= y1:
                self.set(x, y, z, col)
                if d > 0:
                    x = x + 1
                    d = d - dy
                y = y + 1
                z = z + dz / dx
                d = d + dx
    
    def draw_EdgeMatrix(self, m, shading_info):
        """
        This method draws the edges contained in an EdgeMatrix.
        """
        if shading_info[0] == "wireframe":
            shading_info = ["color", [255, 255, 255]]
        
        if shading_info[0] in ["goroud", "phong"]:
            edges = {}
            i = 0
            while i < m.width() - 1:
                x0 = m.get(0, i)
                y0 = m.get(1, i)
                z0 = m.get(2, i)
                x1 = m.get(0, i + 1)
                y1 = m.get(1, i + 1)
                y2 = m.get(2, i + 1)
                i = i + 2
                dx = float(x0 - x1)
                dy = float(y0 - y1)
                dz = float(z0 - z1)
                dx, dy, dz = dx / math.sqrt(dx * dx + dy * dy + dz * dz), dy / math.sqrt(dx * dx + dy * dy + dz * dz), dz / math.sqrt(dx * dx + dy * dy + dz * dz)
                if edges.has_key((x0, y0, z0)):
                    edges[(x0, y0, z0)].append((dx, dy, dz))
                else:
                    edges[(x0, y0, z0)] = [(dx, dy, dz)]
                if edges.has_key((x1, y1, z1)):
                    edges[(x1, y1, z1)].append((dx, dy, dz))
                else:
                    edges[(x1, y1, z1)] = [(dx, dy, dz)]

        for k in edges.keys():
            x = 0
            y = 0
            z = 0
            n = 0
            for dx, dy, dz in edges[k]:
                x += dx
                y += dy
                z += dz
                n += 1
            edges[k] = vector.Vector((x / n, y / n, z / n))
            
        i = 0
        while i < m.width() - 1:
            x0 = m.get(0, i)
            y0 = m.get(1, i)
            z0 = m.get(2, i)
            x1 = m.get(0, i + 1)
            y1 = m.get(1, i + 1)
            y2 = m.get(2, i + 1)
            if self.focalLength != 0:
                y0 = y0 - (len(self.__pixels__) * 0.5)
                y0 = y0 * self.focalLength / (z0 + self.focalLength)
                y0 = y0 + (len(self.__pixels__) * 0.5)
                y1 = y1 - (len(self.__pixels__) * 0.5)
                y1 = y1 * self.focalLength / (z1 + self.focalLength)
                y1 = y1 + (len(self.__pixels__) * 0.5)
                x0 = x0 - (len(self.__pixels__[0]) * 0.5)
                x0 = x0 * self.focalLength / (z0 + self.focalLength)
                x0 = x0 + (len(self.__pixels__[0]) * 0.5)
                x1 = x1 - (len(self.__pixels__[0]) * 0.5)
                x1 = x1 * self.focalLength / (z1 + self.focalLength)
                x1 = x1 + (len(self.__pixels__[0]) * 0.5)
            if shading_info[0] == "flat":
                consts = shading_info[1]
                ambient = shading_info[2]
                lights = shading_info[3]
                col = consts[9:]
                dx = float(x0 - x1)
                dy = float(y0 - y1)
                dz = float(z0 - z1)
                dx, dy, dz = dx / math.sqrt(dx * dx + dy * dy + dz * dz), dy / math.sqrt(dx * dx + dy * dy + dz * dz), dz / math.sqrt(dx * dx + dy * dy + dz * dz)
                segmentvect = vector.Vector(dx, dy, dz)
                xcenter = 0.5 * (x0 + x1)
                ycenter = 0.5 * (y0 + y1)
                zcenter = 0.5 * (z0 + z1)
                for light in lights:
                    xlight = light[3]
                    ylight = light[4]
                    zlight = light[5]
                    dx2 = float(xcenter - xlight)
                    dy2 = float(ycenter - ylight)
                    dz2 = float(zcenter - zlight)
                    dx2, dy2, dz2 = dx2 / math.sqrt(dx2 * dx2 + dy2 * dy2 + dz2 * dz2), dy2 / math.sqrt(dx2 * dx2 + dy2 * dy2 + dz2 * dz2), dz2 / math.sqrt(dx2 * dx2 + dy2 * dy2 + dz2 * dz2)
                    lightvect = vector.Vector(dx2, dy2, dz2)
                    for i in range(3):
                        col[i] += consts[i] * ambient[i]
                        col[i] += light[i] * consts[i + 3] * math.sqrt(1 - Math.pow(lightvect.dot(segmentvect), 2))
                        val = math.cos(math.acos(math.sqrt(1 - Math.pow(lightvect.dot(segmentvect), 2))) - math.acos(0 - dz))
                        col[i] += light[i] * consts[i + 6] * (math.abs(val) + val) * 0.5
                col = [int(v) for v in col]
                self.draw_line(int(x0), int(y0), z0, int(x1), int(y1), z1, ["color", col])
            elif shading_info[0] == "goroud":
                consts = shading_info[1]
                ambient = shading_info[2]
                lights = shading_info[3]
                col0 = consts[9:]
                col1 = col0[:]
                for light in lights:
                    xlight = light[3]
                    ylight = light[4]
                    zlight = light[5]
                    dx0 = float(x0 - xlight)
                    dy0 = float(y0 - ylight)
                    dz0 = float(z0 - zlight)
                    dx0, dy0, dz0 = dx0 / math.sqrt(dx0 * dx0 + dy0 * dy0 + dz0 * dz0), dy0 / math.sqrt(dx0 * dx0 + dy0 * dy0 + dz0 * dz0), dz0 / math.sqrt(dx0 * dx0 + dy0 * dy0 + dz0 * dz0)
                    lightvect0 = vector.Vector(dx0, dy0, dz0)
                    dx1 = float(x1 - xlight)
                    dy1 = float(y1 - ylight)
                    dz1 = float(z1 - zlight)
                    dx1, dy, dz1 = dx1 / math.sqrt(dx1 * dx1 + dy1 * dy1 + dz1 * dz1), dy1 / math.sqrt(dx1 * dx1 + dy1 * dy1 + dz1 * dz1), dz1 / math.sqrt(dx1 * dx1 + dy1 * dy1 + dz1 * dz1)
                    lightvect1 = vector.Vector(dx1, dy1, dz1)
                    for i in range(3):
                        col0[i] += consts[i] * ambient[i]
                        col1[i] += consts[i] * ambient[i]
                        col0[i] += light[i] * consts[i + 3] * math.sqrt(1 - Math.pow(lightvect0.dot(edges[(x0, y0, z0)]), 2))
                        col1[i] += light[i] * consts[i + 3] * math.sqrt(1 - Math.pow(lightvect1.dot(edges[(x1, y1, z1)]), 2))
                        val0 = math.cos(math.acos(math.sqrt(1 - Math.pow(lightvect0.dot(edges[(x0, y0, z0)]), 2))) - math.acos(0 - dz0))
                        col0[i] += light[i] * consts[i + 6] * (math.abs(val0) + val0) * 0.5
                        val1 = math.cos(math.acos(math.sqrt(1 - Math.pow(lightvect1.dot(edges[(x1, y1, z1)]), 2))) - math.acos(0 - dz1))
                        col1[i] += light[i] * consts[i + 6] * (math.abs(val1) + val1) * 0.5
                self.draw_line(int(x0), int(y0), z0, int(x1), int(y1), z1, ["colors", col0, col1])
            elif shading_info[0] == "phong":
                self.draw_line(int(x0), int(y0), z0, int(x1), int(y1), z1, ["edge_vectors", edges[(x0, y0, z0)], edges[(x1, y1, z1)]] + shading_info[1:])
            else:
                self.draw_line(int(x0), int(y0), z0, int(x1), int(y1), z1, shading_info)
                
            i = i + 2
    
    def draw_FaceMatrix(self, m, shading_info, view = [0, 0, -1]):
        """
        This method draws the faces contained in a FaceMatrix.
        """
        i = 0
        while i < m.width() - 2:
            x0 = m.get(0, i)
            y0 = m.get(1, i)
            z0 = m.get(2, i)
            x1 = m.get(0, i + 1)
            y1 = m.get(1, i + 1)
            z1 = m.get(2, i + 1)
            x2 = m.get(0, i + 2)
            y2 = m.get(1, i + 2)
            z2 = m.get(2, i + 2)
            if self.focalLength != 0:
                y0 = y0 - (len(self.__pixels__) * 0.5)
                y0 = y0 * self.focalLength / (z0 + self.focalLength)
                y0 = y0 + (len(self.__pixels__) * 0.5)
                y1 = y1 - (len(self.__pixels__) * 0.5)
                y1 = y1 * self.focalLength / (z1 + self.focalLength)
                y1 = y1 + (len(self.__pixels__) * 0.5)
                y2 = y2 - (len(self.__pixels__) * 0.5)
                y2 = y2 * self.focalLength / (z2 + self.focalLength)
                y2 = y2 + (len(self.__pixels__) * 0.5)
                x0 = x0 - (len(self.__pixels__[0]) * 0.5)
                x0 = x0 * self.focalLength / (z0 + self.focalLength)
                x0 = x0 + (len(self.__pixels__[0]) * 0.5)
                x1 = x1 - (len(self.__pixels__[0]) * 0.5)
                x1 = x1 * self.focalLength / (z1 + self.focalLength)
                x1 = x1 + (len(self.__pixels__[0]) * 0.5)
                x2 = x2 - (len(self.__pixels__[0]) * 0.5)
                x2 = x2 * self.focalLength / (z2 + self.focalLength)
                x2 = x2 + (len(self.__pixels__[0]) * 0.5)
            if self.focalLength != 0 or (vector.Vector(x1 - x0, y1 - y0, z1 - z0)).cross(vector.Vector(x2 - x0, y2 - y0, z2 - z0)).dot(vector.Vector(*view)) > 0:
                self.scanline_convert(x0, y0, z0, x1, y1, z1, x2, y2, z2, shading_info)
            i = i + 3
    
    def scanline_convert(self, x0, y0, z0, x1, y1, z1, x2, y2, z2, shading_info):
        """
        this method shades a triangle
        """
        self.draw_line(x0, y0, z0, x1, y1, z1, col)
        self.draw_line(x0, y0, z0, x2, y2, z2, col)
        self.draw_line(x2, y2, z2, x1, y1, z1, col)[x0, y0, x1, y1, x2, y2] = [int(v) for v in [x0, y0, x1, y1, x2, y2]]
        pts = [(x0, y0, z0), (x1, y1, z1), (x2, y2, z2)]
        ys = [y0, y1, y2]
        top = pts[ys.index(max(ys))]
        pts = [pts[j] for j in range(len(pts)) if j != ys.index(max(ys))]
        ys = [ys[j] for j in range(len(ys)) if j != ys.index(max(ys))]
        mid = pts[ys.index(max(ys))]
        pts = [pts[j] for j in range(len(pts)) if j != ys.index(max(ys))]
        ys = [ys[j] for j in range(len(ys)) if j != ys.index(max(ys))]
        bot = pts[0]
        y = bot[1]
        x0 = bot[0] * 1.0
        x1 = bot[0] * 1.0
        z0 = bot[2] * 1.0
        z1 = bot[2] * 1.0
        while y < top[1]:
            if y == mid[1]:
                x1 = mid[0]
                z1 = mid[2]
            self.draw_line(int(x0), y, z0, int(x1), y, z1, col)
            x0 += (top[0] - bot[0]) * 1.0 / (top[1] - bot[1])
            z0 += (top[2] - bot[2]) * 1.0 / (top[1] - bot[1])
            if y < mid[1]:
                x1 += (mid[0] - bot[0]) * 1.0 / (mid[1] - bot[1])
                z1 += (mid[2] - bot[2]) * 1.0 / (mid[1] - bot[1])
            elif y < top[1]:
                x1 += (top[0] - mid[0]) * 1.0 / (top[1] - mid[1])
                z1 += (top[2] - mid[2]) * 1.0 / (top[1] - mid[1])
            y = y + 1

def display(source = None):
    """
    This function displays the given image file on screen.
    If the function is called with a screen, the file used 
    is the last file that screen was saved to.
    If a filename is specified, that file is displayed.
    """
    if isinstance(source, basestring):
        filename = source
    elif isinstance(source, Screen):
        filename = source._filename
    else:
        filename = None
    if filename == None:
        raise TypeError("no file specified")
    if os.fork():
        os.wait()
    else:
        os.system("display " + filename)
        exit()
