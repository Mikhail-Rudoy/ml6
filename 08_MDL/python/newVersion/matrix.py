from screen import *
import math

class Matrix():
    """
    This class represents a mathematical matrix.
    """
    
    def __init__(self, *args):
        """
        This constructor either initializes the width and height of the 
        matrix and sets every value to 0, or copies the given list 
        representation of a matrix into the matrix.
        """
        if len(args) == 2:
            w, h = args
            self.matrix = [[[0.0] * h] for c in range(w)]
        elif len(args) = 1:
            self.matrix = [col[:] for col in args[0]]
        else:
            return NotImplemented
    
    def identity_matrix(d):
        """
        This function returns a new identity matrix of dimensions 
        d by d.
        """
        m = Matrix(0, 0)
        m.matrix = [[float(i == j) for i in range(d)] for j in range(d)]

    def get(self, r, c):
        """
        This method retrieves the value at a particular location
        in the matrix.
        """
        return self.matrix[c][r]
    
    def set(self, r, c, val):
        """
        This method sets the value at a particular location in the
        matrix.
        """
        self.matrix[c][r] = val
    
    def width(self):
        """
        This method returns the width of the matrix.
        """
        return len(self.matrix)
    
    def height(self):
        """
        This method returns the height of the matrix.
        """
        return len(self.matrix) and len(self.matrix[0])
    
    def clone(self):
        """
        This method returns an exact copy of the matrix
        """
        copy = Matrix(0, 0)
        copy.matrix = [col[:] for col in self.matrix]
        return copy
    
    def __str__(self):
        """
        This method converts the matrix to a textual representation
        of its contents.
        """
        result = ""
        for r in range(self.height()):
            for c in range(self.width()):
                result += str(self.get(r, c)) + " "
            result += "\n"
        return result
    
    def __mul__(self, other):
        """
        Overloading the * operator to also signify scalar multiplication
        and matrix multiplication.
        """
        if isinstance(other, Number):
            result = matrix(0, 0)
            result.matrix = [[val * other for val in col] for col in self.matrix]
            return result
        elif isinstance(other, matrix):
            if other.height() != self.width():
                return NotImplemented
            result = Matrix(other.width(), self.height())
            for r in range(result.height()):
                for c in range(result.width()):
                    v = 0
                    for i in range(self.width()):
                        v += self.get(r, i) * other.get(i, c)
                    result.set(r, c, v)
            return result
        else:
            return NotImplemented
    
    def __rmul__(self, other):
        """
        Overloading the * operator to also signify scalar multiplication
        and matrix multiplication.
        """
        if isinstance(other, Number):
            result = matrix(0, 0)
            result.matrix = [[val * other for val in col] for col in self.matrix]
            return result
        elif isinstance(other, matrix):
            if self.height() != other.width():
                return NotImplemented
            result = Matrix(self.width(), other.height())
            for r in range(result.height()):
                for c in range(result.width()):
                    v = 0
                    for i in range(other.width()):
                        v += other.get(r, i) * self.get(i, c)
                    result.set(r, c, v)
            return result
        else:
            return NotImplemented
    
    def __imul__(self, other):"""
        Overloading the *= operator to also signify scalar multiplication
        and matrix multiplication.
        """
        if isinstance(other, Number):
            for r in range(self.height()):
                for c in range(self.width()):
                    self.set(r, c, self.get(r, c) * other)
            return self
        elif isinstance(other, matrix):
            if self.height() != other.width():
                return NotImplemented
            result = [[0.0] * other.height() for c in range(self.width())]
            for r in range(other.height()):
                for c in range(self.width()):
                    for i in range(other.width()):
                        result[c][r] += other.get(r, i) * self.get(i, c)
            self.matrix = result
            return self
        else:
            return NotImplemented


class Transformation():
    """
    This is a simple utility class for generating transformation.
    matrices.
    """
    
    def ident():
        """
        This function returns a new identity transformation matrix.
        """
        return Matrix.identity_matrix(4)

    def move(a, b, c):
        """
        This function returns a new translation matrix.
        """
        result = Matrix(0, 0)
        result.matrix = [[1.0, 0.0, 0.0, 0.0], \
                         [0.0, 1.0, 0.0, 0.0], \
                         [0.0, 0.0, 1.0, 0.0], \
                         [a, b, c, 1.0]]
    
    def scale(a, b, c):
        """
        This function returns a new scaling matrix.
        """
        result = Matrix(0, 0)
        result.matrix = [[a, 0.0, 0.0, 0.0], \
                         [0.0, b, 0.0, 0.0], \
                         [0.0, 0.0, c, 0.0], \
                         [0.0, 0.0, 0.0, 1.0]]
    
    def rotate(axis, theta):
        """
        This function returns a new rotation matrix.
        """
        result = Matrix(0, 0)
        r = theta * 3.14159265358979323 / 180
        if axis == "x":
            result.matrix = [[1.0, 0.0, 0.0, 0.0], \
                             [0.0, math.cos(r), math.sin(r), 0.0], \
                             [0.0, 0.0 - math.sin(r), math.cos(r), 0.0], \
                             [0.0, 0.0, 0.0, 1.0]]
        elif axis == "y":
            result.matrix = [[math.cos(r), 0.0, math.sin(r), 0.0], \
                             [0.0, 1.0, 0.0, 0.0], \
                             [0.0 - math.sin(r), 0.0, math.cos(r), 0.0], \
                             [0.0, 0.0, 0.0, 1.0]]
        elif axis == "z":
            result.matrix = [[math.cos(r), math.sin(r), 0.0, 0.0], \
                             [0.0 - math.sin(r), math.cos(r), 0.0, 0.0], \
                             [0.0, 0.0, 1.0, 0.0], \
                             [0.0, 0.0, 0.0, 1.0]]
        else:
            return NotImplemented
        return result

class PointMatrix(Matrix):
    """
    Utilization of Matrix class to store three dimensional points.
    """
    
    def __init__(self):
        """
        This constructor initializes an empty matrix.
        """
        self.matrix = []
    
    def add_point(self, x, y, z):
        """
        This method adds a point to the matrix.
        """
        self.matrix.append([x, y, z, 1.0])
    
    def add_points(self, *points):
        """
        This method adds several points to the matrix.
        """
        for p in points:
            self.matrix.append(p + [1.0])

class EdgeMatrix(PointMatrix):
    """
    A matrix which stores edges as pairs of points.
    """
    
    def __init__(self):
        """
        This constructor initializes an empty matrix.
        """
        self.matrix = []
    
    def add_edge(self, x0, y0, z0, x1, y1, z1):
        """
        This method adds an edge to the matrix.
        """
        self.matrix.append([x0, y0, z0, 1])
        self.matrix.append([x1, y1, z1, 1])
    
    def add_circle(self, cx, cy, r, STEPS = 20):
        """
        This method adds edges that approximate a circle.
        """
        l = []
        for n in range(STEPS + 1):
            t0 = (1.0 * n) / STEPS
            x0 = cx + r * math.cos(math.pi * 2 * t0)
            y0 = cy + r * math.sin(math.pi * 2 * t0)
            l.append([x0, y0, 0])
        for i in range(STEPS):
            [x0, y0, z0] = l[i]
            [x1, y1, z1] = l[i + 1]
            self.add_edge(x0, y0, z0, x1, y1, z1)
    
    def add_hermite_curve(self, x0, y0, z0, x1, y1, z1, x2, y2, z2, x3, y3, z3, STEPS = 80):
        """
        This method adds edges that approximate a three dimensional
        cubic hermite curve.
        """
        C = Matrix([[2, -3, 0, 1], [-2, 3, 0, 0], [1, -2, 1, 0], [1, -1, 0, 0]]) * \
            Matrix([[x0, x2, x1 - x0, x3 - x2], [y0, y2, y1 - y0, y3 - y2], [z0, z2, z1 - z0, z3 - z2]])
        l = []
        for n in range(STEPS + 1):
            t = (n * 1.0) / STEPS
            l.append(Matrix([[t * t * t], [t * t], [t], [1]]) * C)
        for i in range(STEPS):
            [[x0], [y0], [z0]] = l[i]
            [[x1], [y1], [z1]] = l[i + 1]
            self.add_edge(x0, y0, z0, x1, y1, z1)
    
    def add_bezier_curve(self, x0, y0, z0, x1, y1, z1, x2, y2, z2, x3, y3, z3, STEPS = 80):
        """
        This method adds edges that approximate a three dimensional
        cubic bezier curve.
        """
        C = Matrix([[1, -3, 3, -1], [0, 3, -6, 3], [0, 0, 3, -3], [0, 0, 0, 1]]) * \
            Matrix([[x0, x1, x2, x3], [y0, y1, y2, y3], [z0, z1, z2, z3]])
        l = []
        for n in range(STEPS + 1):
            t = (n * 1.0) / STEPS
            l.append(Matrix([[t * t * t], [t * t], [t], [1]]) * C)
        for i in range(STEPS):
            [[x0], [y0], [z0]] = l[i]
            [[x1], [y1], [z1]] = l[i + 1]
            self.add_edge(x0, y0, z0, x1, y1, z1)
    
    def add_sphere(self, cx, cy, cz, r, whichlines = "d", STEPS = None):
        """
        This method adds edges that approximate a mesh of a sphere.
        """
        if STEPS == None:
            STEPS = [int(R / 3), int(r / 3)]
        costheta = []
        sintheta = []
        cosphi = []
        sinphi = []
        for n in range(STEPS[0] + 1):
            theta = (2 * n * 3.1415926535899793238462643383279) / STEPS[0]
            costheta.append(math.cos(theta))
            sintheta.append(math.sin(theta))
        for n in range(STEPS[1] + 1):
            phi = (n * 3.1415926535899793238462643383279) / STEPS[1]
            cosphi.append(math.cos(phi))
            sinphi.append(math.sin(phi))
        points = []
        for row in range(STEPS[1] + 1):
            tmp = []
            for col in range(STEPS[0] + 1):
                tmp.append([r * sinphi[row] * sintheta[col] + cx, \
                            r * cosphi[row] + cy, \
                            r * sinphi[row] * costheta[col] + cz])
            points.append(tmp)
        for row in range(STEPS[1]):
            for col in range(STEPS[0]):
                if whichlines in "bd":
                    [x0, y0, z0] = points[row][col]
                    [x1, y1, z1] = points[row + 1][col + 1]
                    self.add_edge(x0, y0, z0, x1, y1, z1)
                    [x0, y0, z0] = points[row][col + 1]
                    [x1, y1, z1] = points[row + 1][col]
                    self.add_edge(x0, y0, z0, x1, y1, z1)
                if whichlines in "bl":
                    [x0, y0, z0] = points[row][col]
                    [x1, y1, z1] = points[row][col + 1]
                    self.add_edge(x0, y0, z0, x1, y1, z1)
                    [x0, y0, z0] = points[row][col]
                    [x1, y1, z1] = points[row + 1][col]
                    self.add_edge(x0, y0, z0, x1, y1, z1)
    
    def add_torus(self, cx, cy, cz, r, R, whichlines = "d", STEPS = None):
        """
        This method adds edges that approximate a mesh of a torus.
        """
        if STEPS == None:
            STEPS = [int(r / 5), int(r / 5)]
        costheta = []
        sintheta = []
        cosphi = []
        sinphi = []
        for n in range(STEPS[0] + 1):
            theta = (2 * n * 3.1415926535899793238462643383279) / STEPS[0]
            costheta.append(math.cos(theta))
            sintheta.append(math.sin(theta))
        for n in range(STEPS[1] + 1):
            phi = (2 * n * 3.1415926535899793238462643383279) / STEPS[1]
            cosphi.append(math.cos(phi))
            sinphi.append(math.sin(phi))
        points = []
        for row in range(STEPS[1] + 1):
            tmp = []
            for col in range(STEPS[0] + 1):
                tmp.append([(r * sinphi[row] + R) * sintheta[col] + cx, \
                            r * cosphi[row] + cy, \
                            (r * sinphi[row] + R) * costheta[col] + cz])
            points.append(tmp)
        for row in range(STEPS[1]):
            for col in range(STEPS[0]):
                if whichlines in "bd":
                    [x0, y0, z0] = points[row][col]
                    [x1, y1, z1] = points[row + 1][col + 1]
                    self.add_edge(x0, y0, z0, x1, y1, z1)
                    [x0, y0, z0] = points[row][col + 1]
                    [x1, y1, z1] = points[row + 1][col]
                    self.add_edge(x0, y0, z0, x1, y1, z1)
                if whichlines in "bl":
                    [x0, y0, z0] = points[row][col]
                    [x1, y1, z1] = points[row][col + 1]
                    self.add_edge(x0, y0, z0, x1, y1, z1)
                    [x0, y0, z0] = points[row][col]
                    [x1, y1, z1] = points[row + 1][col]
                    self.add_edge(x0, y0, z0, x1, y1, z1)
    
    def add_box(self, x0, y0, z0, x1, y1, z1, STEPS = [1, 1, 1]):
        """
        This method adds edges that approximate a box mesh.
        """
        for n in range(STEPS[0] + 1):
            t = (1.0 * n) / STEPS[0]
            xmid = t * x0 + (1 - t) * x1
            self.add_edge(xmid, y0, z0, xmid, y0, z1)
            self.add_edge(xmid, y1, z0, xmid, y1, z1)
            self.add_edge(xmid, y0, z0, xmid, y1, z0)
            self.add_edge(xmid, y0, z1, xmid, y1, z1)
        for n in range(STEPS[1] + 1):
            t = (1.0 * n) / STEPS[1]
            ymid = t * y0 + (1 - t) * y1
            self.add_edge(x0, ymid, z0, x0, ymid, z1)
            self.add_edge(x1, ymid, z0, x1, ymid, z1)
            self.add_edge(x0, ymid, z0, x1, ymid, z0)
            self.add_edge(x0, ymid, z1, x1, ymid, z1)
        for n in range(STEPS[2] + 1):
            t = (1.0 * n) / STEPS[2]
            zmid = t * z0 + (1 - t) * z1
            self.add_edge(x0, y0, zmid, x1, y0, zmid)
            self.add_edge(x0, y1, zmid, x1, y1, zmid)
            self.add_edge(x0, y0, zmid, x0, y1, zmid)
            self.add_edge(x1, y0, zmid, x1, y1, zmid)

class FaceMatrix(PointMatrix):
    """
    A matrix which stores faces as triples of points.
    """
    
    def __init__(self):
        """
        This constructor creates an empty matrix.
        """
        self.matrix = []
    
    def add_face(self, x0, y0, z0, x1, y1, z1, x2, y2, z2):
        """
        This method adds a face to the matrix.
        """
        matrix.append([x0, y0, z0, 1])
        matrix.append([x1, y1, z1, 1])
        matrix.append([x2, y2, z2, 1])
    
    def add_sphere(self, cx, cy, cz, r, STEPS = None):
        """
        This method adds faces approximating a sphere to the matrix.
        """
        if STEPS == None:
            STEPS = [int(r / 5), int(r / 5)]
        costheta = []
        sintheta = []
        cosphi = []
        sinphi = []
        for n in range(STEPS[0] + 1):
            theta = (2 * n * 3.1415926535899793238462643383279) / STEPS[0]
            costheta.append(math.cos(theta))
            sintheta.append(math.sin(theta))
        for n in range(STEPS[1] + 1):
            phi = (n * 3.1415926535899793238462643383279) / STEPS[1]
            cosphi.append(math.cos(phi))
            sinphi.append(math.sin(phi))
        points = []
        for row in range(STEPS[1] + 1):
            tmp = []
            for col in range(STEPS[0] + 1):
                tmp.append([r * sinphi[row] * sintheta[col] + cx, \
                            r * cosphi[row] + cy, \
                            r * sinphi[row] * costheta[col] + cz])
            points.append(tmp)
        for row in range(STEPS[1]):
            for col in range(STEPS[0]):
                [x0, y0, z0] = points[row][col]
                [x1, y1, z1] = points[row + 1][col]
                [x2, y2, z2] = points[row + 1][col + 1]
                [x3, y3, z3] = points[row][col + 1]
                self.add_face(x0, y0, z0, x1, y1, z1, x2, y2, z2)
                self.add_face(x0, y0, z0, x2, y2, z2, x3, y3, z3)
    
    def add_torus(self, cx, cy, cz, r, R, STEPS = None):
        """
        This method adds faces approximating a torus to the matrix.
        """
        if STEPS == None:
            STEPS = [int(R / 3), int(r / 3)]
        costheta = []
        sintheta = []
        cosphi = []
        sinphi = []
        for n in range(STEPS[0] + 1):
            theta = (2 * n * 3.1415926535899793238462643383279) / STEPS[0]
            costheta.append(math.cos(theta))
            sintheta.append(math.sin(theta))
        for n in range(STEPS[1] + 1):
            phi = (2 * n * 3.1415926535899793238462643383279) / STEPS[1]
            cosphi.append(math.cos(phi))
            sinphi.append(math.sin(phi))
        points = []
        for row in range(STEPS[1] + 1):
            tmp = []
            for col in range(STEPS[0] + 1):
                tmp.append([(r * sinphi[row] + R) * sintheta[col] + cx, \
                            r * cosphi[row] + cy, \
                            (r * sinphi[row] + R) * costheta[col] + cz])
            points.append(tmp)
        for row in range(STEPS[1]):
            for col in range(STEPS[0]):
                [x0, y0, z0] = points[row][col]
                [x1, y1, z1] = points[row + 1][col]
                [x2, y2, z2] = points[row + 1][col + 1]
                [x3, y3, z3] = points[row][col + 1]
                self.add_face(x0, y0, z0, x1, y1, z1, x2, y2, z2)
                self.add_face(x0, y0, z0, x2, y2, z2, x3, y3, z3)
    
    def add_box(self, x0, y0, z0, x1, y1, z1):
        """
        This method adds the faces of a box to the matrix.
        """
        [x0, x1] = sorted([x0, x1])
        [y0, y1] = sorted([y0, y1])
        [z0, z1] = sorted([z0, z1])
        self.add_face(x0, y0, z0, x0, y1, z0, x1, y1, z0)
        self.add_face(x0, y0, z0, x1, y1, z0, x1, y0, z0)
        self.add_face(x1, y0, z0, x1, y1, z0, x1, y1, z1)
        self.add_face(x1, y0, z0, x1, y1, z1, x1, y0, z1)
        self.add_face(x1, y0, z1, x1, y1, z1, x0, y1, z1)
        self.add_face(x1, y0, z1, x0, y1, z1, x0, y0, z1)
        self.add_face(x0, y0, z1, x0, y1, z1, x0, y1, z0)
        self.add_face(x0, y0, z1, x0, y1, z0, x0, y0, z0)
        self.add_face(x0, y0, z1, x0, y0, z0, x1, y0, z0)
        self.add_face(x0, y0, z1, x1, y0, z0, x1, y0, z1)
        self.add_face(x0, y1, z0, x0, y1, z1, x1, y1, z1)
        self.add_face(x0, y1, z0, x1, y1, z1, x1, y1, z0)
