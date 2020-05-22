from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def generate_img_from_text(text, font_path, font_size):
    # Создание белого квадрата, на котором будет написан текст
    img_width = round(font_size * 1.2)
    img_height = round(font_size * 1.2)
    img = Image.new('RGB', (img_width, img_height), (255, 255, 255))
    idraw = ImageDraw.Draw(img)

    # Печать текста поверх белово квадрата
    font = ImageFont.truetype(font_path, font_size)

    text_width, text_height = idraw.textsize(text, font=font)
    idraw.text(((img_width - text_width) / 2, (img_height - text_height) / 2), text, (0, 0, 0), font=font)
    return img


def create_image_sample_text(text, font_path, font_size):
    # тестовое изображние, будем на нём смотреть реальный размер текста
    img = Image.new("RGB", (1000, font_size), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, round(font_size * 1.1))
    text_width, text_height = draw.textsize(text, font=font)    # как раз проверяем какой в итоге размер

    # а теперь, зная какие реальные размеры, можем чётко задать размеры изображения
    result_img = Image.new("RGB", (round(text_width * 1.02), round(text_height * 1.1)), (255, 255, 255))
    result_draw = ImageDraw.Draw(result_img)
    result_draw.text((0, 0), text, (0, 0, 0), font=font)
    return result_img


def generate_dictionary(symbols_string, font_path, font_size):
    result = {}
    for symbol in symbols_string:
        result[symbol] = generate_img_from_text(symbol, font_path, font_size)

    return result
