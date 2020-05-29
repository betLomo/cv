import modules.oversampling as oversampling
import modules.semitone as semitone
import modules.binarization as binarization
import utils as utils

IMAGES_RESOURCE = "images/resource/1_task/"
IMAGES_RESULT = "images/result/1_task/"


@utils.timeit
def task_interpolation(original_path, result_path, n):
    pix_array = utils.picture_to_array(IMAGES_RESOURCE + original_path)
    pix_interpolated = oversampling.interpolation(pix_array, n)
    utils.array_to_picture(pix_interpolated, IMAGES_RESULT + result_path)


@utils.timeit
def task_decimation(original_path, result_path, m):
    pix_array = utils.picture_to_array(IMAGES_RESOURCE + original_path)
    pix_decimated = oversampling.decimation(pix_array, m)
    utils.array_to_picture(pix_decimated, IMAGES_RESULT + result_path)


@utils.timeit
def task_oversample_twice(original_path, result_path, ratio):
    pix_array = utils.picture_to_array(IMAGES_RESOURCE + original_path)
    pix_twice = oversampling.twice(pix_array, ratio)
    utils.array_to_picture(pix_twice, IMAGES_RESULT + result_path)


@utils.timeit
def task_oversample_once(original_path, result_path, ratio):
    pix_array = utils.picture_to_array(IMAGES_RESOURCE + original_path)
    pix_once = oversampling.once(pix_array, ratio)
    utils.array_to_picture(pix_once, IMAGES_RESULT + result_path)


@utils.timeit
def task_semitone(original_path, result_path):
    pix_array = utils.picture_to_array(IMAGES_RESOURCE + original_path)
    pix_semitone = semitone.semitone(pix_array)
    utils.array_to_picture(pix_semitone, IMAGES_RESULT + result_path)


@utils.timeit
def task_threshold(sample_path, result_path):
    pix_array = utils.picture_to_array(IMAGES_RESOURCE + sample_path)
    semitone_arr = semitone.semitone(pix_array)
    threshold = binarization.bernsen_threshold(semitone_arr)
    pix_threshold = binarization.apply_threshold(semitone_arr, threshold)
    utils.array_to_picture(pix_threshold, IMAGES_RESULT + result_path)


# Интерполяция
#task_interpolation("screen.bmp", "screen_large.bmp", 6)

# Децимация
#task_decimation("screen.bmp", "screen_small.bmp", 2)

# Передискретизация в 2 подхода
#task_oversample_twice("screen.bmp", "screen_twice.bmp", 2.8)

# Передискретизация в 1 подход
#task_oversample_once("screen.bmp", "screen_once.bmp", 2.8)

# Полутоновое изображение
#task_semitone("eye.jpeg", "eye_BW.bmp")
#task_semitone("cat.jpg", "cat_BW.bmp")
#task_semitone("mountains.jpeg", "mountains_BW.bmp")
#task_semitone("screen.bmp", "screen_BW.bmp")

# Улучшенный алгоритм адаптивной бинаризации Бернсена
#task_threshold("eye.jpeg", "eye_binary.bmp")
#task_threshold("cat.jpg", "cat_binary.bmp")
#task_threshold("mountains.jpeg", "mountains_binary.bmp")
#task_threshold("screen.bmp", "screen_binary.bmp")
