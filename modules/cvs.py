import csv


def save_model(path, first_row, str, features):
    [
        weight,
        special_weight,
        center_of_gravity_x, center_of_gravity_y,
        norm_center_of_gravity_x, norm_center_of_gravity_y,
        horizontal, vertical,
        norm_horizontal, norm_vertical,
    ] = features

    with open(path, mode='w') as analysis_file:
        writer = csv.writer(analysis_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(first_row)
        for s in str:
            writer.writerow(
                [
                    s,
                    weight[s],
                    "%.3f" % special_weight[s],
                    "%.2f" % center_of_gravity_x[s],
                    "%.2f" % center_of_gravity_y[s],
                    "%.3f" % norm_center_of_gravity_x[s],
                    "%.3f" % norm_center_of_gravity_y[s],
                    "%.0f" % horizontal[s],
                    "%.0f" % vertical[s],
                    "%.3f" % norm_horizontal[s],
                    "%.3f" % norm_vertical[s]
                ]
            )
