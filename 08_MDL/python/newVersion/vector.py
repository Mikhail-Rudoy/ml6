class Vector():
    """
    A class used to represent 3-vectors
    """
    
    def __init__(self, x, y, z):
        """
        initializes a vector
        """
        self.vals = [x, y, z]
    
    def dot(self, other):
        """
        This method returns the dot product of the calling 
        vector and the parameter.
        """
        result = 0
        for i in range(3):
            result += self.vals[i] * other.vals[i]
        return result
    
    def cross(self, other):
        """
        This method returns the cross product of the calling 
        vector and the parameter.
        """
        [x0, y0, z0] = self.vals
        [x1, y1, z1] = other.vals
        return [y0 * z1 - y1 * z0, x1 * z0 - x0 * z1, x0 * y1 - x1 * y0]
