# храним матрицу пикселей
# имеем pointer, которым двигаем по пикселям
# pointer - 1ый пиксель, куда можно ставить слово/картинку

import sys

w, h, c = map(int, sys.stdin.readline().split())
pixels = [[0] * w]
x = y = 0
last_in_x = last_in_y = 0
max_height_of_line = h
lst = []
for line in sys.stdin:
    lst.append(line)

p = 0

while p < len(lst):
    line = lst[p]
    line = line.strip()
    if line == '':
        x = 0
        while len(pixels) <= y + max_height_of_line:
            pixels.append([0] * w)
        y += max_height_of_line
        max_height_of_line = h
        last_in_x = x
        last_in_y = y

    i = 0
    while i < len(line):
        if line[i] == '(':
            make_line_param = ''
            open_ind = i
            close_ind = i
            while line[i] != ')':
                i += 1
                if i == len(line):
                    make_line_param += ' '
                    p += 1
                    line = lst[p].strip()
                    i = 0
                make_line_param += line[i]

            param = make_line_param[:-1].split()
            width = height = 0

            dx = dy = -1
            for j in range(len(param)):
                if 'layout' in param[j]:
                    layout = param[j][7:]
                elif 'width' in param[j]:
                    width = int(param[j][6:])
                elif 'height' in param[j]:
                    height = int(param[j][7:])
                elif 'dx' in param[j]:
                    dx = int(param[j][3:])
                elif 'dy' in param[j]:
                    dy = int(param[j][3:])

            if layout == 'floating':
                x_float = last_in_x + dx
                y_float = last_in_y + dy
                if x_float < 0:
                    x_float = 0
                elif x_float + width >= w:
                    x_float = w - width
                last_in_x = x_float + width
                last_in_y = y_float
                print(x_float, y_float)

            if x >= w:
                x = 0
                while len(pixels) <= y + max_height_of_line:
                    pixels.append([0] * w)
                y += max_height_of_line
                max_height_of_line = h
                last_in_x = x
                last_in_y = y

            if layout == 'embedded':
                # найдем позицию в которую можно начать вставлять рисунок
                cnt = 0
                a = x
                while True:
                    if a >= w:
                        while len(pixels) <= y + max_height_of_line:
                            pixels.append([0] * w)
                        cnt = 0
                        a = 0
                        y += max_height_of_line
                        max_height_of_line = h

                    if pixels[y][a] == 1 or pixels[y][a] == 2:
                        cnt = 0
                    elif pixels[y][a] == 0:
                        cnt += 1

                    if (cnt == width) and (a - width + 1 == 0):

                        x = a - width + 1
                        break
                    elif (cnt == width) and (0 <= a - width < w) and (
                            pixels[y][a - width] == 2):
                        x = a - width + 1
                        break
                    elif (cnt == width + c) and (a - c - width + 1 != 0):

                        x = a - width + 1
                        break
                    a += 1

                if height > max_height_of_line:
                    max_height_of_line = height

                print(x, y)
                for k in range(y, y + height):
                    if len(pixels) <= k:
                        pixels.append([0] * w)
                    for j in range(x, x + width):
                        pixels[k][j] = 1
                x += width
                last_in_x = x
                last_in_y = y

            elif layout == 'surrounded':
                cnt = 0
                a = x
                while True:
                    if a >= w:
                        while len(pixels) <= y + max_height_of_line:
                            pixels.append([0] * w)
                        cnt = 0
                        a = 0
                        y += max_height_of_line
                        max_height_of_line = h

                    if pixels[y][a] == 1 or pixels[y][a] == 2:
                        cnt = 0
                    elif pixels[y][a] == 0:
                        cnt += 1
                    if cnt == width:
                        x = a - width + 1
                        break
                    a += 1

                print(x, y)
                for k in range(y, y + height):
                    if len(pixels) <= k:
                        pixels.append([0] * w)
                    for j in range(x, x + width):
                        pixels[k][j] = 2
                x += width

                last_in_x = x
                last_in_y = y
            i += 1

        else:
            word = ''
            while i < len(line) and line[i] != ' ':
                word += line[i]
                i += 1
            if word.isalpha() or any(x in word for x in
                                     [".", ",", ":", ";", "!", "?", "-", "'", '1', '2', '3', '4', '5', '6', '7', '8',
                                      '9', '0']):
                # ищем, куда вставить слово
                cnt = 0
                a = x
                while True:
                    if a >= w:
                        while len(pixels) <= y + max_height_of_line:
                            pixels.append([0] * w)
                        cnt = 0
                        a = 0
                        y += max_height_of_line
                        max_height_of_line = h

                    if pixels[y][a] == 1 or pixels[y][a] == 2:
                        cnt = 0
                    elif pixels[y][a] == 0:
                        cnt += 1

                    if (cnt == len(word) * c) and (a - len(word) * c + 1 == 0):
                        x = a - len(word) * c + 1
                        break
                    elif (cnt == len(word) * c) and (0 <= a - len(word) * c < w) and (
                            pixels[y][a - len(word) * c] == 2):

                        x = a - len(word) * c + 1
                        break
                    elif (cnt == len(word) * c + c) and (a - c - len(word) * c + 1 != 0):
                        x = a - len(word) * c + 1
                        break
                    a += 1

                for k in range(x, x + len(word) * c):
                    pixels[y][k] = 1
                x += len(word) * c
                last_in_x = x
                last_in_y = y
        i += 1
    p += 1
