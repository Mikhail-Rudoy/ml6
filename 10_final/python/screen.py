import math, os, vector, matrix, random

class Screen():
    """
    This class stores the color data associated with an image.
    """
    
    def __init__(self, w = 600, h = 600):
        """
        This constructor stores the pixel data for a screen of resolution 
        w by h.
        Every pixel is initialized to black.
        """
        black = [0, 0, 0]
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
    
    def draw_line(self, x0, y0, z0, x1, y1, z1, col):
        """
        This method draws a line between two points on the screen.
        """
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
    
    def draw_EdgeMatrix(self, m, col):
        """
        This method draws the edges contained in an EdgeMatrix.
        """
        i = 0
        while i < m.width() - 1:
            x0 = m.get(0, i)
            y0 = m.get(1, i)
            z0 = m.get(2, i)
            x1 = m.get(0, i + 1)
            y1 = m.get(1, i + 1)
            y2 = m.get(2, i + 1)
            self.draw_line(int(x0), int(y0), z0, int(x1), int(y1), z1, col)
            i = i + 2
    
    def draw_FaceMatrix(self, m, col, view = [0, 0, -1]):
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
            if (vector.Vector(x1 - x0, y1 - y0, z1 - z0)).cross(vector.Vector(x2 - x0, y2 - y0, z2 - z0)).dot(vector.Vector(*view)) > 0:
                self.draw_line(x0, y0, z0, x1, y1, z1, col)
                self.draw_line(x0, y0, z0, x2, y2, z2, col)
                self.draw_line(x2, y2, z2, x1, y1, z1, col)
                [x0, y0, x1, y1, x2, y2] = [int(v) for v in [x0, y0, x1, y1, x2, y2]]
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
                    self.draw_line(int(x0), y, z0, int(x1), y, z1, [0, 0, 255])
                    x0 += (top[0] - bot[0]) * 1.0 / (top[1] - bot[1])
                    z0 += (top[2] - bot[2]) * 1.0 / (top[1] - bot[1])
                    if y < mid[1]:
                        x1 += (mid[0] - bot[0]) * 1.0 / (mid[1] - bot[1])
                        z1 += (mid[2] - bot[2]) * 1.0 / (mid[1] - bot[1])
                    elif y < top[1]:
                        x1 += (top[0] - mid[0]) * 1.0 / (top[1] - mid[1])
                        z1 += (top[2] - mid[2]) * 1.0 / (top[1] - mid[1])
                    y = y + 1
            i = i + 3

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
