import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from PIL import ImageDraw

import math


def weight(pix_arr):
    w = 0
    size = pix_arr.shape
    for i in range(0, size[0]):
        for j in range(0, size[1]):
            w += pix_arr[i][j]

    return w


def specific_weight(pix_arr):
    size = pix_arr.shape
    return weight(pix_arr) / (size[0] * size[1])


def calc_moment(pix_arr, p, q):
    moment = 0

    size = pix_arr.shape
    for i in range(0, size[0]):
        for j in range(0, size[1]):
            moment += pix_arr[i][j] * (i**p) * (j**q)

    return moment


def zero_moment(pix_arr):
    return calc_moment(pix_arr, 0, 0)


def center_of_gravity_x(pix_arr):
    return calc_moment(pix_arr, 1, 0) / zero_moment(pix_arr)


def center_of_gravity_y(pix_arr):
    return calc_moment(pix_arr, 0, 1) / zero_moment(pix_arr)


def norm_center_of_gravity_x(pix_arr):
    return (center_of_gravity_x(pix_arr) - 1) / (pix_arr.shape[0] - 1)


def norm_center_of_gravity_y(pix_arr):
    return (center_of_gravity_y(pix_arr) - 1) / (pix_arr.shape[1] - 1)


def axial_moment_horizontal(pix_arr):
    axial_moment_x = 0
    center_y = center_of_gravity_y(pix_arr)

    size = pix_arr.shape
    for i in range(0, size[0]):
        for j in range(0, size[1]):
            axial_moment_x += pix_arr[i][j] * (center_y - j)**2

    return axial_moment_x


def axial_moment_vertical(pix_arr):
    axial_moment_y = 0
    center_x = center_of_gravity_x(pix_arr)

    size = pix_arr.shape
    for i in range(0, size[0]):
        for j in range(0, size[1]):
            axial_moment_y += pix_arr[i][j] * (center_x - i)**2

    return axial_moment_y


def norm_axial_moment_horizontal(pix_arr):
    return axial_moment_horizontal(pix_arr) / (weight(pix_arr)**2)


def norm_axial_moment_vertical(pix_arr):
    return axial_moment_vertical(pix_arr) / (weight(pix_arr)**2)


def calc_image_profile(pix, p=0, q=0):
    pix_height = pix.shape[0]
    pix_width = pix.shape[1]

    profile = []

    if p == 1:
        for x in range(0, pix_height):
            current_sum = 0
            for y in range(0, pix_width):
                current_sum += pix[x][y]
            profile.append(current_sum)
    elif q == 1:
        for y in range(0, pix_width):
            current_sum = 0
            for x in range(0, pix_height):
                current_sum += pix[x][y]
            profile.append(current_sum)

    return profile


def calc_image_profile_angle(pix):
    pix_height = pix.shape[0]
    pix_width = pix.shape[1]
    ctg = 27/130

    profile = []

    for y in range(math.ceil(pix_height * ctg), pix_width):
        current_sum = 0
        for x in range(0, pix_height):
            current_sum += pix[x][y - math.ceil(ctg * x)]
        profile.append(current_sum)

    return profile


def horizontal_profile(profile, path, figsize=(5.0, 5.0)):
    pts = np.arange(len(profile))
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(profile[::-1], pts)
    ax.set_yticklabels([])
    fig.savefig(path)
    plt.close()


def vertical_profile(profile, path, figsize=(5.0, 5.0)):
    pts = np.arange(len(profile))
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(pts, profile)
    ax.set_xticklabels([])
    fig.savefig(path)
    plt.close()


# Блок про распознавание
def detect_symbols_in_profile(p):
    bounds = []

    bound_start = None
    for i in range(0, len(p)):
        if (p[i - 1] == 0 and p[i] != 0) or i == 0:
            bound_start = i
        elif (p[i - 1] != 0 and p[i] == 0) or (i == len(p) - 1 and bound_start is not None):
            bounds.append((bound_start, i))
            bound_start = None

    return bounds


def detect_strings(p, n):
    bounds = []
    white_counter = 1

    bound_start = None

    for i in range(0, len(p)):
        if p[i] == 0 and bound_start is not None:
            if p[i - 1] != 0:
                white_counter = 1
            else:
                white_counter = white_counter + 1

            if white_counter == n:
                bounds.append((bound_start, i - white_counter))
                bound_start = None
        elif p[i] != 0:
            if bound_start is None:
                bound_start = i

        #    if white_counter > n:
        #        bound_start = i
        #    white_counter = 0
        #elif i == len(p) - 1 and bound_start is not None:
        #    bounds.append((bound_start, i))
        #    bound_start = None

    #print(bounds)
    return bounds


def draw_polygons(source_path, result_path, rects):
    """
    :param source_path:
    :param result_path:
    :param rects: [x0, y0, x1, y1]
    :return:
    """
    img = Image.open(source_path)
    img.load()
    draw = ImageDraw.Draw(img)
    for i in range(0, len(rects)):
        draw.polygon(rects[i], outline="red")
        #draw.rectangle(rects[i], outline="red")

    img.save(result_path)


def draw_lines(source_path, result_path, lines):
    img = Image.open(source_path)
    img.load()
    draw = ImageDraw.Draw(img)
    for i in range(0, len(lines)):
        draw.line(lines[i], fill="red", width=1)

    img.save(result_path)


def get_polygon(pix):
    result = []
    prof_x = calc_image_profile(pix, 1, 0)
    horizontal_bounds = detect_strings(prof_x, 2)
    for i in range(0, len(horizontal_bounds)):
        (y0, y1) = horizontal_bounds[i]
        line_pix = pix[y0:y1]
        prof_y = calc_image_profile_angle(line_pix)
        vertical_bounds = detect_symbols_in_profile(prof_y)
        for j in range(0, len(vertical_bounds)):
            (x0, x1) = vertical_bounds[j]
            char_pix = line_pix[:, x0:x1]
            result.append(get_symbol_polygon(char_pix, x0, x1, y0, y1))

    return result


# Конвертация параллелограмма в обычную матрицу
def polygon_to_matrix(arr, pix):
    a, b, c,  d = arr
    (ax, ay) = a
    (bx, by) = b
    (dx, dy) = d
    ctg = 27/130

    w = bx - ax
    result = []

    for i in range(ay, dy):
        row = []
        x0 = ax - round((i - ay) * ctg)
        for j in range(x0, x0 + w):
            row.append(pix[i][j])
        result.append(row)

    return np.array(result)


def get_symbol_polygon(char_pix, x0=None, x1=None, y0=None, y1=None):
    # Котангенс наклона курсива (был высчитан вручную для arial_italic.ttf)
    ctg = (27 / 130)

    if x0 is None:
        x0 = 0
    if y0 is None:
        y0 = 0
    if x1 is None:
        x1 = char_pix.shape[1]
    if y1 is None:
        y1 = char_pix.shape[0]

    char_prof_x = calc_image_profile(char_pix, 1, 0)
    char_bounds = detect_symbols_in_profile(char_prof_x)
    (fy0, fy1) = (char_bounds[0][0], char_bounds[-1][1])
    ver_shift = y1 - (y0 + fy1)
    hor_shift = round(ver_shift * ctg)
    bottom_left = (x0 + hor_shift, y0 + fy1)
    bottom_right = (x1 + hor_shift, y0 + fy1)
    top_left = (x0 + round(ctg * (fy1 - fy0)) + hor_shift, y0 + fy0)
    top_right = (x1 + round(ctg * (fy1 - fy0)) + hor_shift, y0 + fy0)

    return [top_left, top_right, bottom_right, bottom_left]


def get_pix_hypothesis(pix, model_dict):
    pix_polygons = get_polygon(pix)
    res = []

    for poly in pix_polygons:
        symbol = polygon_to_matrix(poly, pix)
        weight_black_norm = specific_weight(symbol)
        x_coords_norm = norm_center_of_gravity_x(symbol)
        y_coords_norm = norm_center_of_gravity_y(symbol)
        x_axis_moment_norm = norm_axial_moment_horizontal(symbol)
        y_axis_moment_norm = norm_axial_moment_vertical(symbol)

        diff_dict = {}
        for sym in model_dict:
            black_diff = (weight_black_norm - model_dict[sym]["black"])
            x_center_diff = (x_coords_norm - model_dict[sym]["x_center"])
            y_center_diff = (y_coords_norm - model_dict[sym]["y_center"])
            x_axis_diff = (x_axis_moment_norm - model_dict[sym]["x_axis"])
            y_axis_diff = (y_axis_moment_norm - model_dict[sym]["y_axis"])
            diff_dict[sym] = 1 - (
                        black_diff ** 2 +
                        x_center_diff ** 2 +
                        y_center_diff ** 2 +
                        x_axis_diff ** 2 +
                        y_axis_diff ** 2
            ) ** (1 / 2)

        res.append(diff_dict)

    return res
