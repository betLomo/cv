"""
Модуль содержить различные вспомогательные функции общего назначения
"""
from PIL import Image
import numpy as np
import time


def picture_to_array(image_path):
    """
    Получает матрицу пикселей из изображения по пути
    :param image_path: путь к исходному изображению
    :return: матрица пикселей
    """
    img = Image.open(image_path)
    img.load()
    return np.array(img)


def array_to_picture(pix, image_path):
    """
    Сохраняет матрицу пикселей как изображение по пути
    :param pix: матрица пикселей
    :param image_path: путь к новому изображению
    :return: void
    """
    img = Image.fromarray(pix)
    img.save(image_path)


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r %2.2f ms' % (method.__name__ + args.__str__(), (te - ts) * 1000))
        return result
    return timed


def pix_invert(pix_normalized, _):
    pix_height = pix_normalized.shape[0]
    pix_width = pix_normalized.shape[1]

    pix_inverted = np.empty([pix_height, pix_width]).astype(np.uint8)

    for x in range(0, pix_height):
        for y in range(0, pix_width):
            pix_inverted[x][y] = 1 if (pix_normalized[x][y] == 0) else 0

    return pix_inverted
