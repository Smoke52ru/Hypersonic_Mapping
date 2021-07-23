from PIL import Image, ImageDraw, ImageColor
from os import mkdir, listdir

regexp_float = r'-?[0-9]*[.,]?[0-9]+'  # выражение выводит все целые числа и десятичные дроби в строке
rec_count = 0
library_counter = 0
SEP_LINE = '#######################'

# визуализация карты препятствий
picture_dir = 'pictures'
picture_width = 800
picture_height = 600
picture_counter = 1


def draw_picture(name, line_list, circles_list, scale=1000):
    global picture_counter
    image = Image.new('RGB', (picture_width, picture_height))
    draw = ImageDraw.Draw(image)
    # отрисовка четырехугольников
    for idx, line in enumerate(line_list):
        draw.line(tuple(
            x * scale + picture_width / 2 if idx % 2 == 0 else picture_height - x * scale for idx, x in
            enumerate(line)))
    # отрисовка окружностей
    for circ in circles_list:
        center_x, center_y, radius = circ
        draw.ellipse(((center_x - radius) * scale + picture_width / 2,
                      (center_y - radius) * scale + picture_height,
                      (center_x + radius) * scale + picture_width / 2,
                      (center_y + radius) * scale + picture_height))
    # отрисовка начала координат
    draw.rectangle((picture_width / 2 - 3, picture_height - 3, picture_width / 2 + 3, picture_height),
                   fill=ImageColor.getrgb('yellow'))

    if picture_dir not in listdir():
        mkdir(picture_dir)
    image.save(f'{picture_dir}\\{name}_{picture_counter}.png', 'PNG')
    picture_counter += 1


# генератор float от start до stop включительно
def float_range(start, stop, step):
    while start < stop:
        yield float(start)
        start += step


def quads_handler():
    res_list = list()
    for quad in range(n_quads):
        for point in range(3):
            res_list.append(
                (round(eval(quads[8 * quad + point * 2]), 4),
                 round(eval(quads[8 * quad + point * 2 + 1]), 4),
                 round(eval(quads[8 * quad + point * 2 + 2]), 4),
                 round(eval(quads[8 * quad + point * 2 + 3]), 4)))
        res_list.append((round(eval(quads[8 * (quad + 1) - 2]), 4),
                         round(eval(quads[8 * (quad + 1) - 1]), 4),
                         round(eval(quads[8 * quad + 0]), 4),
                         round(eval(quads[8 * quad + 1]), 4)))
    return res_list


def circles_handler():
    res_list = list()
    for circle in range(n_circle):
        res_list.append((round(eval(circles[3 * circle + 0]), 4),
                         round(eval(circles[3 * circle + 1]), 4),
                         round(eval(circles[3 * circle + 2]), 4)))
    return res_list


# функция разбивающая фигуры на примитивы
def rec_fun():
    global rec_count, n_params, library_counter
    rec_count += 1
    for j in float_range(t_min[rec_count - 1], t_max[rec_count - 1] + t_step[rec_count - 1], t_step[rec_count - 1]):
        t[rec_count] = round(j, 4)
        if rec_count == n_params:
            quad_list = quads_handler()
            circle_list = circles_handler()
            draw_picture('pic', quad_list, circle_list)

            for line in quad_list:
                res_file.write(f'{line[0]} {line[1]} {line[2]} {line[3]}\n')
                if line[0] != line[2]:  # Not horizontal
                    min_x, max_x = sorted([line[0], line[2]])
                    res_file.write(f'x\n{min_x} {max_x}\n')
                else:
                    min_y, max_y = sorted([line[1], line[3]])
                    res_file.write(f'y\n{min_y} {max_y}\n')
            for circ in circle_list:
                x, y, r = circ
                res_file.write(f'{x} {y} {r}\n')
                res_file.write(f'0\n')
            res_file.write(SEP_LINE + '\n')
            # запись справочной информации в файл-библиотеку
            library_counter += 1
            library_file.write(f'Решение №{library_counter}\n')
            for param in range(n_params):
                library_file.write(f'{t_name[param]} = {t[param + 1]}\n')
        else:
            rec_fun()
    rec_count -= 1


input_file = open('gen_input_quads.txt', 'r')
name_of_output = input_file.readline()[:-1]
library_file = open(f'{name_of_output}_library.txt', 'w')
res_file = open('input_generated.txt', 'w')
n_params = int(input_file.readline())
t = [0. for x in range(n_params + 1)]  #
t_min, t_max, t_step, t_name = list(), list(), list(), list()
for i in range(n_params):
    string = input_file.readline()
    subs = string.split()
    t_min.append(float(subs[0])), t_step.append(float(subs[1])), t_max.append(float(subs[2])), t_name.append(subs[3])
n_quads, n_circle = [int(x) for x in input_file.readline().split()]
quads, circles = list(), list()
for i in range(1, n_quads + 1, 1):
    for j in range(8):
        quads.append(input_file.readline()[:-1])
for i in range(1, n_circle + 1, 1):
    for j in range(3):
        circles.append(input_file.readline()[:-1])
input_file.close()
# подсчет количества сгенерированных случаев
n_iter = 1
for i in range(n_params):
    n_iter *= (t_max[i] - t_min[i]) / t_step[i] + 1.
n_iter = int(round(n_iter))
n_lines = 4 * n_quads
library_file.write(f'{name_of_output}\n{n_iter}\n{n_lines} {n_circle}\n')
res_file.write(f'{name_of_output}\n{n_iter}\n{n_lines} {n_circle}\n')
rec_fun()

res_file.close()
library_file.close()
