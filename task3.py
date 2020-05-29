import modules.sobel as sobel
import utils as utils

IMAGES_RESOURCE = "images/resource/3_task/"
IMAGES_RESULT = "images/result/3_task/"


@utils.timeit
def task_sobel(original_path, result_path1, result_path2, result_path3):
    pix_array = utils.picture_to_array(IMAGES_RESOURCE + original_path)
    pix_result1 = sobel.sobelOperator(pix_array)[0]
    pix_result2 = sobel.sobelOperator(pix_array)[1]
    pix_result3 = sobel.sobelOperator(pix_array)[2]
    utils.array_to_picture(pix_result1, IMAGES_RESULT + result_path1)
    utils.array_to_picture(pix_result2, IMAGES_RESULT + result_path2)
    utils.array_to_picture(pix_result3, IMAGES_RESULT + result_path3)

# Оператор Собеля
#task_sobel("MARBLES_BW.bmp", "MARBLES_sobel.bmp", "MARBLES_x.bmp", "MARBLES_y.bmp")
#task_sobel("mountains_BW.bmp", "mountains_sobel.bmp", "mountains_x.bmp", "mountains_y.bmp")
#task_sobel("cat_BW.bmp", "cat_sobel.bmp", "cat_x.bmp", "cat_y.bmp")
#task_sobel("eye_BW.bmp", "eye_sobel.bmp", "eye_x.bmp", "eye_y.bmp")
