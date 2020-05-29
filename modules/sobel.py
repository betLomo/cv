import numpy as np


def sobelOperator(img):
    container = np.copy(img)
    container2 = np.copy(img)
    container3 = np.copy(img)
    size = container.shape
    for i in range(1, size[0] - 1):
        for j in range(1, size[1] - 1):
            gx = (img[i - 1][j - 1] + 2*img[i][j - 1] + img[i + 1][j - 1]) - (img[i - 1][j + 1] + 2*img[i][j + 1] +
                                                                              img[i + 1][j + 1])
            gy = (img[i - 1][j - 1] + 2*img[i - 1][j] + img[i - 1][j + 1]) - (img[i + 1][j - 1] + 2*img[i + 1][j] +
                                                                              img[i + 1][j + 1])

            container[i][j] = min(255, np.abs(gx) + np.abs(gy))
            container2[i][j] = min(255, np.abs(gx) + np.abs(128))
            container3[i][j] = min(255, np.abs(128) + np.abs(gy))

    return [container, container2, container3]
