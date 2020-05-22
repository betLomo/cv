import utils as u
import csv
import modules.text_generation as tg
import modules.binarization as binary
import modules.semitone as semitone
import modules.signs as s


def get_normalized_image(pix):
    img_grayscale = binary.apply_threshold(semitone.semitone(pix), 128, 1)
    return u.pix_invert(img_grayscale, 0)


def load_model(path):
    result = {}

    with open(path, mode='r') as analysis_file:
        analysis_file.readline()
        analysis_reader = csv.reader(analysis_file, delimiter=';', quotechar='"')
        for row in analysis_reader:
            result[row[0]] = {
                "black": float(row[2]),
                "x_center": float(row[5]),
                "y_center": float(row[6]),
                "x_axis": float(row[9]),
                "y_axis": float(row[10]),
                #"icm45": float(row[13]),
                #"icm135": float(row[14]),
            }


    return result


def save_hypothesis(hyp, path):
    with open(path, mode='w') as analysis_file:
        analysis_writer = csv.writer(analysis_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for h in hyp:
            res = []
            for key, value in sorted(h.items(), key=lambda item: item[1], reverse=True):
                res.append("%s (%.3f)" % (key, value))
            analysis_writer.writerow(res)



def save_string(hypothesis, model_string, path):
    real = list(map(lambda d: max(d.items(), key=lambda x: x[1])[0], hypothesis))
    real_str = ''.join([str(elem) for elem in real])
    real_fixed = list(real_str.replace("ЬI", "Ы"))
    theory = list(model_string)

    correct = []
    for i in range(0, len(real_fixed)):
        correct.append(1 if real_fixed[i] == theory[i] else 0)

    with open(path, mode='w') as diff_string:
        diff_writer = csv.writer(diff_string, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        diff_writer.writerow(real_fixed)
        diff_writer.writerow(theory)
        diff_writer.writerow(correct)


SAMPLES_PATH = "media/samples/text/"
RESULTS_PATH = "media/results/task6"
SAMPLE_TEXT = "ШИРОКАЯ ЭЛЕКТРИФИКАЦИЯ ЮЖНЫХ ОБЛАСТЕЙ ДАСТ МОЩНЫЙ ТОЛЧОК ПОДЪЁМУ СЕЛЬСКОГО ХОЗЯЙСТВА"
SAMPLE_TEXT_NO_SPACE = "ШИРОКАЯЭЛЕКТРИФИКАЦИЯЮЖНЫХОБЛАСТЕЙДАСТМОЩНЫЙТОЛЧОКПОДЪЁМУСЕЛЬСКОГОХОЗЯЙСТВА"
SAMPLE_FONT = "fonts/arial_italic.ttf"

tg.create_image_sample_text(SAMPLE_TEXT, SAMPLE_FONT, 52).save(SAMPLES_PATH + "/sample_52.bmp")
tg.create_image_sample_text(SAMPLE_TEXT, SAMPLE_FONT, 40).save(SAMPLES_PATH + "/sample_40.bmp")
tg.create_image_sample_text(SAMPLE_TEXT, SAMPLE_FONT, 60).save(SAMPLES_PATH + "/sample_28.bmp")

# 1. Подготовить текст из одной строки, пользуясь выбранным алфавитом и теми же параметрами шрифта
img_52 = get_normalized_image(u.picture_to_array(SAMPLES_PATH + "sample_52.bmp"))
img_40 = get_normalized_image(u.picture_to_array(SAMPLES_PATH + "sample_40.bmp"))
img_28 = get_normalized_image(u.picture_to_array(SAMPLES_PATH + "sample_28.bmp"))

model_dict = load_model('dictionary/sign_table.csv')

hypothesis_52 = s.get_pix_hypothesis(img_52, model_dict)
hypothesis_40 = s.get_pix_hypothesis(img_40, model_dict)
hypothesis_28 = s.get_pix_hypothesis(img_28, model_dict)

save_hypothesis(hypothesis_52, RESULTS_PATH + '/size_52/hypothesis.csv')
save_hypothesis(hypothesis_40, RESULTS_PATH + '/size_40/hypothesis.csv')
save_hypothesis(hypothesis_28, RESULTS_PATH + '/size_28/hypothesis.csv')

save_string(hypothesis_52, SAMPLE_TEXT_NO_SPACE, RESULTS_PATH + '/size_52/diff.csv')
save_string(hypothesis_40, SAMPLE_TEXT_NO_SPACE, RESULTS_PATH + '/size_40/diff.csv')
save_string(hypothesis_28, SAMPLE_TEXT_NO_SPACE, RESULTS_PATH + '/size_28/diff.csv')
