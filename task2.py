import modules.conservative_smoothing as smoothing
import utils as utils

IMAGES_RESOURCE = "images/resource/2_task/"
IMAGES_RESULT = "images/result/2_task/"


@utils.timeit
def task_smoothing(original_path, result_path, xor_path):
    pix_array = utils.picture_to_array(IMAGES_RESOURCE + original_path)
    pix_smoothing = smoothing.conservative_smoothing_gray(pix_array, 2)
    utils.array_to_picture(pix_smoothing, IMAGES_RESULT + result_path)
    pix_xor = smoothing.xor(pix_array, pix_smoothing)
    utils.array_to_picture(pix_xor, IMAGES_RESULT + xor_path)


# Фильтрация методом консервативного сглаживания
#task_smoothing("number_BW.bmp", "smooth_number_BW.bmp", "smooth_number_BW_xor.bmp")
#task_smoothing("number_binary.bmp", "smooth_number_binary.bmp", "smooth_number_binary_xor.bmp")
#task_smoothing("virus_binary.bmp", "smooth_virus.bmp", "smooth_virus_xor.bmp")
#task_smoothing("virus_BW.bmp", "smooth_virus_BW.bmp", "smooth_virus_BW_xor.bmp")
#task_smoothing("letter_binary.bmp", "smooth_letter.bmp", "smooth_letter_xor.bmp")
#task_smoothing("letter_BW.bmp", "smooth_letter_BW.bmp", "smooth_letter_BW_xor.bmp")
#task_smoothing("mountains_binary.bmp", "smooth_mountains.bmp", "smooth_mountains_xor.bmp")
