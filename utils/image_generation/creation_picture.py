import random
from math import sqrt
import re
from typing import Tuple
from config.const import IMAGE_DIR, FONTS_DIR

from PIL import Image, ImageDraw, ImageFont


def decoding_color(color: str) -> Tuple[int, int, int, int]:
    default_color = (0, 0, 0, 255)
    pattern = r'^#[0-9a-fA-F]{8}$'

    if re.match(pattern, color) is not None:
        rgba_color = re.findall(r"(..)", color[1:])
        return tuple(int(i, 16) for i in rgba_color)
    return default_color


def repaint_icon(img: Image,
                 color: str,):

    rgba_color = decoding_color(color)

    for y in range(img.height):
        for x in range(img.width):
            if img.getpixel((x, y)) != (0, 0, 0, 0):
                img.putpixel((x, y), rgba_color)


def draw_round_gradient(img: Image,
                        xy: Tuple[int, int, int, int],
                        inner_color: str,
                        outer_color: str,
                        center: Tuple[int, int] = None):

    def mix_colors(color_bg: Tuple[int, int, int],
                   color_pt: Tuple[int, int, int],
                   alpha: int) -> Tuple[int, int, int]:

        mix_color = [0, 0, 0]
        mix_ratio = alpha / 255
        mix_color_bg = [i * (1 - mix_ratio) for i in color_bg]
        mix_color_pt = [i * mix_ratio for i in color_pt]

        for i in range(len(mix_color)):
            mix_color[i] = int(mix_color_bg[i] + mix_color_pt[i])
        return tuple(mix_color)

    width = xy[2] - xy[0]
    height = xy[3] - xy[1]

    start = (width // 2, height // 2) if not center else center

    rgba_inner_color = decoding_color(inner_color)
    rgba_outer_color = decoding_color(outer_color)

    max_distance2start = max(
        sqrt((0 - start[0]) ** 2 + (0 - start[1]) ** 2),
        sqrt((width - start[0]) ** 2 + (0 - start[1]) ** 2),
        sqrt((0 - start[0]) ** 2 + (height - start[1]) ** 2),
        sqrt((width - start[0]) ** 2 + (height - start[1]) ** 2)
    )

    for y in range(height):
        for x in range(width):
            distance2start = sqrt((x - start[0]) ** 2 + (y - start[1]) ** 2)

            distance2start = distance2start / max_distance2start

            r = rgba_outer_color[0] * distance2start + rgba_inner_color[0] * (1 - distance2start)
            g = rgba_outer_color[1] * distance2start + rgba_inner_color[1] * (1 - distance2start)
            b = rgba_outer_color[2] * distance2start + rgba_inner_color[2] * (1 - distance2start)
            a = rgba_outer_color[3] * distance2start + rgba_inner_color[3] * (1 - distance2start)

            img.putpixel((x, y),
                         mix_colors(img.getpixel((x, y)),
                                    (int(r), int(g), int(b)),
                                    int(a)
                                    )
                         )


def calc_font_size(text: str,
                   width: int,
                   font_path: str):  # height=0):

    img = Image.new('RGB', (1, 1), color="#000000")
    img_cnv = ImageDraw.Draw(img)

    size1 = 100
    size2 = 200

    bbox1 = img_cnv.textbbox((0, 0), text, font=ImageFont.truetype(font_path, size1, encoding='UTF-8'))
    bbox2 = img_cnv.textbbox((0, 0), text, font=ImageFont.truetype(font_path, size2, encoding='UTF-8'))

    text_width1 = bbox1[2] - bbox1[0]
    text_width2 = bbox2[2] - bbox2[0]

    # text_height2 = bbox2[3] - bbox2[1]
    # text_height1 = bbox1[3] - bbox1[1]

    relation_width = (size2 - size1) / (text_width2 - text_width1)
    # relation_width -= 0.01
    # relation_height = (size2 - size1) / (text_height2 - text_height1)

    return int(width * relation_width)


def create_insult(path: str,
                  upper_text: str,
                  bottom_text: str,
                  upper_color: str,
                  bottom_color: str,
                  upper_stroke_color: str,
                  bottom_stroke_color: str,
                  stroke_width: int,
                  giant_text: bool,
                  size: int,
                  distance: int) -> str:
    save_path = f'{path[:-4]}-mem-insult.png'
    text_size = size // 10
    impact = FONTS_DIR / 'Impact.ttf'

    img = Image.open(path).convert('RGB').resize((size, size))
    img_cnv = ImageDraw.Draw(img)

    text_size1 = calc_font_size(upper_text, size - (2 * distance), impact) if upper_text != '' else text_size
    text_size2 = calc_font_size(bottom_text, size - (2 * distance), impact)

    if min(text_size1, text_size2) < text_size:
        text_size = min(text_size1, text_size2)

    if giant_text and upper_text == '':
        text_size = text_size2
    elif giant_text:
        text_size = min(text_size1, text_size2)

    font = ImageFont.truetype(impact, text_size)

    img_cnv.text((size // 2, distance),
                 upper_text,
                 font=font,
                 fill=upper_color,
                 stroke_width=stroke_width,
                 stroke_fill=upper_stroke_color,
                 anchor="mt"
                 )
    img_cnv.text((size // 2, size - distance),
                 bottom_text,
                 font=font,
                 fill=bottom_color,
                 stroke_width=stroke_width,
                 stroke_fill=bottom_stroke_color,
                 anchor="ms"
                 )

    img.save(save_path)
    return save_path


def create_demotiv(path: str,
                   upper_text: str,
                   bottom_text: str,
                   footnote: str,
                   upper_color: str,
                   bottom_color: str,
                   stroke_color: str,
                   stroke_width: int,
                   size: int,
                   distance: int) -> str:
    save_path = f'{path[:-4]}-mem-demotiv.png'
    times_new_roman = FONTS_DIR / 'Times New Roman.ttf'
    arial = FONTS_DIR / 'Arial.ttf'

    img_paste = Image.open(path).convert('RGB')
    relation = img_paste.height / img_paste.width

    img_paste = img_paste.resize((size - (2 * distance), int((size - (2 * distance)) * relation)))

    img = Image.new('RGB', (size, size), color="#000000")

    text_size1 = calc_font_size(upper_text, size - (6 * distance), times_new_roman)
    text_size2 = calc_font_size(bottom_text, size - (6 * distance), arial) if bottom_text != '' else text_size1

    if text_size1 > text_size2 * 2:
        text_size = text_size2 * 2
    else:
        text_size = text_size1


    font_upper = ImageFont.truetype(times_new_roman, text_size)
    font_bottom = ImageFont.truetype(arial, text_size // 2)

    font_footnote = ImageFont.truetype(times_new_roman, 25)

    #  Отношение высоты буквы к размеру шрифта:
    #  Arial: 0.74
    #  Times New Roman: 0.68

    if bottom_text == '':
        img = img.resize((img.width, int(3 * distance + img_paste.height + 0.68 * text_size)))
    else:
        img = img.resize((img.width, int(3.5 * distance + img_paste.height + 1.05 * text_size)))

    img_cnv = ImageDraw.Draw(img)
    upper_bbox = list(img_cnv.textbbox((0, 0), upper_text, font_upper))
    delta = 0  # высота между блоками текста upper и bottom
    if bottom_text != '':
        height_upper = upper_bbox[3] - upper_bbox[1]  # высота верхнего текста
        PHASALO_ratio = 1.05  # межстрочный интерва 5%
        if height_upper * PHASALO_ratio > 0.5 * distance + 0.68 * text_size:
            delta = height_upper * PHASALO_ratio
            img = img.resize((img.width, int(3.5 * distance +
                                             img_paste.height + 1.05 * text_size +
                                             delta - (0.5 * distance + 0.68 * text_size))))
            img_cnv = ImageDraw.Draw(img)
        else:
            delta = 0.5 * distance + 0.68 * text_size

    img_cnv.rectangle((distance - 8,
                       distance - 8,
                       img_paste.width + distance + 8,
                       img_paste.height + distance + 8),
                      fill='#000000',
                      outline=stroke_color,
                      width=stroke_width,
                      )

    img.paste(img_paste, (distance, distance))

    bbox = img_cnv.textbbox((int(img_paste.width + distance - 1),
                             int(img_paste.height + distance)),
                            footnote,
                            font=font_footnote,
                            anchor='rt')

    bbox = list(bbox)
    bbox[0] -= 4
    bbox[2] += 4
    bbox = tuple(bbox)

    img_cnv.rectangle(bbox, fill="#000000")

    img_cnv.text((int(img_paste.width + distance),
                  int(img_paste.height + distance)),
                 footnote,
                 font=font_footnote,
                 fill=stroke_color,
                 stroke_fill="#000000",
                 anchor="rt"
                 )
    img_cnv.text((img.width // 2,
                  img_paste.height + 2 * distance),
                 upper_text,
                 font=font_upper,
                 fill=upper_color,
                 anchor="mt"
                 )
    img_cnv.text((img.width // 2,
                  int(img_paste.height + 2 * distance + delta)),
                 bottom_text,
                 font=font_bottom,
                 fill=bottom_color,
                 anchor="mt"
                 )

    img.save(save_path)
    return save_path


def create_book(path: str,
                author: str,
                title: str,
                descriptor: str,
                annotation_location: str,
                annotation: list,
                author_backing_color: str,
                title_backing_color: str,
                logo_backing_color: str,
                size: int,
                distance: int) -> str:
    save_path = f'{path[:-4]}-mem-book.png'
    basic_color = "#faef9f"
    relation = 930 / 600
    illustration_height = int(size * relation * 370 / 930)

    small_distance = distance // 8
    descriptor_line_width = 2 * distance // 3

    img_past = Image.open(path).convert('RGB')
    img_logo = Image.open(IMAGE_DIR / 'logo.png').convert('RGBA')

    myriad_pro_bold = FONTS_DIR / 'Myriad Pro Bold.OTF'
    myriad_pro_cond_bold = FONTS_DIR / 'Myriad Pro Cond Bold.OTF'
    myriad_pro_cond_italic = FONTS_DIR / 'Myriad Pro Cond Italic.OTF'

    img = Image.new('RGB', (size, int(size * relation)), color=basic_color)
    img_cnv = ImageDraw.Draw(img)

    # Верхний черный прямоугольник
    img_cnv.rectangle((distance,
                       distance - 2 * small_distance,
                       size - distance,
                       distance - small_distance),
                      fill="#000000")

    # Нижний черный прямоугольник для надписи "русская классика"
    img_cnv.rectangle((distance,
                       img.height - (distance - 2 * small_distance) - descriptor_line_width,
                       img.width - distance,
                       img.height - (distance - 2 * small_distance)),
                      fill="#000000")

    font_descriptor = ImageFont.truetype(myriad_pro_bold, 18)
    for i in range(len(descriptor) + 1):
        img_cnv.text((distance + int((size - (distance * 2)) * (i / (len(descriptor) + 1))),
                      img.height - (distance - 2 * small_distance) - descriptor_line_width // 2),
                     f' {descriptor}'[i],
                     font=font_descriptor,
                     fill=basic_color,
                     anchor="mm"
                     )

    annotation_size = random.randint(90, 140)
    font_annotation = ImageFont.truetype(myriad_pro_cond_italic, 19)

    if annotation_location == 'l':
        position_annotation = int(1.5 * distance)
        position_l_title = int(2 * distance) + 153
        position_r_title = img.width - distance
    else:
        position_annotation = img.width - int(1.5 * distance) - 153
        position_l_title = distance
        position_r_title = img.width - int(2 * distance) - 153

    # Прямоугольник для названия (около "Книги, изменившие мир.")
    img_cnv.rectangle((position_l_title,
                       img.height - (distance - small_distance) - descriptor_line_width - annotation_size,
                       position_r_title,
                       img.height - (distance - small_distance) - descriptor_line_width),
                      fill=author_backing_color)

    img_cnv.text((position_annotation,
                  img.height - (distance - small_distance) - descriptor_line_width - (annotation_size // 2) - 22),
                 annotation[0],
                 font=font_annotation,
                 fill='#000000',
                 anchor="lm"
                 )
    img_cnv.text((position_annotation,
                  img.height - (distance - small_distance) - descriptor_line_width - (annotation_size // 2)),
                 annotation[1],
                 font=font_annotation,
                 fill='#000000',
                 anchor="lm"
                 )
    img_cnv.text((position_annotation,
                  img.height - (distance - small_distance) - descriptor_line_width - (annotation_size // 2) + 22),
                 annotation[2],
                 font=font_annotation,
                 fill='#000000',
                 anchor="lm"
                 )

    if len(title) < 6:
        title_name_font = myriad_pro_bold
    else:
        title_name_font = myriad_pro_cond_italic

    if len(title.split()) >= 2 and len(title) > 16:
        bottom_title = " ".join(title.split()[(len(title.split()) // 2 + len(title.split()) % 2):])
        upper_title = " ".join(title.split()[:(len(title.split()) - len(title.split()) // 2)])

        if len(upper_title) >= len(bottom_title):
            max_title = upper_title
        else:
            max_title = bottom_title

        title_size = calc_font_size(max_title, int(img.width - 3.5 * distance - 153), title_name_font)
        title_font = ImageFont.truetype(title_name_font, title_size)

        img_cnv.text((position_l_title + distance // 4,
                      img.height - (distance - small_distance) - descriptor_line_width - (annotation_size // 2) - 5),
                     upper_title,
                     font=title_font,
                     fill='#000000',
                     anchor="lb"
                     )

        img_cnv.text((position_l_title + distance // 4,
                      img.height - (distance - small_distance) - descriptor_line_width - (annotation_size // 2) + 5),
                     bottom_title,
                     font=title_font,
                     fill='#000000',
                     anchor="lt"
                     )

    else:
        title_size = calc_font_size(title, int(img.width - 3.5 * distance - 153), title_name_font)

        if title_size > annotation_size:
            title_size = annotation_size

        title_font = ImageFont.truetype(title_name_font, title_size)

        if len(title) < 6:
            position = img.height - (distance - small_distance) - descriptor_line_width - int(0.82 * annotation_size // 2)
        else:
            position = img.height - (distance - small_distance) - descriptor_line_width - int(0.92 * annotation_size // 2)

        img_cnv.text((position_l_title + distance // 4,
                      position),
                     title,
                     font=title_font,
                     fill='#000000',
                     anchor="lm"
                     )

    if len(author.split()) <= 1:
        bottom_author = author if author != '' else "Иванов"
        upper_author = "Иван Иванович"
    else:
        bottom_author = author.split()[-1]
        upper_author = " ".join(author.split()[:-1])

    if len(upper_author.split()) == 2:
        upper_author_name_font = myriad_pro_cond_bold
    else:
        upper_author_name_font = myriad_pro_bold

    upper_author_size = size // 2
    upper_author_font = ImageFont.truetype(upper_author_name_font, upper_author_size)
    upper_author_width = img_cnv.textlength(upper_author, font=upper_author_font)

    while (upper_author_width >= (img.width - 2.5 * distance) - upper_author_size) and \
            (upper_author_size != 1):
        upper_author_size = upper_author_size - 1 if upper_author_size - 1 > 0 else 1
        upper_author_font = ImageFont.truetype(upper_author_name_font, upper_author_size)
        upper_author_width = img_cnv.textlength(upper_author, font=upper_author_font)

    bottom_author_size = calc_font_size(bottom_author, int(img.width - 2.5 * distance), myriad_pro_cond_bold)
    bottom_author_font = ImageFont.truetype(myriad_pro_cond_bold, bottom_author_size)

    # Тут сложная логика через левую коленку, но если в двух словах
    # скрипт вычислил сверху абсолютные значения для картинки, верхнего и нижнего имени автора.
    # код ниже растягивает эти значения на оставшуюся часть картинки
    #
    #                    Срезаем место сверху
    #                    |          Срезаем место снизу
    #                    |          |                                                    Срезаем расстояния меж блоками
    #                    L_______   L_________________________________________________   L___________________
    place = img.height - distance - distance - descriptor_line_width - annotation_size - (4 * small_distance)

    relation4place = place / (illustration_height + upper_author_size + bottom_author_size)

    illustration_height = int(illustration_height * relation4place)
    upper_author_size = int(upper_author_size * relation4place)
    bottom_author_size = int(bottom_author_size * relation4place)

    img_past = img_past.resize((size - (distance * 2), illustration_height))
    img.paste(img_past, (distance, distance))

    img_cnv.rectangle((distance,
                       distance + img_past.height + small_distance,
                       size - distance,
                       distance + img_past.height + 2 * small_distance),
                      fill="#000000")

    # Чтобы было удобно считать, определяем новый «нуль» (Относительно низа картинки)
    zero_below_img = distance + img_past.height + 3 * small_distance

    img_cnv.rectangle((distance,
                       zero_below_img,
                       size - distance,
                       zero_below_img + upper_author_size),
                      fill=author_backing_color)

    img_cnv.rectangle((distance,
                       zero_below_img,
                       distance + upper_author_size,
                       zero_below_img + upper_author_size),
                      fill=logo_backing_color)

    img_logo = img_logo.resize((upper_author_size, upper_author_size))
    img.paste(img_logo,
              (distance,
               zero_below_img),
              mask=img_logo)

    img_cnv.text(((img.width + upper_author_size) // 2,
                  int(zero_below_img + 0.62 * upper_author_size)),
                 upper_author,
                 font=upper_author_font,
                 fill='#000000',
                 anchor="mm"
                 )

    img_cnv.rectangle((distance,
                       zero_below_img + small_distance + upper_author_size,
                       size - distance,
                       int(zero_below_img + small_distance + upper_author_size + bottom_author_size)),
                      fill=title_backing_color)

    img_cnv.text((img.width // 2,
                  int(zero_below_img + small_distance + upper_author_size + 0.62 * bottom_author_size)),
                 bottom_author,
                 font=bottom_author_font,
                 fill=basic_color,
                 anchor="mm"
                 )

    img.save(save_path)
    return save_path


def create_fact(path: str,
                upper_text: str,
                bottom_text: str,
                upper_color: str,
                bottom_color: str,
                stroke_color: str,
                opacity: str,
                size: int,
                distance: int) -> str:
    save_path = f'{path[:-4]}-mem-fact.png'

    arial = FONTS_DIR / 'Arial.ttf'

    img = Image.open(path).convert('RGB').resize((size, size))
    img_cnv = ImageDraw.Draw(img, "RGBA")

    # Затемнение картинки

    # img_cnv.rectangle((0, 0, img.width, img.height),
    #                   fill='#000000' + opacity)
    draw_round_gradient(img,
                        (0, 0, size, size),
                        "#000000" + opacity,
                        "#00000000",
                        # (img.width // 2, 3 * img.height // 4)
                        )

    center_line_height = size // 100
    center_line_width = size // 5

    img_cnv.rectangle((img.width // 2 - center_line_width // 2,
                       img.height // 2 - center_line_height // 2,
                       img.width // 2 + center_line_width // 2,
                       img.height // 2 + center_line_height // 2),
                      fill=stroke_color + opacity,
                      )

    upper_text = upper_text[:51]

    bottom_strings = []
    if len(bottom_text.split()) > 1:

        line = ''
        for i in bottom_text.split():
            line += i + ' '
            if len(line) >= 30:
                line = line[:-1]
                bottom_strings.append(line)
                line = ''

        if line != '':
            bottom_strings.append(line)

    else:
        bottom_strings = [bottom_text[:31]]

    upper_size = size // 10
    new_upper_size = calc_font_size(upper_text, size - (2 * distance), arial)
    if new_upper_size < upper_size:
        upper_size = new_upper_size

    bottom_size = size // 15
    for bottom_string in bottom_strings:
        new_bottom_size = calc_font_size(bottom_string, size - (2 * distance), arial) if bottom_text != '' else bottom_size
        if new_bottom_size < bottom_size:
            bottom_size = new_bottom_size

    font_upper = ImageFont.truetype(arial, upper_size)
    font_bottom = ImageFont.truetype(arial, bottom_size)

    img_cnv.text((img.width // 2,
                  img.height // 2 - distance),
                 upper_text,
                 font=font_upper,
                 fill=upper_color,
                 stroke_width=2,
                 anchor="ms"
                 )

    for number_string in range(len(bottom_strings)):
        x_past = img.height // 2 + (number_string * bottom_size) + 2 * distance

        if x_past > img.height:
            break

        img_cnv.text((img.width // 2,
                      x_past),
                     bottom_strings[number_string],
                     font=font_bottom,
                     fill=bottom_color,
                     anchor="ms"
                     )

    img.save(save_path)
    return save_path


def create_tele(path: str,
                profile_name: str,
                msg: str,
                online_status: str,
                ignore_status: bool,
                time_inner: str,
                profile_name_color: str,
                msg_color: str,
                bg_color: str,
                msg_bg_color: str,
                opacity: str) -> str:
    save_path = f'{path[:-4]}-mem-tele.png'
    width = 1080
    height = 1920
    name_case_height = height // 12
    msg_case_height = height // 14
    distance = width // 36
    max_in_strings = 35

    roboto = FONTS_DIR / 'Roboto-Regular.ttf'

    img = Image.new('RGB', (width, height), color="#395778")
    img_cnv = ImageDraw.Draw(img, "RGBA")

    img_past = Image.open(path).convert('RGB').resize((name_case_height - distance,
                                                       name_case_height - distance))

    msg_strings_temp = []
    msg_strings = []

    nct = 0
    for nc in range(len(msg)):
        if msg[nc] == '$':
            msg_strings_temp.append(msg[nct:nc].replace('$', '').strip())
            nct = nc
    msg_strings_temp.append(msg[nct:(len(msg) - 1)].replace('$', '').strip())

    line = ''
    for string in msg_strings_temp:
        for word in string:
            line += word + ' '
            if len(line) >= 30:
                line = line[:-1]
                bottom_strings.append(line)
                line = ''

        if line != '':
            bottom_strings.append(line)



    img_cnv.rectangle((img.width // 2 - center_line_width // 2,
                       img.height // 2 - center_line_height // 2,
                       img.width // 2 + center_line_width // 2,
                       img.height // 2 + center_line_height // 2),
                      fill=stroke_color + opacity,
                      )

    upper_text = upper_text[:51]

    bottom_strings = []
    if len(bottom_text.split()) > 1:
        counter = 0
        line = ""

        for i in bottom_text.split():
            counter += 1
            line += i + " "
            if len(line) >= 30:
                line = line[:-1]
                bottom_strings.append(line)
                line = ""

        if line != "":
            bottom_strings.append(line)

    else:
        bottom_strings = [bottom_text[:31]]

    upper_size = size // 10
    new_upper_size = calc_font_size(upper_text, size - (2 * distance), arial)
    if new_upper_size < upper_size:
        upper_size = new_upper_size

    bottom_size = size // 5
    for bottom_string in bottom_strings:
        new_bottom_size = calc_font_size(bottom_string, size - (2 * distance), arial) if bottom_text != '' else bottom_size
        if new_bottom_size < bottom_size:
            bottom_size = new_bottom_size

    font_upper = ImageFont.truetype(arial, upper_size)
    font_bottom = ImageFont.truetype(arial, bottom_size)

    img_cnv.text((img.width // 2,
                  img.height // 2 - distance),
                 upper_text,
                 font=font_upper,
                 fill=upper_color,
                 stroke_width=2,
                 anchor="ms"
                 )

    for number_string in range(len(bottom_strings)):
        x_past = img.height // 2 + (number_string * bottom_size) + 2 * distance

        if x_past > img.height:
            break

        img_cnv.text((img.width // 2,
                      x_past),
                     bottom_strings[number_string],
                     font=font_bottom,
                     fill=bottom_color,
                     anchor="ms"
                     )

    img.save(save_path)
    return save_path
