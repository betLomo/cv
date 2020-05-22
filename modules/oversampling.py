import numpy as np
import math
from fractions import Fraction


def func(pix_array, k):
    height, width, _ = pix_array.shape
    height_new = round(height * k)
    width_new = round(width * k)
    pix_new = np.empty([height_new, width_new, 3]).astype(np.uint8)

    for x in range(0, height_new):
        for y in range(0, width_new):
            pix_new[x][y] = pix_array[math.floor(x/k)][math.floor(y/k)]

    return pix_new


# Сжатие (децимация) изображения в N раз;
def decimation(pix_array, n):
    return func(pix_array, 1/n)


# Растяжение (интерполяция) изображения в M раз;
def interpolation(pix_array, m):
    return func(pix_array, m)


# Передискретизация изображения в K=M/N раз путём растяжения и последующего сжатия (в два прохода);
def twice(pix_array, k):
    res = Fraction(k).limit_denominator()
    return decimation(interpolation(pix_array, res.numerator), res.denominator)


# Передискретизация изображения в K раз за один проход.
def once(pix_array, k):
    return interpolation(pix_array, k)
