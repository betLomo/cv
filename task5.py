import modules.text_generation as tg
import utils as utils
import modules.signs as s
import numpy as np
import modules.binarization as binary
import modules.semitone as semitone

SAMPLES_PATH = "media/samples/text/"
RESULTS_PATH = "media/results/task5/"


#def save_char_profiles(_img, _rects_img, path):
 #   for (x0, y0, x1, y1) in _rects_img:
  #      subpix = _img[y0:y1, x0:x1]
   #     name = "[%.0f, %.0f, %.0f, %.0f]" % (x0, y0, x1, y1)
    #    _prof_x = fa.calc_image_profile(subpix, 1, 0)[::-1]
     #   _prof_y = fa.calc_image_profile(subpix, 0, 1)
      #  fa.visualize_profile(_prof_x, "horizontal", RESULTS_PATH + path + "/char_profiles/horizontal/" + name + ".png")
       # fa.visualize_profile(_prof_y, "vertical", RESULTS_PATH + path + "/char_profiles/vertical/" + name + ".png")


def get_normalized_image(pix):
    img_grayscale = binary.apply_threshold(semitone.semitone(pix), 128, 1)
    return utils.pix_invert(img_grayscale, 0)


# 1. Подготовить текст из одной строки, пользуясь выбранным алфавитом и теми же параметрами шрифта
tg.generate_img_from_text("ШИРОКАЯ ЭЛЕКТРИФИКАЦИЯ ЮЖНЫХ ГУБЕРНИЙ ДАСТ МОЩНЫЙ ТОЛЧОК ПОДЪЁМУ СЕЛЬСКОГО ХОЗЯЙСТВА", "fonts/arial_italic.ttf", 52)
img_1 = get_normalized_image(utils.picture_to_array(SAMPLES_PATH + "text3.png"))

# 2. Реализовать алгоритм расчёта горизонтального и вертикального профиля изображения
# Профили X и Y
prof_x = s.calc_image_profile(img_1, 1, 0)[::-1]
prof_y = s.calc_image_profile(img_1, 0, 1)
# сохраняем графики профилей в картинках
s.horizontal_profile(prof_x, RESULTS_PATH + "1/line_profiles/horizontal.png")
s.vertical_profile(prof_y, RESULTS_PATH + "1/line_profiles/vertical.png", (25, 5))

# 3. Реализовать алгоритм сегментации символов в строке на основе профилей с прореживанием
#rects_img_1 = s.get_polygon(img_1)
#s.draw_polygons(SAMPLES_PATH + "text3.png", RESULTS_PATH + "/1/bounds.png", rects_img_1)

#for i in range(0, len(poly_img_1)):
   # norm = s.polygon_to_matrix(poly_img_1[i], img_1) * 255
   # utils.array_to_picture(norm, RESULTS_PATH + 'exp/' + str(i) + '.bmp')
    #print(norm)


poly_img_1 = s.get_polygon(img_1)
s.draw_polygons(SAMPLES_PATH + "text3.png", RESULTS_PATH + "/1/bounds.png", poly_img_1)

# (пробуем ещё с изображением с многими строками)
#img_2 = fa.get_normalized_image(utils.pix_from_path(SAMPLES_PATH + "2.png"))
#rects_img_2 = fa.get_polygon(img_2)
#fa.draw_polygons(SAMPLES_PATH + "2.png", RESULTS_PATH + "/2/bounds.png", rects_img_2)

# 4. Построить профили символов выбранного алфавита
#save_char_profiles(img_1, rects_img_1, "/1")
#save_char_profiles(img_2, rects_img_2, "/2")
