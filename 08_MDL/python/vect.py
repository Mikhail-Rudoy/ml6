def dot(V1, V2):
    i = 0
    result = 0
    while i < len(V1) and i < len(V2):
        result = result + V1[i] * V2[i]
        i = i + 1
    return result

def cross(V1, V2):
    [x0, y0, z0] = V1
    [x1, y1, z1] = V2
    return [y0 * z1 - y1 * z0, x1 * z0 - x0 * z1, x0 * y1 - x1 * y0]

def vec(P1, P2):
    i = 0
    result = []
    while i < len(P1) and i < len(P2):
        result.append(P2[i] - P1[i])
        i = i + 1
    return result
