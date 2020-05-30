import numpy as np
import math


def get_co_occurrence_matrix(pix, l):
    d = 3
    angles = [0.25 * math.pi, 0.75 * math.pi, 1.25 * math.pi, 1.75 * math.pi]

    height, width = pix.shape
    p = np.zeros([l, l]).astype(np.uint)

    for x in range(0, width):
        for y in range(0, height):
            for a in angles:
                dx = d * round(math.cos(a))
                dy = d * round(math.sin(a))
                _x = x + dx
                _y = y + dy
                if (0 <= _x < width) and (0 <= _y < height):
                    i, j = pix[y][x], pix[_y][_x]
                    p[i][j] = p[i][j] + 1

    return p


def semitone_gradation(pix, l):
    step = 256 / l
    height, width = pix.shape
    result = np.empty([height, width]).astype(np.uint8)

    for x in range(0, height):
        for y in range(0, width):
            result[x, y] = math.floor(pix[x][y] / step)

    return result


def spread_image(pix):
    height, width = pix.shape

    result = np.empty([height, width]).astype(np.uint8)
    max_value, min_value = np.max(pix), np.min(pix[np.nonzero(pix)])

    for x in range(0, height):
        for y in range(0, width):
            result[x, y] = round(pix[x][y] / max_value * 255)

    return result


def av(matrix, axis=0):
    result = 0
    size = matrix.shape[0]
    for i in range(0, size):
        # считаем PJ(i) или PI(j)
        p = 0
        for j in range(0, size):
            p += matrix[i][j] if axis == 0 else matrix[j][i]
        result += i * p

    return result / (size**2)


def sums(matrix):
    result = []
    size = matrix.shape[0]
    for i in range(0, size):
        p = 0
        for j in range(0, size):
            p += matrix[i][j]
        result.append(p)

    return result


def dispersion(matrix, axis=0):
    dis = 0
    m = av(matrix, axis)
    size = matrix.shape[0]

    if axis == 0:
        for i in range(0, size):
            # считаем PJ(i) или PI(j)
            p = 0
            for j in range(0, size):
                p += matrix[i][j]
            dis += p * (i - m)**2
    else:
        for i in range(0, size):
            p = 0
            for j in range(0, size):
                p += matrix[j][i]
            dis += p * (i - m)**2

    return dis
