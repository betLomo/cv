import numpy as np


def semitone(pix_array):
    height, width, _ = pix_array.shape
    pix_new = np.empty([height, width]).astype(np.uint8)

    for x in range(0, height):
        for y in range(0, width):
            pix_new[x][y] = np.mean(pix_array[x][y])

    return pix_new
