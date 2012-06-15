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
        c, r = int(x), int(y)
        col = [int(v) for v in col]
        for i in range(3):
            if col[i] < 0:
                col[i] = 0
            if col[i] > 255:
                col[i] = 255
        if r < len(self.__pixels__) and r >= 0 and \
                c >= 0 and c < len(self.__pixels__[r]) and \
                self.__zbuffer__[r][c] > z:
            self.__pixels__[r][c] = col
            self.__zbuffer__[r][c] = z
    
    def get(self, x, y):
        c, r = int(x), int(y)
        if r < len(self.__pixels__) and r >= 0 and \
                c >= 0 and c < len(self.__pixels__[r]):
            return self.__pixels__[r][c]
    
    def draw_line_one_color(self, x0, y0, z0, x1, y1, z1, col):
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
                z = z + dz / dy
                d = d + dx

    def draw_line_two_segment_vectors(self, x0, y0, z0, x1, y1, z1, consts, ambient, lights, segmentvect0, segmentvect1):
        x0 = int(x0)
        y0 = int(y0)
        z0 = float(z0)
        x1 = int(x1)
        y1 = int(y1)
        z1 = float(z1)
        dx = x1 - x0
        dy = y1 - y0
        dz = z1 - z0
        dx0, dy0, dz0 = [float(v) for v in segmentvect0.vals]
        dx1, dy1, dz1 = [float(v) for v in segmentvect1.vals]
        ddx = dx1 - dx0
        ddy = dy1 - dy0
        ddz = dz1 - dz0
        if dx + dy < 0:
            dx = 0 - dx
            dy = 0 - dy
            dz = 0 - dz
            ddx = 0 - ddx
            ddy = 0 - ddy
            ddz = 0 - ddz
            x0, x1 = x1, x0
            y0, y1 = y1, y0
            z0, z1 = z1, z0
            dx0, dx1 = dx1, dx0
            dy0, dy1 = dy1, dy0
            dz0, dz1 = dz1, dz0
        if dx == 0 and dy == 0:
            if z0 > z1:
                self.set(x0, y0, z0, self.get_color_from_segment_vector(consts, ambient, lights, segmentvect0, x0, y0, z0))
            else:
                self.set(x0, y0, z1, self.get_color_from_segment_vector(consts, ambient, lights, segmentvect1, x1, y1, z1))
        elif dx == 0:
            y = y0
            z = z0
            DX = dx0
            DY = dy0
            DZ = dz0
            while y <= y1:
                self.set(x0, y, z, self.get_color_from_segment_vector(consts, ambient, lights, vector.Vector(DX, DY, DZ), x0, y, z))
                y = y + 1
                z = z + dz / dy
                DX = DX + ddx / dy
                DY = DY + ddy / dy
                DZ = DZ + ddz / dy
        elif dy == 0:
            x = x0
            z = z0
            DX = dx0
            DY = dy0
            DZ = dz0
            while x <= x1:
                self.set(x, y0, z, self.get_color_from_segment_vector(consts, ambient, lights, vector.Vector(DX, DY, DZ), x, y0, z))
                x = x + 1
                z = z + dz / dx
                DX = DX + ddx / dx
                DY = DY + ddy / dx
                DZ = DZ + ddz / dx
        elif dy < 0:
            d = 0
            x = x0
            y = y0
            z = z0
            DX = dx0
            DY = dy0
            DZ = dz0
            while x <= x1:
                self.set(x, y, z, self.get_color_from_segment_vector(consts, ambient, lights, vector.Vector(DX, DY, DZ), x, y, z))
                if d > 0:
                    y = y - 1
                    d = d - dx
                x = x + 1
                z = z + dz / dx
                d = d - dy
                DX = DX + ddx / dx
                DY = DY + ddy / dx
                DZ = DZ + ddz / dx
        elif dx < 0:
            d = 0
            z = z0
            x = x0
            y = y0
            DX = dx0
            DY = dy0
            DZ = dz0
            while y <= y1:
                self.set(x, y, z, self.get_color_from_segment_vector(consts, ambient, lights, vector.Vector(DX, DY, DZ), x, y, z))
                if d > 0:
                    x = x - 1
                    d = d - dy
                y = y + 1
                z = z + dz / dy
                d = d - dx
                DX = DX + ddx / dy
                DY = DY + ddy / dy
                DZ = DZ + ddz / dy
        elif dx > dy:
            d = 0
            x = x0
            y = y0
            z = z0
            DX = dx0
            DY = dy0
            DZ = dz0
            while x <= x1:
                self.set(x, y, z, self.get_color_from_segment_vector(consts, ambient, lights, vector.Vector(DX, DY, DZ), x, y, z))
                if d > 0:
                    y = y + 1
                    d = d - dx
                x = x + 1
                z = z + dz / dx
                d = d + dy
                DX = DX + ddx / dx
                DY = DY + ddy / dx
                DZ = DZ + ddz / dx
        else:
            d = 0
            x = x0
            y = y0
            z = z0
            DX = dx0
            DY = dy0
            DZ = dz0
            while y <= y1:
                self.set(x, y, z, self.get_color_from_segment_vector(consts, ambient, lights, vector.Vector(DX, DY, DZ), x, y, z))
                if d > 0:
                    x = x + 1
                    d = d - dy
                y = y + 1
                z = z + dz / dy
                d = d + dx
                DX = DX + ddx / dy
                DY = DY + ddy / dy
                DZ = DZ + ddz / dy
    
    def draw_line_two_normal_vectors(self, x0, y0, z0, x1, y1, z1, consts, ambient, lights, normalvect0, normalvect1):
        x0 = int(x0)
        y0 = int(y0)
        z0 = float(z0)
        x1 = int(x1)
        y1 = int(y1)
        z1 = float(z1)
        dx = x1 - x0
        dy = y1 - y0
        dz = z1 - z0
        dx0, dy0, dz0 = [float(v) for v in normalvect0.vals]
        dx1, dy1, dz1 = [float(v) for v in normalvect1.vals]
        ddx = dx1 - dx0
        ddy = dy1 - dy0
        ddz = dz1 - dz0
        if dx + dy < 0:
            dx = 0 - dx
            dy = 0 - dy
            dz = 0 - dz
            ddx = 0 - ddx
            ddy = 0 - ddy
            ddz = 0 - ddz
            x0, x1 = x1, x0
            y0, y1 = y1, y0
            z0, z1 = z1, z0
            dx0, dx1 = dx1, dx0
            dy0, dy1 = dy1, dy0
            dz0, dz1 = dz1, dz0
        if dx == 0 and dy == 0:
            if z0 > z1:
                self.set(x0, y0, z0, self.get_color_from_normal_vector(consts, ambient, lights, normalvect0, x0, y0, z0))
            else:
                self.set(x0, y0, z1, self.get_color_from_normal_vector(consts, ambient, lights, normalvect1, x1, y1, z1))
        elif dx == 0:
            y = y0
            z = z0
            DX = dx0
            DY = dy0
            DZ = dz0
            while y <= y1:
                self.set(x0, y, z, self.get_color_from_normal_vector(consts, ambient, lights, vector.Vector(DX, DY, DZ), x0, y, z))
                y = y + 1
                z = z + dz / dy
                DX = DX + ddx / dy
                DY = DY + ddy / dy
                DZ = DZ + ddz / dy
        elif dy == 0:
            x = x0
            z = z0
            DX = dx0
            DY = dy0
            DZ = dz0
            while x <= x1:
                self.set(x, y0, z, self.get_color_from_normal_vector(consts, ambient, lights, vector.Vector(DX, DY, DZ), x, y0, z))
                x = x + 1
                z = z + dz / dx
                DX = DX + ddx / dx
                DY = DY + ddy / dx
                DZ = DZ + ddz / dx
        elif dy < 0:
            d = 0
            x = x0
            y = y0
            z = z0
            DX = dx0
            DY = dy0
            DZ = dz0
            while x <= x1:
                self.set(x, y, z, self.get_color_from_normal_vector(consts, ambient, lights, vector.Vector(DX, DY, DZ), x, y, z))
                if d > 0:
                    y = y - 1
                    d = d - dx
                x = x + 1
                z = z + dz / dx
                d = d - dy
                DX = DX + ddx / dx
                DY = DY + ddy / dx
                DZ = DZ + ddz / dx
        elif dx < 0:
            d = 0
            z = z0
            x = x0
            y = y0
            DX = dx0
            DY = dy0
            DZ = dz0
            while y <= y1:
                self.set(x, y, z, self.get_color_from_normal_vector(consts, ambient, lights, vector.Vector(DX, DY, DZ), x, y, z))
                if d > 0:
                    x = x - 1
                    d = d - dy
                y = y + 1
                z = z + dz / dy
                d = d - dx
                DX = DX + ddx / dy
                DY = DY + ddy / dy
                DZ = DZ + ddz / dy
        elif dx > dy:
            d = 0
            x = x0
            y = y0
            z = z0
            DX = dx0
            DY = dy0
            DZ = dz0
            while x <= x1:
                self.set(x, y, z, self.get_color_from_normal_vector(consts, ambient, lights, vector.Vector(DX, DY, DZ), x, y, z))
                if d > 0:
                    y = y + 1
                    d = d - dx
                x = x + 1
                z = z + dz / dx
                d = d + dy
                DX = DX + ddx / dx
                DY = DY + ddy / dx
                DZ = DZ + ddz / dx
        else:
            d = 0
            x = x0
            y = y0
            z = z0
            DX = dx0
            DY = dy0
            DZ = dz0
            while y <= y1:
                self.set(x, y, z, self.get_color_from_normal_vector(consts, ambient, lights, vector.Vector(DX, DY, DZ), x, y, z))
                if d > 0:
                    x = x + 1
                    d = d - dy
                y = y + 1
                z = z + dz / dy
                d = d + dx
                DX = DX + ddx / dy
                DY = DY + ddy / dy
                DZ = DZ + ddz / dy
    
    def draw_line_two_colors(self, x0, y0, z0, x1, y1, z1, col0, col1):
        x0 = int(x0)
        y0 = int(y0)
        z0 = float(z0)
        r0 = float(col0[0])
        g0 = float(col0[1])
        b0 = float(col0[2])
        x1 = int(x1)
        y1 = int(y1)
        z1 = float(z1)
        r1 = float(col1[0])
        g1 = float(col1[1])
        b1 = float(col1[2])
        dx = x1 - x0
        dy = y1 - y0
        dz = z1 - z0
        dr = r1 - r0
        dg = g1 - g0
        db = b1 - b0
        if dx + dy < 0:
            dx = 0 - dx
            dy = 0 - dy
            dz = 0 - dz
            dr = 0 - dr
            dg = 0 - dg
            db = 0 - db
            x0, x1 = x1, x0
            y0, y1 = y1, y0
            z0, z1 = z1, z0
            r0, r1 = r1, r0
            g0, g1 = g1, g0
            b0, b1 = b1, b0
        if dx == 0 and dy == 0:
            if z0 > z1:
                self.set(x0, y0, z0, [r0, g0, b0])
            else:
                self.set(x0, y0, z1, [r1, g1, b1])
        elif dx == 0:
            y = y0
            z = z0
            r = r0
            g = g0
            b = b0
            while y <= y1:
                self.set(x0, y, z, [r, g, b])
                y = y + 1
                z = z + dz / dy
                r = r + dr / dy
                g = g + dg / dy
                b = b + db / dy
        elif dy == 0:
            x = x0
            z = z0
            r = r0
            g = g0
            b = b0
            while x <= x1:
                self.set(x, y0, z, [r, g, b])
                x = x + 1
                z = z + dz / dx
                r = r + dr / dx
                g = g + dg / dx
                b = b + db / dx
        elif dy < 0:
            d = 0
            x = x0
            y = y0
            z = z0
            r = r0
            g = g0
            b = b0
            while x <= x1:
                self.set(x, y, z, [r, g, b])
                if d > 0:
                    y = y - 1
                    d = d - dx
                x = x + 1
                z = z + dz / dx
                d = d - dy
                r = r + dr / dx
                g = g + dg / dx
                b = b + db / dx
        elif dx < 0:
            d = 0
            z = z0
            x = x0
            y = y0
            r = r0
            g = g0
            b = b0
            while y <= y1:
                self.set(x, y, z, [r, g, b])
                if d > 0:
                    x = x - 1
                    d = d - dy
                y = y + 1
                z = z + dz / dy
                d = d - dx
                r = r + dr / dy
                g = g + dg / dy
                b = b + db / dy
        elif dx > dy:
            d = 0
            x = x0
            y = y0
            z = z0
            r = r0
            g = g0
            b = b0
            while x <= x1:
                self.set(x, y, z, [r, g, b])
                if d > 0:
                    y = y + 1
                    d = d - dx
                x = x + 1
                z = z + dz / dx
                d = d + dy
                r = r + dr / dx
                g = g + dg / dx
                b = b + db / dx
        else:
            d = 0
            x = x0
            y = y0
            z = z0
            r = r0
            g = g0
            b = b0
            while y <= y1:
                self.set(x, y, z, [r, g, b])
                if d > 0:
                    x = x + 1
                    d = d - dy
                y = y + 1
                z = z + dz / dy
                d = d + dx
                r = r + dr / dy
                g = g + dg / dy
                b = b + db / dy

    def get_color_from_segment_vector(self, consts, ambient, lights, segmentvect, x, y, z):
        dx, dy, dz = segmentvect.vals
        if dx == 0 and dy == 0 and dz == 0:
            return [consts[i] * ambient[i] + consts[9 + i] for i in range(3)]
        dx, dy, dz = dx / math.sqrt(dx * dx + dy * dy + dz * dz), dy / math.sqrt(dx * dx + dy * dy + dz * dz), dz / math.sqrt(dx * dx + dy * dy + dz * dz)
        segmentvect = vector.Vector(dx, dy, dz)
        col = consts[9:]
        for i in range(3):
            col[i] += consts[i] * ambient[i]
        for light in lights:
            xlight = light[3]
            ylight = light[4]
            zlight = light[5]
            dx = float(x - xlight)
            dy = float(y - ylight)
            dz = float(z - zlight)
            dx, dy, dz = dx / math.sqrt(dx * dx + dy * dy + dz * dz), dy / math.sqrt(dx * dx + dy * dy + dz * dz), dz / math.sqrt(dx * dx + dy * dy + dz * dz)
            lightvect = vector.Vector(dx, dy, dz)
            for i in range(3):
                col[i] += light[i] * consts[i + 3] * math.sqrt(1 - math.pow(lightvect.dot(segmentvect), 2))
                val = math.cos(math.acos(math.sqrt(1 - math.pow(lightvect.dot(segmentvect), 2))) - math.acos(0 - segmentvect.vals[2]))
                col[i] += light[i] * consts[i + 6] * (abs(val) + val) * 0.5
        return [float(v) for v in col]

    def draw_EdgeMatrix_wireframe(self, m):
        i = 0
        while i < m.width() - 1:
            x0 = m.get(0, i)
            y0 = m.get(1, i)
            z0 = m.get(2, i)
            x1 = m.get(0, i + 1)
            y1 = m.get(1, i + 1)
            z1 = m.get(2, i + 1)
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
            self.draw_line_one_color(int(x0), int(y0), z0, int(x1), int(y1), z1, [255, 255, 255])    
            i = i + 2
    
    def draw_EdgeMatrix_flat(self, m, consts, ambient, lights):
        i = 0
        while i < m.width() - 1:
            x0 = m.get(0, i)
            y0 = m.get(1, i)
            z0 = m.get(2, i)
            x1 = m.get(0, i + 1)
            y1 = m.get(1, i + 1)
            z1 = m.get(2, i + 1)
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
            dx = float(x0 - x1)
            dy = float(y0 - y1)
            dz = float(z0 - z1)
            x = 0.5 * (x0 + x1)
            y = 0.5 * (y0 + y1)
            z = 0.5 * (z0 + z1)
            col = self.get_color_from_segment_vector(consts, ambient, lights, vector.Vector(dx, dy, dz), x, y, z)
            self.draw_line_one_color(int(x0), int(y0), z0, int(x1), int(y1), z1, col)
            i = i + 2
    
    def draw_EdgeMatrix_goroud(self, m, consts, ambient, lights):
        edges = {}
        i = 0
        while i < m.width() - 1:
            x0 = m.get(0, i)
            y0 = m.get(1, i)
            z0 = m.get(2, i)
            x1 = m.get(0, i + 1)
            y1 = m.get(1, i + 1)
            z1 = m.get(2, i + 1)
            i = i + 2
            dx = float(x0 - x1)
            dy = float(y0 - y1)
            dz = float(z0 - z1)
            if dx == 0 and dy == 0 and dz == 0:
                continue
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
            n = 0.0
            for dx, dy, dz in edges[k]:
                x += dx
                y += dy
                z += dz
                n += 1
            edges[k] = vector.Vector(x / n, y / n, z / n)
        
        i = 0
        while i < m.width() - 1:
            x0 = m.get(0, i)
            y0 = m.get(1, i)
            z0 = m.get(2, i)
            x1 = m.get(0, i + 1)
            y1 = m.get(1, i + 1)
            z1 = m.get(2, i + 1)
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
            if x0 == x1 and y0 == y1 and z0 == z1:
                i = i + 2
                continue
            col0 = self.get_color_from_segment_vector(consts, ambient, lights, edges[(x0, y0, z0)], x0, y0, z0)
            col1 = self.get_color_from_segment_vector(consts, ambient, lights, edges[(x1, y1, z1)], x1, y1, z1)
            self.draw_line_two_colors(int(x0), int(y0), z0, int(x1), int(y1), z1, col0, col1)
            i = i + 2
    
    def draw_EdgeMatrix_phong(self, m, consts, ambient, lights):
        edges = {}
        i = 0
        while i < m.width() - 1:
            x0 = m.get(0, i)
            y0 = m.get(1, i)
            z0 = m.get(2, i)
            x1 = m.get(0, i + 1)
            y1 = m.get(1, i + 1)
            z1 = m.get(2, i + 1)
            i = i + 2
            dx = float(x0 - x1)
            dy = float(y0 - y1)
            dz = float(z0 - z1)
            if dx == 0 and dy == 0 and dz == 0:
                continue
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
            n = 0.0
            for dx, dy, dz in edges[k]:
                x += dx
                y += dy
                z += dz
                n += 1
            edges[k] = vector.Vector(x / n, y / n, z / n)
        
        i = 0
        while i < m.width() - 1:
            x0 = m.get(0, i)
            y0 = m.get(1, i)
            z0 = m.get(2, i)
            x1 = m.get(0, i + 1)
            y1 = m.get(1, i + 1)
            z1 = m.get(2, i + 1)
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
            if x0 == x1 and y0 == y1 and z0 == z1:
                i = i + 2
                continue
            self.draw_line_two_segment_vectors(int(x0), int(y0), z0, int(x1), int(y1), z1, consts, ambient, lights, edges[(x0, y0, z0)], edges[(x0, y0, z0)])
            i = i + 2
    
    def draw_EdgeMatrix(self, m, shading_info):
        if shading_info[0] == "wireframe":
            self.draw_EdgeMatrix_wireframe(m)
        elif shading_info[0] == "flat":
            self.draw_EdgeMatrix_flat(m, shading_info[1], shading_info[2], shading_info[3])
        elif shading_info[0] == "goroud":
            self.draw_EdgeMatrix_goroud(m, shading_info[1], shading_info[2], shading_info[3])
        elif shading_info[0] == "phong":
            self.draw_EdgeMatrix_phong(m, shading_info[1], shading_info[2], shading_info[3])
    
    def draw_FaceMatrix(self, m, shading_info):
        normals = None
        if shading_info[0] in ["goroud", "phong"]:
            i = 0
            normals = {}
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
                i = i + 2
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
                dx, dy, dz = ((vector.Vector(x1 - x0, y1 - y0, z1 - z0)).cross(vector.Vector(x2 - x0, y2 - y0, z2 - z0))).vals
                if dx != 0 or dy != 0 or dz != 0:
                    dx, dy, dz = dx / math.sqrt(dx * dx + dy * dy + dz * dz), dy / math.sqrt(dx * dx + dy * dy + dz * dz), dz / math.sqrt(dx * dx + dy * dy + dz * dz)
                if normals.has_key((int(x0), int(y0), int(z0))):
                    normals[(int(x0), int(y0), int(z0))].append((dx, dy, dz))
                else:
                    normals[(int(x0), int(y0), int(z0))] = [(dx, dy, dz)]
                if normals.has_key((int(x1), int(y1), int(z1))):
                    normals[(int(x1), int(y1), int(z1))].append((dx, dy, dz))
                else:
                    normals[(int(x1), int(y1), int(z1))] = [(dx, dy, dz)]
                if normals.has_key((int(x2), int(y2), int(z2))):
                    normals[(int(x2), int(y2), int(z2))].append((dx, dy, dz))
                else:
                    normals[(int(x2), int(y2), int(z2))] = [(dx, dy, dz)]
            for k in normals.keys():
                x = 0
                y = 0
                z = 0
                n = 0.0
                for dx, dy, dz in normals[k]:
                    x += dx
                    y += dy
                    z += dz
                    n += 1
                normals[k] = vector.Vector(x / n, y / n, z / n)
        
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
            i = i + 3
            if (vector.Vector(x1 - x0, y1 - y0, z1 - z0)).cross(vector.Vector(x2 - x0, y2 - y0, z2 - z0)).dot(vector.Vector(0, 0, -1)) == 0:
                continue
            if (vector.Vector(x1 - x0, y1 - y0, z1 - z0)).cross(vector.Vector(x2 - x0, y2 - y0, z2 - z0)).dot(vector.Vector(0, 0, -1)) > 0 or shading_info[0] == "wireframe":
                self.scanline_convert(x0, y0, z0, x1, y1, z1, x2, y2, z2, shading_info, normals)
    
    def get_color_from_normal_vector(self, consts, ambient, lights, normalvect, x, y, z):
        dx, dy, dz = normalvect.vals
        if dx == 0 and dy == 0 and dz == 0:
            return [consts[i] * ambient[i] + consts[9 + i] for i in range(3)]
        dx, dy, dz = dx / math.sqrt(dx * dx + dy * dy + dz * dz), dy / math.sqrt(dx * dx + dy * dy + dz * dz), dz / math.sqrt(dx * dx + dy * dy + dz * dz)
        normalvect = vector.Vector(dx, dy, dz)
        col = consts[9:]
        for i in range(3):
            col[i] += consts[i] * ambient[i]
        for light in lights:
            xlight = light[3]
            ylight = light[4]
            zlight = light[5]
            dx = 0 - float(x - xlight)
            dy = 0 - float(y - ylight)
            dz = 0 - float(z - zlight)
            dx, dy, dz = dx / math.sqrt(dx * dx + dy * dy + dz * dz), dy / math.sqrt(dx * dx + dy * dy + dz * dz), dz / math.sqrt(dx * dx + dy * dy + dz * dz)
            lightvect = vector.Vector(dx, dy, dz)
            for i in range(3):
                val = light[i] * consts[i + 3] * (normalvect.dot(lightvect))
                col[i] += (abs(val) + val) * 0.5
                val = vector.Vector(*[2 * lightvect.dot(normalvect) * normalvect.vals[i] - lightvect.vals[i] for i in range(3)]).dot(vector.Vector(0, 0, -1))
                col[i] += light[i] * consts[i + 6] * (abs(val) + val) * 0.5
        return [float(v) for v in col]
    
    def scanline_convert(self, x0, y0, z0, x1, y1, z1, x2, y2, z2, shading_info, normals):
        if shading_info[0] == "wireframe":
            self.scanline_convert_wireframe(x0, y0, z0, x1, y1, z1, x2, y2, z2)
        elif shading_info[0] == "flat":
            self.scanline_convert_flat(x0, y0, z0, x1, y1, z1, x2, y2, z2, shading_info[1], shading_info[2], shading_info[3])
        elif shading_info[0] == "goroud":
            self.scanline_convert_goroud(x0, y0, z0, x1, y1, z1, x2, y2, z2, shading_info[1], shading_info[2], shading_info[3], normals)
        elif shading_info[0] == "phong": 
            self.scanline_convert_phong(x0, y0, z0, x1, y1, z1, x2, y2, z2, shading_info[1], shading_info[2], shading_info[3], normals)
    
    def scanline_convert_wireframe(self, x0, y0, z0, x1, y1, z1, x2, y2, z2):
        self.draw_line_one_color(x0, y0, z0, x1, y1, z1, [255, 255, 255])
        self.draw_line_one_color(x0, y0, z0, x2, y2, z2, [255, 255, 255])
        self.draw_line_one_color(x2, y2, z2, x1, y1, z1, [255, 255, 255])
    
    def scanline_convert_flat(self, x0, y0, z0, x1, y1, z1, x2, y2, z2, consts, ambient, lights):
        col = self.get_color_from_normal_vector(consts, ambient, lights, (vector.Vector(x1 - x0, y1 - y0, z1 - z0)).cross(vector.Vector(x2 - x0, y2 - y0, z2 - z0)), (x0 + x1 + x2) / 3.0, (y0 + y1 + y2) / 3.0, (z0 + z1 + z2) / 3.0)
        self.draw_line_one_color(x0, y0, z0, x1, y1, z1, col)
        self.draw_line_one_color(x0, y0, z0, x2, y2, z2, col)
        self.draw_line_one_color(x2, y2, z2, x1, y1, z1, col)
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
            self.draw_line_one_color(int(x0), y, z0, int(x1), y, z1, col)
            x0 += (top[0] - bot[0]) * 1.0 / (top[1] - bot[1])
            z0 += (top[2] - bot[2]) * 1.0 / (top[1] - bot[1])
            if y < mid[1]:
                x1 += (mid[0] - bot[0]) * 1.0 / (mid[1] - bot[1])
                z1 += (mid[2] - bot[2]) * 1.0 / (mid[1] - bot[1])
            elif y < top[1]:
                x1 += (top[0] - mid[0]) * 1.0 / (top[1] - mid[1])
                z1 += (top[2] - mid[2]) * 1.0 / (top[1] - mid[1])
            y = y + 1
    
    def scanline_convert_goroud(self, x0, y0, z0, x1, y1, z1, x2, y2, z2, consts, ambient, lights, normals):
        col0 = self.get_color_from_normal_vector(consts, ambient, lights, normals[(int(x0), int(y0), int(z0))], x0, y0, z0)
        col1 = self.get_color_from_normal_vector(consts, ambient, lights, normals[(int(x1), int(y1), int(z1))], x1, y1, z1)
        col2 = self.get_color_from_normal_vector(consts, ambient, lights, normals[(int(x2), int(y2), int(z2))], x2, y2, z2)
        self.draw_line_two_colors(x0, y0, z0, x1, y1, z1, col0, col1)
        self.draw_line_two_colors(x0, y0, z0, x2, y2, z2, col0, col2)
        self.draw_line_two_colors(x2, y2, z2, x1, y1, z1, col2, col1)
        [x0, y0, x1, y1, x2, y2] = [int(v) for v in [x0, y0, x1, y1, x2, y2]]
        pts = [(x0, y0, z0, col0), (x1, y1, z1, col1), (x2, y2, z2, col2)]
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
        col0 = bot[3][:]
        col1 = bot[3][:]
        while y < top[1]:
            if y == mid[1]:
                x1 = mid[0]
                z1 = mid[2]
                col1 = mid[3][:]
            self.draw_line_two_colors(int(x0), y, z0, int(x1), y, z1, col0, col1)
            x0 += (top[0] - bot[0]) * 1.0 / (top[1] - bot[1])
            z0 += (top[2] - bot[2]) * 1.0 / (top[1] - bot[1])
            for i in range(3):
                col0[i] += (top[3][i] - bot[3][i]) / (top[1] - bot[1])
            if y < mid[1]:
                x1 += (mid[0] - bot[0]) * 1.0 / (mid[1] - bot[1])
                z1 += (mid[2] - bot[2]) * 1.0 / (mid[1] - bot[1])
                for i in range(3):
                    col1[i] += (mid[3][i] - bot[3][i]) / (mid[1] - bot[1])
            elif y < top[1]:
                x1 += (top[0] - mid[0]) * 1.0 / (top[1] - mid[1])
                z1 += (top[2] - mid[2]) * 1.0 / (top[1] - mid[1])
                for i in range(3):
                    col1[i] += (top[3][i] - mid[3][i]) / (top[1] - mid[1])
            y = y + 1
    
    def scanline_convert_phong(self, x0, y0, z0, x1, y1, z1, x2, y2, z2, consts, ambient, lights, normals):
        norm0 = normals[(int(x0), int(y0), int(z0))].vals
        norm1 = normals[(int(x1), int(y1), int(z1))].vals
        norm2 = normals[(int(x2), int(y2), int(z2))].vals
        self.draw_line_two_normal_vectors(x0, y0, z0, x1, y1, z1, consts, ambient, lights, vector.Vector(*norm0), vector.Vector(*norm1))
        self.draw_line_two_normal_vectors(x0, y0, z0, x2, y2, z2, consts, ambient, lights, vector.Vector(*norm0), vector.Vector(*norm2))
        self.draw_line_two_normal_vectors(x2, y2, z2, x1, y1, z1, consts, ambient, lights, vector.Vector(*norm2), vector.Vector(*norm1))
        [x0, y0, x1, y1, x2, y2] = [int(v) for v in [x0, y0, x1, y1, x2, y2]]
        pts = [(x0, y0, z0, norm0), (x1, y1, z1, norm1), (x2, y2, z2, norm2)]
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
        norm0 = bot[3][:]
        norm1 = bot[3][:]
        while y < top[1]:
            if y == mid[1]:
                x1 = mid[0]
                z1 = mid[2]
                norm1 = mid[3][:]
            self.draw_line_two_normal_vectors(int(x0), y, z0, int(x1), y, z1, consts, ambient, lights, vector.Vector(*norm0), vector.Vector(*norm1))
            x0 += (top[0] - bot[0]) * 1.0 / (top[1] - bot[1])
            z0 += (top[2] - bot[2]) * 1.0 / (top[1] - bot[1])
            for i in range(3):
                norm0[i] += (top[3][i] - bot[3][i]) * 1.0 / (top[1] - bot[1])
            if y < mid[1]:
                x1 += (mid[0] - bot[0]) * 1.0 / (mid[1] - bot[1])
                z1 += (mid[2] - bot[2]) * 1.0 / (mid[1] - bot[1])
                for i in range(3):
                    norm1[i] += (mid[3][i] - bot[3][i]) * 1.0 / (mid[1] - bot[1])
            elif y < top[1]:
                x1 += (top[0] - mid[0]) * 1.0 / (top[1] - mid[1])
                z1 += (top[2] - mid[2]) * 1.0 / (top[1] - mid[1])
                for i in range(3):
                    norm1[i] += (top[3][i] - mid[3][i]) * 1.0 / (top[1] - mid[1])
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
