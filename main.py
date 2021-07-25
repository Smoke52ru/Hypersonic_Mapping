from math import pi, cos, sin
import re

EPS = 0.000001
regexp_float = r'-?[0-9]*[.,]?[0-9]+'  # выражение выводит все целые и разделенные запятой(точкой) числа

# главная функция
with open('input_generated.txt', 'r') as f:
    name_of_output = f.readline()[:-1]  # читаем имя файла без символа переноса строки
    iters_quantity = int(f.readline())  # общее количество прогонов
    num_lines, num_circles = [int(x) for x in f.readline().split()]  # количестов линий и кругов
    for cur_iter in range(iters_quantity):
        list_of_distances = [0. for x in range(181)]
        for n in range(num_lines):
            x0, y0, x1, y1 = [float(x) for x in re.findall(regexp_float, f.readline())]
            lim = f.readline()[0]
            if x0 == x1:            # Vertical
                if lim == 'y':
                    ymin, ymax = [float(x) for x in re.findall(regexp_float, f.readline())]
                for i in range(181):
                    if i != 90:
                        b = x0 / cos(pi * i / 180)
                        if (list_of_distances[i] == 0 or b < list_of_distances[i]) and b > 0:
                            if lim == 'y':
                                if ymin <= (b * sin(pi * i / 180)) <= ymax:
                                    list_of_distances[i] = b
                            else:
                                list_of_distances[i] = b
            else:                   # Not Vertical
                if lim == 'y':
                    ymin, ymax = [float(x) for x in re.findall(regexp_float, f.readline())]
                elif lim == 'x':
                    xmin, xmax = [float(x) for x in re.findall(regexp_float, f.readline())]
                for i in range(181):
                    if abs(sin(pi * i / 180) - cos(pi * i / 180) * (y1 - y0) / (x1 - x0)) > EPS:  # ... != 0
                        b = (y0 - x0 * (y1 - y0) / (x1 - x0)) / (
                                sin(pi * i / 180) - cos(pi * i / 180) * (y1 - y0) / (x1 - x0))
                        if (list_of_distances[i] == 0 or b < list_of_distances[i]) and b > 0:
                            if lim == 'x':
                                if xmin <= b * cos(pi * i / 180) <= xmax:
                                    list_of_distances[i] = b
                            elif lim == 'y':
                                if ymin <= sin(pi * i / 180) <= ymax:
                                    list_of_distances[i] = b
                            else:
                                list_of_distances[i] = b
        for n in range(num_circles):    # Circle
            x0, y0, r = [float(x) for x in re.findall(regexp_float, f.readline())]
            lim = f.readline()[0]
            if lim == 'y':
                ymin, ymax = [float(x) for x in re.findall(regexp_float, f.readline())]
            elif lim == 'x':
                xmin, xmax = [float(x) for x in re.findall(regexp_float, f.readline())]
            for i in range(181):
                if pow(-2 * x0 * cos(pi * i / 180) - 2 * y0 * sin(pi * i / 180), 2) - 4 * (
                        pow(x0, 2) + pow(y0, 2) - pow(r, 2)) >= 0:
                    b = 2 * x0 * cos(pi * i / 180) + 2 * y0 * sin(pi * i / 180) + pow(
                        pow(-2 * x0 * cos(pi * i / 180) - 2 * y0 * sin(pi * i / 180), 2) - 4 * (
                                pow(x0, 2) + pow(y0, 2) - pow(r, 2)), 0.5) / 2
                    if (list_of_distances[i] == 0 or b < list_of_distances[i]) and b > 0:
                        if lim == 'x':
                            if xmin <= b * cos(pi * i / 180) <= xmax:
                                list_of_distances[i] = b
                        if lim == 'y':
                            if ymin <= b * sin(pi * i / 180) <= ymax:
                                list_of_distances[i] = b
                        else:
                            list_of_distances[i] = b
            for i in range(181):
                if pow(-2 * x0 * cos(pi * i / 180) - 2 * y0 * sin(pi * i / 180), 2) - 4 * (
                        pow(x0, 2) + pow(y0, 2) - pow(r, 2)) >= 0:
                    b = 2 * x0 * cos(pi * i / 180) + 2 * y0 * sin(pi * i / 180) - pow(
                        pow(-2 * x0 * cos(pi * i / 180) - 2 * y0 * sin(pi * i / 180), 2) - 4 * (
                                pow(x0, 2) + pow(y0, 2) - pow(r, 2)), 0.5) / 2
                    if (list_of_distances[i] == 0 or b < list_of_distances[i]) and b > 0:
                        if lim == 'x':
                            if xmin <= b * cos(pi * i / 180) <= xmax:
                                list_of_distances[i] = b
                        if lim == 'y':
                            if ymin <= b * sin(pi * i / 180) <= ymax:
                                list_of_distances[i] = b
                        else:
                            list_of_distances[i] = b
        with open(name_of_output + str(cur_iter+1) + '.txt', 'w') as out:
            for idx, res in enumerate(list_of_distances):
                out.write(f'{idx},{int(bool(res))},{res}\n')
        f.readline()
