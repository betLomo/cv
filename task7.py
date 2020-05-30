import modules.texture_analysis as t
import utils as u
import modules.semitone as semitone

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
    u.array_to_picture(pix_semitone, IMAGES_RESULT + result_path + "semitone.png")

    co_occurrence_matrix = t.get_co_occurrence_matrix(pix_semitone)
    spread_image = t.norm_matrix(co_occurrence_matrix)

    dis_i = t.dispersion(spread_image, 0)
    dis_j = t.dispersion(spread_image, 1)
    save_to_txt(dis_i, dis_j, IMAGES_RESULT + result_path + "features.txt")

    u.array_to_picture(spread_image, IMAGES_RESULT + result_path + "visualized.png")


texture("water.jpg", "water/")
texture("grass.jpg", "grass/")
texture("metal.jpg", "metal/")
texture("rust.jpg", "rust/")
texture("soil.jpg", "soil/")
texture("tree.jpeg", "tree/")
