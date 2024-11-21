def check(width_of_road, x_coord, pref_mini_y, pref_maxi_y, suf_mini_y, suf_maxi_y):
    last_not_cover = 0
    # двигаем правую границу дорожки и для каждого
    # положения ищем последнюю точку которая не покрывается
    # тогда найденная точка отвечает за префикс, а right_border за суффикс
    for right_border in range(n):
        while x_coord[last_not_cover] <= x_coord[right_border] - width_of_road:
            last_not_cover += 1
        # смотри максимальную и минимальную координаты по Y на префиксе (до левой границы)
        # и суффиксе (правее правой границы)
        # Но нужно проверить что суффикс и префикс вообще есть
        if last_not_cover != 0:
            maxi_y_in_pref = pref_maxi_y[last_not_cover - 1]
            mini_y_in_pref = pref_mini_y[last_not_cover - 1]
        else:
            maxi_y_in_pref = -1
            mini_y_in_pref = h + 1

        if right_border != n - 1:
            maxi_y_in_suf = suf_maxi_y[right_border + 1]
            mini_y_in_suf = suf_mini_y[right_border + 1]
        else:
            maxi_y_in_suf = -1
            mini_y_in_suf = h + 1

        maxi_y = max(maxi_y_in_suf, maxi_y_in_pref)
        mini_y = min(mini_y_in_suf, mini_y_in_pref)
        if maxi_y - mini_y + 1 <= width_of_road:
            return True
    return False


w, h, n = map(int, input().split())

dots = []
for _ in range(n):
    dots.append(tuple(map(int, input().split())))
dots.sort()

# выписываем отдельно координаты по X и Y
x_coord = []
y_coord = []
for i in range(n):
    x_coord.append(dots[i][0])
    y_coord.append(dots[i][1])

# насчитаем максимальный и минимальный Y на префиксе
pref_maxi_y = [y_coord[0]]
pref_mini_y = [y_coord[0]]

for i in range(1, n):
    pref_maxi_y.append(max(pref_maxi_y[i - 1], y_coord[i]))
    pref_mini_y.append(min(pref_mini_y[i - 1], y_coord[i]))

#  аналогично минимальный и максимальный Y на суффиксе
suf_maxi_y = [0] * n
suf_mini_y = [0] * n
suf_mini_y[-1] = y_coord[-1]
suf_maxi_y[-1] = y_coord[-1]
for i in range(n - 2, -1, -1):
    suf_maxi_y[i] = max(suf_maxi_y[i + 1], y_coord[i])
    suf_mini_y[i] = min(suf_mini_y[i + 1], y_coord[i])

# бин поиск по ширине вертикальной дорожки

l, r = 0, min(h, w)
while r - l > 1:
    m = (l + r) // 2
    if check(m, x_coord, pref_mini_y, pref_maxi_y, suf_mini_y, suf_maxi_y):
        r = m
    else:
        l = m

print(r)
