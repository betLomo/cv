import modules.oversampling as oversampling
import modules.semitone as semitone
import modules.binarization as binarization
import utils as utils

IMAGES = "images/sobel/"


@utils.timeit
def task_interpolation(original_path, result_path, n):
    pix_array = utils.picture_to_array(IMAGES + original_path)
    pix_interpolated = oversampling.interpolation(pix_array, n)
    utils.array_to_picture(pix_interpolated, IMAGES + result_path)


@utils.timeit
def task_decimation(original_path, result_path, m):
    pix_array = utils.picture_to_array(IMAGES + original_path)
    pix_decimated = oversampling.decimation(pix_array, m)
    utils.array_to_picture(pix_decimated, IMAGES + result_path)


@utils.timeit
def task_oversample_twice(original_path, result_path, ratio):
    pix_array = utils.picture_to_array(IMAGES + original_path)
    pix_twice = oversampling.twice(pix_array, ratio)
    utils.array_to_picture(pix_twice, IMAGES + result_path)


@utils.timeit
def task_oversample_once(original_path, result_path, ratio):
    pix_array = utils.picture_to_array(IMAGES + original_path)
    pix_once = oversampling.once(pix_array, ratio)
    utils.array_to_picture(pix_once, IMAGES + result_path)


@utils.timeit
def task_semitone(original_path, result_path):
    pix_array = utils.picture_to_array(IMAGES + original_path)
    pix_semitone = semitone.semitone(pix_array)
    utils.array_to_picture(pix_semitone, IMAGES + result_path)


@utils.timeit
def task_threshold(sample_path, result_path):
    pix_array = utils.picture_to_array(IMAGES + sample_path)
    #pix_semitone = semitone.semitone(pix_array)
    pix_threshold = binarization.apply_threshold(pix_array, 128)
    utils.array_to_picture(pix_threshold, IMAGES + result_path)


#task_interpolation("screen.bmp", "screen_large.bmp", 6)
#task_decimation("screen.bmp", "screen_small.bmp", 2)
#task_oversample_twice("screen.bmp", "screen_twice.bmp", 2.8)
#task_oversample_once("screen.bmp", "screen_once.bmp", 2.8)
#task_semitone("eye.jpeg", "eye_BW.bmp")
task_threshold("cat_sobel.bmp", "car_sobel_binary.bmp")
task_threshold("eye_sobel.bmp", "eye_sobel_binary.bmp")
task_threshold("mountains_sobel.bmp", "mountains_sobel_binary.bmp")
task_threshold("MARBLES_sobel.bmp", "MARBLES_sobel_binary.bmp")
