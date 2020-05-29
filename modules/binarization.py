import numpy as np
from numpy.lib.stride_tricks import as_strided


def view_as_windows(arr_in, window_shape, step=1):
    # получаем размерность масссива
    ndim = arr_in.ndim

    if isinstance(window_shape, int):
        window_shape = (window_shape,) * ndim

    step = (step,) * ndim
    arr_shape = np.array(arr_in.shape)
    window_shape = np.array(window_shape, dtype=arr_shape.dtype)

    slices = [slice(None, None, st) for st in step]
    window_strides = np.array(arr_in.strides)

    indexing_strides = arr_in[slices].strides

    win_indices_shape = (((np.array(arr_in.shape) - np.array(window_shape))
                          // np.array(step)) + 1)

    new_shape = tuple(list(win_indices_shape) + list(window_shape))
    strides = tuple(list(indexing_strides) + list(window_strides))

    arr_out = as_strided(arr_in, shape=new_shape, strides=strides)
    return arr_out


def bernsen_threshold(img, w_size=55, c_thr=30):
    thresholds = np.zeros(img.shape, np.uint8)

    # Obtaining windows
    hw_size = w_size // 2
    padded_img = np.ones((img.shape[0] + w_size - 1, img.shape[1] + w_size - 1)) * np.nan
    padded_img[hw_size: -hw_size, hw_size: -hw_size] = img

    winds = view_as_windows(padded_img, (w_size, w_size))

    mins = np.nanmin(winds, axis=(2, 3))
    maxs = np.nanmax(winds, axis=(2, 3))

    # Calculating contrast and mid values
    contrast = maxs - mins
    mid_vals = (maxs + mins) / 2

    thresholds[contrast <= c_thr] = 128
    thresholds[contrast > c_thr] = mid_vals[contrast > c_thr]

    return thresholds


def apply_threshold(pix_arr, threshold=128, wp_val=255):
    return ((pix_arr >= threshold) * wp_val).astype(np.uint8)
