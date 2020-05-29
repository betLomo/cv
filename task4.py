import modules.text_generation as text
import utils as utils
import numpy as np
import modules.binarization as binary
import modules.semitone as semitone
import modules.signs as signs
import modules.cvs as cvs_custom

DICTIONARY_PATH = "dictionary"
SYMBOLS_STRING = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЬЭЮЯI"
SAMPLES_PATH = "dictionary/samples/"


def symbols_config_to_pix(dictionary):
    result = {}
    for key in dictionary:
        result[key] = np.array(dictionary[key])
    return result


def pix_config_grayscale(dictionary):
    result = {}
    for key in dictionary:
        result[key] = semitone.semitone(dictionary[key])

    return result


def pix_config_treshold(dictionary):
    result = {}
    for key in dictionary:
        result[key] = binary.apply_threshold(dictionary[key])

    return result


def pix_config_to_path(dictionary, path):
    for key in dictionary:
        utils.array_to_picture(dictionary[key], path + "/" + key + ".png")


def pix_config_to_binary(dictionary):
    result = {}
    for key in dictionary:
        result[key] = binary.apply_threshold(dictionary[key], 128, 1)

    return result


def invert(pix_normalized):
    pix_height = pix_normalized.shape[0]
    pix_width = pix_normalized.shape[1]

    pix_inverted = np.empty([pix_height, pix_width]).astype(np.uint8)

    for x in range(0, pix_height):
        for y in range(0, pix_width):
            pix_inverted[x][y] = 1 if (pix_normalized[x][y] == 0) else 0

    return pix_inverted


def pix_config_invert(dictionary):
    result = {}
    for key in dictionary:
        result[key] = invert(dictionary[key])

    return result


def pix_apply(dictionary, f):
    result = {}
    for key in dictionary:
        result[key] = f(dictionary[key])

    return result


def pix_apply_plot_vertical(dictionary):
    result = {}
    for key in dictionary:
        result[key] = signs.vertical_profile(signs.calc_image_profile(dictionary[key], 0, 1), DICTIONARY_PATH + '/plots_vertical/' + key + '.png')

    return result


def pix_apply_plot_horizontal(dictionary):
    result = {}
    for key in dictionary:
        result[key] = signs.horizontal_profile(signs.calc_image_profile(dictionary[key], 1, 0), DICTIONARY_PATH + '/plots_horizontal/' + key + '.png')

    return result


def pix_crop(dictionary):
    #tmp = "dictionary/tmp/"
    result = {}
    for key in dictionary:
        d = dictionary[key]
        xleft, xright = signs.detect_symbols_in_profile(signs.calc_image_profile_angle(d))[0]
        yleft, yright = signs.detect_strings(signs.calc_image_profile(d, 1, 0), 4)[0]
        ver_dict_cropped = d[:, xleft:xright]
        hor_dict_cropped = ver_dict_cropped[yleft:yright]
        polygon = signs.get_symbol_polygon(hor_dict_cropped, xleft+1, xright+1, yleft, yright)
        result[key] = signs.polygon_to_matrix(polygon, dictionary[key])
        #norm = result[key] * 255
        #utils.array_to_picture(norm, tmp + key + '.bmp')

    return result


# создаём словарь со всеми символами
symbols = symbols_config_to_pix(text.generate_dictionary(SYMBOLS_STRING, "fonts/arial_italic.ttf", 52))

# переводим все символы в полутона
symbols_grayscale = pix_config_grayscale(symbols)

# переводим все символы в ч/б
symbols_threshold = pix_config_treshold(symbols_grayscale)

# сохраняем исходные изображения символов в директорию (один символ - один файл)
pix_config_to_path(symbols_threshold, DICTIONARY_PATH + "/samples")

# нормализуем
symbols_normalized = pix_config_to_binary(symbols_threshold)

# инвертируем чёрное и белое
symbols_final = pix_config_invert(symbols_normalized)

# обрезаем все символы
symbols_crop = pix_crop(symbols_final)

# Вес
symbols_weight = pix_apply(symbols_crop, signs.weight)

# Удельный вес
symbols_specific_weight = pix_apply(symbols_crop, signs.specific_weight)

# Нулевой момент
symbols_zero_moment = pix_apply(symbols_crop, signs.zero_moment)

# Координата х центра тяжести
symbols_center_of_gravity_x = pix_apply(symbols_crop, signs.center_of_gravity_x)

# Координата y центра тяжести
symbols_center_of_gravity_y = pix_apply(symbols_crop, signs.center_of_gravity_y)

# Нормированная координата х центра тяжести
symbols_norm_center_of_gravity_x = pix_apply(symbols_crop, signs.norm_center_of_gravity_x)

# Нормированная координата y центра тяжести
symbols_norm_center_of_gravity_y = pix_apply(symbols_crop, signs.norm_center_of_gravity_y)

# Осевой момент инерции по-горизонтали
symbols_horizontal = pix_apply(symbols_crop, signs.axial_moment_horizontal)

# Осевой момент инерциии по-вертикали
symbols_vertical = pix_apply(symbols_crop, signs.axial_moment_vertical)

# Нормированный осевой момент инерции по-горизонтали
symbols_norm_horizontal = pix_apply(symbols_crop, signs.norm_axial_moment_horizontal)

# Нормированный осевой момент инерции по-вертикали
symbols_norm_vertical = pix_apply(symbols_crop, signs.norm_axial_moment_vertical)

# Сохранение в .cvs файл
cvs_custom.save_model('./dictionary/sign_table.csv', [
        'Символ',
        'Вес',
        'Удельный вес',
        'Центр тяжести (X)',
        'Центр тяжести (Y)',
        'Нормированный центр тяжести (X)',
        'Нормированный центр тяжести (Y)',
        'Горизонтальный осевой момент',
        'Вертикальный осевой момент',
        'Номированный горизонтальный осевой момент',
        'Номированный вертикальный осевой момент',
    ], SYMBOLS_STRING, [
        symbols_weight,
        symbols_specific_weight,
        symbols_center_of_gravity_x, symbols_center_of_gravity_y,
        symbols_norm_center_of_gravity_x, symbols_norm_center_of_gravity_y,
        symbols_horizontal, symbols_vertical,
        symbols_norm_horizontal, symbols_norm_vertical,
    ])

# Профили
pix_apply_plot_horizontal(symbols_final)
pix_apply_plot_vertical(symbols_final)
