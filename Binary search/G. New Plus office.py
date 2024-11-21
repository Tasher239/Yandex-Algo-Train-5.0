def check(n, m, lst, target_side, pref_sum):
    for i in range(n - 3 * target_side + 1):
        for j in range(target_side, m - 2 * target_side + 1):
            if lst[i][j] == 1:
                if (pref_sum[i + target_side][j + target_side] - pref_sum[i][j + target_side] -
                    pref_sum[i + target_side][j] + pref_sum[i][j]) == target_side ** 2 and \
                        (pref_sum[i + 2 * target_side][j] - pref_sum[i + target_side][j] -
                         pref_sum[i + 2 * target_side][j - target_side] + pref_sum[i + target_side][
                             j - target_side]) == target_side ** 2 and \
                        (pref_sum[i + 2 * target_side][j + target_side] - pref_sum[i + target_side][j + target_side] -
                         pref_sum[i + 2 * target_side][j] + pref_sum[i + target_side][j]) == target_side ** 2 and \
                        (pref_sum[i + 2 * target_side][j + 2 * target_side] - pref_sum[i + target_side][
                            j + 2 * target_side] - pref_sum[i + 2 * target_side][j + target_side] +
                         pref_sum[i + target_side][j + target_side]) == target_side ** 2 and \
                        (pref_sum[i + 3 * target_side][j + target_side] - pref_sum[i + 2 * target_side][
                            j + target_side] - pref_sum[i + 3 * target_side][j] + pref_sum[i + 2 * target_side][
                             j]) == target_side ** 2:
                    return True
    return False


n, m = map(int, input().split())
# n-длина, m-ширина

pref_sum = [[0] * (m + 1) for _ in range(n + 1)]
lst = [[0] * m for _ in range(n)]

for i in range(n):
    tmp = list(input())
    for j in range(m):
        if tmp[j] == '.':
            lst[i][j] = 0
        else:
            lst[i][j] = 1
        pref_sum[i + 1][j + 1] = lst[i][j] + pref_sum[i][j + 1] + pref_sum[i + 1][j] - pref_sum[i][j]

l, r = 1, min(n, m)
while r - l > 1:
    mid = (l + r) // 2
    if check(n, m, lst, mid, pref_sum):
        l = mid
    else:
        r = mid
print(l)

"""
  1
2 3 4
  5

"""
