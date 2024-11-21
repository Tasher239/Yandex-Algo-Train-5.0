def cnt_votes(i, votes, suf, level):  # сколько голосов над уровнем стрижки
    # бин-поиском ищем первого над уровнем стрижки,
    # после чего считаем сумму над стрижкой
    # left - индекс последнего столба < уровня стрижки m
    # right - индекс первого столба >= уровня стрижки
    l, r = -1, n
    while r - l > 1:
        m = (l + r) // 2
        if votes[m][0] < level:
            l = m
        else:
            r = m
    cnt_buy = suf[r] - (n - r) * level
    if votes[i][0] > level:
        cnt_buy -= (votes[i][0] - level)
    return cnt_buy


def model(i, votes, suf):  # сколько надо купить голосов, чтобы i партия выиграла
    # Бин-поиск по высоте столба
    # l - максимально возможный уровень стрижки, когда голосов еще хватает
    l, r = 0, maxi_vote + 1
    while r - l > 1:
        # level - уровень стрижки
        level = (r + l) // 2
        cnt_buy = cnt_votes(i, votes, suf, level)  # кол-во купленных голосов

        # если суммарно над уровнем стрижки больше чем надо,
        # то поднимаем левую границу поиска
        if cnt_buy + votes[i][0] > level:
            l = level
        else:
            r = level
    cnt_buy = cnt_votes(i, votes, suf, l)
    # если мы выше уровня стрижки больше, чем на 2, то можно вернуть голоса
    otday = max(0, (votes[i][0] + cnt_buy) - (l + 2))

    return cnt_buy - otday, l, otday


# Чтение данных
n = int(input())
votes = []
vzatka = []
maxi_vote = 0
for i in range(n):
    vt, vz = map(int, input().split())
    maxi_vote = max(maxi_vote, vt)
    votes.append([vt, i])
    vzatka.append(vz)
votes.sort()
# Суффиксные суммы чтобы быстро считать голоса над
# уровнем стрижки
suf = [0] * (n + 1)
suf[-2] = votes[-1][0]
for i in range(n - 2, -1, -1):
    suf[i] = suf[i + 1] + votes[i][0]

min_sm = float('inf')
for i in range(n):
    # Смотрим только на продажные партии
    if vzatka[votes[i][1]] != -1:

        # для ответа понадобится минимальное кол-во денег (bye), потраченные на покупку голосов,
        # уровень стрижки, чтобы понизить всех, кто будет выше и
        # otday - лишние голоса, которые надо вернуть

        # функция model - моделирует процесс и выдает параметры выше для каждой партии
        cnt_buy, level, otday = model(i, votes, suf)
        if vzatka[votes[i][1]] + cnt_buy < min_sm:
            min_sm = vzatka[votes[i][1]] + cnt_buy
            ans = [votes[i][1], cnt_buy, level, otday]

# восстановление распределения голосов

ind_win_part = ans[0]
ans_buy = ans[1]
ans_level = ans[2]
ans_otday = ans[3]
ans_vote = [0] * n

for i in range(n):
    if votes[i][1] == ind_win_part:
        ans_vote[votes[i][1]] = (votes[i][0] + ans_buy)
    elif votes[i][0] > ans_level:
        if ans_otday > 0:
            ans_vote[votes[i][1]] = ans_level + 1
            ans_otday -= 1
        else:
            ans_vote[votes[i][1]] = ans_level
    else:
        ans_vote[votes[i][1]] = votes[i][0]

print(min_sm)
print(ans[0] + 1)
print(*ans_vote)
