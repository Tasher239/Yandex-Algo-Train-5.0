class Player:
    def __init__(self, x, y, v):
        self.x = x
        self.y = y
        self.v = v


def proverka(target_dot_x, target_dot_y, t):
    for player in lst:
        if round((target_dot_x - player.x) ** 2 + (target_dot_y - player.y) ** 2, 5) < round((player.v * t) ** 2, 5):
            return False
    return True


def circle_intersection(x1, y1, r1, x2, y2, r2):
    A = -2 * x2
    B = -2 * y2
    C = x2 ** 2 + y2 ** 2 + r1 ** 2 - r2 ** 2

    # ближайшая к центру точка прямой
    x0 = -(A * C) / (A ** 2 + B ** 2)
    y0 = -(B * C) / (A ** 2 + B ** 2)

    # расстояние от этой точки до центра
    dist = abs(C) / ((A ** 2 + B ** 2) ** 0.5)

    if dist > r1:
        return []
    elif dist == r1:
        return [(x0, y0)]
    elif dist < r1:
        p = (r1 ** 2 - C ** 2 / (A ** 2 + B ** 2)) ** 0.5
        coef = (p ** 2 / (A ** 2 + B ** 2)) ** 0.5
        dot1_x = x0 + B * coef
        dot1_y = y0 - A * coef
        dot2_x = x0 - B * coef
        dot2_y = y0 + A * coef

        return [(dot1_x, dot1_y), (dot2_x, dot2_y)]


# проверка, что до момента поднятия мяча пройдет времени не меньше t
# т.е. соперник добежит до точки мяча через время time или позднее
def check(t):
    global x_ans, y_ans, lst, d
    if proverka(0, d, t):
        x_ans = 0
        y_ans = d
        return True

    # x' = x-x1 => x=x'+x1

    for i in range(len(lst)):
        x1 = 0
        y1 = 0
        r1 = lst[i].v * t

        x2 = 0 - lst[i].x
        y2 = 0 - lst[i].y
        r2 = d

        intersections = circle_intersection(x1, y1, r1, x2, y2, r2)

        if len(intersections) == 1:
            x_tmp = intersections[0][0] + lst[i].x
            y_tmp = intersections[0][1] + lst[i].y
            if (x_tmp ** 2 + y_tmp ** 2) ** 0.5 <= d and y_tmp >= 0 and proverka(x_tmp, y_tmp, t):
                x_ans = x_tmp
                y_ans = y_tmp
                return True

        elif len(intersections) == 2:
            dot1_x = intersections[0][0] + lst[i].x
            dot1_y = intersections[0][1] + lst[i].y
            dot2_x = intersections[1][0] + lst[i].x
            dot2_y = intersections[1][1] + lst[i].y

            if (dot1_x ** 2 + dot1_y ** 2) ** 0.5 <= d and dot1_y >= 0 and proverka(dot1_x, dot1_y, t):
                x_ans = dot1_x
                y_ans = dot1_y
                return True
            elif (dot2_x ** 2 + dot2_y ** 2) ** 0.5 <= d and dot2_y >= 0 and proverka(dot2_x, dot2_y, t):
                x_ans = dot2_x
                y_ans = dot2_y
                return True

        # считаем что ее центр в начале координат
        # при выводе ответа координаты нужно восстановить обратно
        # x ** 2 + y ** 2 = r ** 2
        for j in range(len(lst)):
            if i != j:
                x2 = lst[j].x - lst[i].x
                y2 = lst[j].y - lst[i].y
                r2 = lst[j].v * t

                intersections = circle_intersection(x1, y1, r1, x2, y2, r2)

                if len(intersections) == 1:
                    x_tmp = intersections[0][0] + lst[i].x
                    y_tmp = intersections[0][1] + lst[i].y
                    if (x_tmp ** 2 + y_tmp ** 2) ** 0.5 <= d and y_tmp >= 0 and proverka(x_tmp, y_tmp, t):
                        x_ans = x_tmp
                        y_ans = y_tmp
                        return True

                elif len(intersections) == 2:
                    dot1_x = intersections[0][0] + lst[i].x
                    dot1_y = intersections[0][1] + lst[i].y
                    dot2_x = intersections[1][0] + lst[i].x
                    dot2_y = intersections[1][1] + lst[i].y

                    if (dot1_x ** 2 + dot1_y ** 2) ** 0.5 <= d and dot1_y >= 0 and proverka(dot1_x, dot1_y, t):
                        x_ans = dot1_x
                        y_ans = dot1_y
                        return True
                    elif (dot2_x ** 2 + dot2_y ** 2) ** 0.5 <= d and dot2_y >= 0 and proverka(dot2_x, dot2_y, t):
                        x_ans = dot2_x
                        y_ans = dot2_y
                        return True
    return False


# для каждых двух игроков вычисляем точку пересечения окружностей,


# соответствующих точкам в которые они могут попасть за время не больше t
# т.е. радиусы Vasya.v*t
# к этому добавляем окружность с центом в (0,0,d)
# в качестве базовой (опорной) точки возьмем (0, d)


d, n = map(int, input().split())
lst = []

for _ in range(n):
    x, y, v = map(int, input().split())
    Vasya = Player(x, y, v)
    lst.append(Vasya)

x_ans = y_ans = -1
l, r = 0, 10**4
while r - l > 2 * 0.00001:
    m = (l + r) / 2
    # print(m)
    if check(m):
        l = m
    else:
        r = m

print((l + r) / 2)
print(x_ans, y_ans)

# 3.53553
# 5.00000 0.00000
