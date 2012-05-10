import math, os

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
        for r in range(h):
            self.__pixels__ = self.__pixels__ + [[]]
            for c in range(w):
                self.__pixels__[r] = self.__pixels__[r] + [black[:]]
    
    def save(self, filename = None):
        """
        This method saves the screen to a filename.
        If no filename is specified, the ultimate filename used 
        by the screen object is used.
        """
        if filename == None:
            filename = self.__filename__
            if filename == None:
                raise TypeError("no file specified")
        self.__filename__ = filename
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
    
    def display(source = None):
        """
        This function displays the given image file on screen.
        If the function is called with a screen or as a method, 
        the file used is the last file that screen was saved to.
        If a filename is specified, that file is displayed.
        """
        if isinstance(source, basestring):
            filename = source
        elif isinstance(source, Screen):
            filename = source.__filename__
        else:
            filename = None
        if filename == None:
            raise TypeError("no file specified")
        if os.fork():
            os.wait()
        else:
            os.system("display " + filename)
            exit()
    
    def set(self, x, y, col):
        """
        This method draws a color to a particular pixel of the 
        screen.
        """
        c, r = int(x), int(y)
        if r < len(self.__pixels__) and r >= 0 and \
                c >= 0 and c < len(self.__pixels__[r]):
            self.__pixels__[r][c] = col
    
    def get(self, x, y):
        """
        This method returns the color currently occupying the given
        pixel.
        """
        c, r = int(x), int(y)
        if r < len(self.__pixels__) and r >= 0 and \
                c >= 0 and c < len(self.__pixels__[r]):
            return self.__pixels__[r][c]
    
    def draw_line(self, x0, y0, x1, y1, col):
        """
        This method draws a line between two points on the screen.
        """
        dx = x1 - x0
        dy = y1 - y0
        if dx + dy < 0:
            dx = 0 - dx
            dy = 0 - dy
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        if dx == 0:
            y = y0
            while y <= y1:
                self.set(x0, y, col)
                y = y + 1
        elif dy == 0:
            x = x0
            while x <= x1:
                self.set(x, y0, col)
                x = x + 1
        elif dy < 0:
            d = 0
            x = x0
            y = y0
            while x <= x1:
                self.set(x, y, col)
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
                self.set(x, y, col)
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
                self.set(x, y, col)
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
                self.set(x, y, col)
                if d > 0:
                    x = x + 1
                    d = d - dy
                y = y + 1
                d = d + dx
