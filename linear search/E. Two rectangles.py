# будем проверять только возможные случаи
def f_up_down(lst, m, n):
    # левая и правая границы верхнего прямоугольника
    left_x1 = -1
    right_x1 = -1
    i = 0
    while (left_x1 == -1 or right_x1 == -1) and i < m:
        j = 0
        while j < n:
            if lst[i][j] == '#' and left_x1 == -1:
                left_x1 = j
            if lst[i][j] == '.' and left_x1 != -1 and right_x1 == -1:
                right_x1 = j - 1
            elif lst[i][j] == '#' and j == n - 1 and left_x1 != -1 and right_x1 == -1:
                right_x1 = j
            if lst[i][j] == '#' and (left_x1 == -1 or (left_x1 != -1 and right_x1)):
                lst[i][j] = 'a'
            j += 1
        i += 1

    # полное пересечение(соприкосновение) по верхней грани
    # при этом верхний прямоугольник мб как больше нижнего так и меньше

    # ищем левую и правую границы нижнего прямоугольника, т.е. первый столбец, отличный от left_x1, в котором будет '#'
    left_x2 = -1
    right_x2 = -1
    row_start_2 = 1
    blank_line_all = False
    # print(f'i={i}')
    for p in range(i, m):
        blank_line = True
        fl = False
        first_meet = -1
        last_meet = -1
        for j in range(n):
            # print(lst[p][j])
            if lst[p][j] == '#':
                # print('sees')
                blank_line = False
            if lst[p][j] == '.' and first_meet != -1 and last_meet != -1:
                # print(f'fl={fl}, {i, j}')
                fl = True
            if (lst[p][j] == '#') and (first_meet == -1):
                first_meet = j
                # print(f'first_meet={first_meet}')
            if (lst[p][j] == '#') and (fl is False):
                # print(f'last_meet={last_meet}')
                last_meet = j
            if lst[p][j] == '#' and fl is True:
                # print(p, j)
                return []
            if lst[p][j] == '#':
                lst[p][j] = 'a'
        if blank_line is True:
            blank_line_all = True
        if (first_meet == left_x1 and last_meet == right_x1) and (blank_line_all is True):
            # print('meet blank line')
            # print(f'first_meet={first_meet}, last_meet={last_meet}')
            left_x2 = first_meet
            right_x2 = last_meet
            row_start_2 = p
            break
        elif (first_meet != left_x1 or last_meet != right_x1) and first_meet != -1:
            # print('no blank lines')
            # print(f'first_meet={first_meet}, last_meet={last_meet}')
            left_x2 = first_meet
            right_x2 = last_meet
            row_start_2 = p
            break

    # print(f'start_i={row_start_2}', right_x2)
    # print(f'left_x2={left_x2}, right_x2={right_x2}')

    if left_x2 == -1 and right_x2 == -1:
        return []
    # дальше '#' должны непрерывно встречаться только в столбцах [left_x2; right_x2]
    for p in range(row_start_2, m):
        # print(lst[p])
        for j in range(n):
            if lst[p][j] == '#' and not (left_x2 <= j <= right_x2):
                # print('# outside')
                return []
            if ("b" in lst[p] or '#' in lst[p]) and (lst[p][j] == '.') and (left_x2 <= j <= right_x2):
                # print('. inside')
                return []
            elif lst[p][j] == '#' or lst[p][j] == 'a':
                lst[p][j] = 'b'
    return lst


def f_left_right(lst_copy2, m, n):
    # перевернем на 90 градусов наш рисунок, а потом повернем обратно
    rotated_lst = [list(row)[::-1] for row in zip(*lst_copy2)]
    rotated_ans_lst = f_up_down(rotated_lst, n, m)
    # print(rotated_ans_lst)
    # обратно переворачиваю на 90 ответ
    back_rotated_ans = [list(row) for row in list(zip(*rotated_ans_lst))[::-1]]
    return back_rotated_ans


def f_one_line(lst_copy3, m, n):
    # левая и правая границы верхнего прямоугольника
    left_x1 = -1
    right_x1 = -1
    i = 0
    while (left_x1 == -1 or right_x1 == -1) and i < m:
        j = 0
        while j < n:
            if lst_copy3[i][j] == '#' and left_x1 == -1:
                left_x1 = j
            if lst_copy3[i][j] == '.' and left_x1 != -1 and right_x1 == -1:
                right_x1 = j - 1
            elif lst_copy3[i][j] == '#' and j == n - 1 and left_x1 != -1 and right_x1 == -1:
                right_x1 = j
            if lst_copy3[i][j] == '#' and (left_x1 == -1 or (left_x1 != -1 and right_x1)):
                lst_copy3[i][j] = 'a'
            j += 1
        i += 1
    if left_x1 == right_x1:
        return []
    lst_copy3[i - 1][right_x1] = 'b'
    fl = True
    for p in range(i + 1, m):
        for j in range(n):
            if lst_copy3[p][j] != '.':
                fl = False
    if fl is False:
        return []
    else:
        return lst_copy3


def f_one_col(lst_copy4, m, n):
    # перевернем на 90 градусов наш рисунок, а потом повернем обратно
    rotated_lst = [list(row)[::-1] for row in zip(*lst_copy4)]
    rotated_ans_lst = f_one_line(rotated_lst, n, m)
    # print(rotated_ans_lst)
    # обратно переворачиваю на 90 ответ
    back_rotated_ans = [list(row) for row in list(zip(*rotated_ans_lst))[::-1]]
    return back_rotated_ans


def f_one_rect(lst_copy5, m, n):
    # проверим что линий с # больше 1
    cnt = 0
    for p in range(m):
        if '#' in lst_copy5[p]:
            cnt += 1
        if cnt > 1:
            break
    if cnt < 2 or n < 2:
        return []

    # левая и правая границы верхнего прямоугольника
    left_x1 = -1
    right_x1 = -1
    i = 0
    while (left_x1 == -1 or right_x1 == -1) and i < m:
        j = 0
        while j < n:
            if lst_copy5[i][j] == '#' and left_x1 == -1:
                left_x1 = j
            if lst_copy5[i][j] == '.' and left_x1 != -1 and right_x1 == -1:
                right_x1 = j - 1
            elif lst_copy5[i][j] == '#' and j == n - 1 and left_x1 != -1 and right_x1 == -1:
                right_x1 = j
            if lst_copy5[i][j] == '#' and (left_x1 == -1 or (left_x1 != -1 and right_x1)):
                lst_copy5[i][j] = 'a'
            j += 1
        i += 1
    # дальше прямоугольник продолжается с теми же размерами
    # print(left_x1, right_x1)
    blank_line_all = False
    # print(f'i={i}')
    for p in range(i, m):
        blank_line = True
        for j in range(n):
            if lst_copy5[p][j] == '#':
                lst_copy5[p][j] = 'b'
                blank_line = False
            if lst_copy5[p][j] != '.' and not (left_x1 <= j <= right_x1):
                return []
            if (lst_copy5[p][j] == '.') and (left_x1 <= j <= right_x1) and ('#' in lst_copy5[p] or 'b' in lst_copy5[p]):
                # print('wew')
                return []
            if blank_line_all is True and lst_copy5[p][j] != '.':
                return []

        if blank_line is True:
            blank_line_all = True
    return lst_copy5

lst = []
m, n = map(int, input().split())
for _ in range(m):
    lst.append(list(input()))

lst_copy1 = [row[:] for row in lst]
lst_copy2 = [row[:] for row in lst]
lst_copy3 = [row[:] for row in lst]
lst_copy4 = [row[:] for row in lst]
lst_copy5 = [row[:] for row in lst]
ans1 = f_up_down(lst_copy1, m, n)
ans2 = f_left_right(lst_copy2, m, n)
ans3 = f_one_line(lst_copy3, m, n)
ans4 = f_one_col(lst_copy4, m, n)
ans5 = f_one_rect(lst_copy5, m, n)
# print(ans5)
# print(ans1, ans2, ans3, ans4, ans5)
if len(ans1) == 0 and len(ans2) == 0 and len(ans3) == 0 and len(ans4) == 0 and len(ans5) == 0:
    print('NO')
else:
    print('YES')
    if len(ans1) != 0:
        for i in range(len(ans1)):
            print(''.join(ans1[i]))
    elif len(ans2) != 0:
        for i in range(len(ans2)):
            print(''.join(ans2[i]))
    elif len(ans5) != 0:
        for i in range(len(ans5)):
            print(''.join(ans5[i]))
    elif len(ans3) != 0:
        for i in range(len(ans3)):
            print(''.join(ans3[i]))
    elif len(ans4) != 0:
        for i in range(len(ans4)):
            print(''.join(ans4[i]))

"""
5 6
#.....
.#####
..####
..####
....##

2 2
##
##

2 7
.##.##.
.##.##.

4 7
.##....
.##....
.##.#..
.##.#..



5 7
.#####.
.#####.
.######
.######
.......

5 7
.#####.
.#####.
.####..
.####..
#......


5 7
.#####.
.#####.
.#####.
.#####.
.......


6 7
.......
#######
.......
#####..
#####..
.......

6 7
#######
.......
.......
.####..
#####..
.......

6 7
#######
..#####
..#####
..###..
..###..
.......

6 7
.......
..#####
..#####
..#####
..###..
.......

7 7
.......
..#####
..#####
..#####
.......
..###..
.......


7 7
.......
..###..
.######
..###..
.......
.......
.......

3 1
.
#
#

3 2
..
#.
#.

"""