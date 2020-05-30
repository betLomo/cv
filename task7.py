import modules.texture_analysis as t
import utils as u
import modules.semitone as semitone
import modules.signs as s

IMAGES_RESOURCE = "images/resource/7_task/"
IMAGES_RESULT = "images/result/7_task/"


def save_to_txt(dis_i, dis_j, path):
    file = open(path, "a")
    file.truncate(0)
    file.write("dis_i=" + str(dis_i) + "\n")
    file.write("dis_j=" + str(dis_j) + "\n")
    file.close()


@u.timeit
def texture(sample_path, result_path):
    pix = u.picture_to_array(IMAGES_RESOURCE + sample_path)
    pix_semitone = semitone.semitone(pix)
    # градации яркостей
    gradation_matrix = t.semitone_gradation(pix_semitone, 255)
    co_occurrence_matrix = t.get_co_occurrence_matrix(gradation_matrix, 255)
    # Дисперсия
    dis_i = t.dispersion(co_occurrence_matrix, 0)
    dis_j = t.dispersion(co_occurrence_matrix, 1)
    save_to_txt(dis_i, dis_j, IMAGES_RESULT + result_path + "features.txt")

    # Гистаграмма
    sums = t.sums(co_occurrence_matrix)
    s.vertical_profile(sums, IMAGES_RESULT + result_path + "histogram.png", (20.0, 5.0))


    spread_image = t.spread_image(co_occurrence_matrix)
    u.array_to_picture(spread_image, IMAGES_RESULT + result_path + "visualized.png")


texture("water.jpg", "water/")
texture("grass.jpg", "grass/")
texture("metal.jpg", "metal/")
texture("rust.jpg", "rust/")
texture("soil.jpg", "soil/")
texture("tree.jpeg", "tree/")
