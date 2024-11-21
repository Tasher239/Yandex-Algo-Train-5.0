n = int(input())
a = []
b = []
for i in range(n):
    a_i, b_i = map(int, input().split())
    a.append((a_i, i))
    b.append((b_i, i))

obsh = []
for i in range(n):
    obsh.append((a[i][0], a[i][0] - b[i][0], i))

positive = []
negative = []
for i in range(n):
    if obsh[i][1] >= 0:
        positive.append(obsh[i])
    else:
        negative.append(obsh[i])

minus = []
sm = 0
for i in range(len(positive)):
    sm += positive[i][1]
for i in range(len(positive)):
    minus.append(sm - positive[i][1])

ind_maxi_neg = 0
if len(negative) != 0:
    for i in range(len(negative)):
        if negative[i][0] > negative[ind_maxi_neg][0]:
            ind_maxi_neg = i

ind_maxi = 0
if len(positive) != 0:
    for i in range(len(positive)):
        if minus[ind_maxi] + positive[ind_maxi][0] < minus[i] + positive[i][0]:
            ind_maxi = i

if len(negative) == 0 or (
        len(positive) > 0 and sm + negative[ind_maxi_neg][0] <= minus[ind_maxi] + positive[ind_maxi][0]):
    print(minus[ind_maxi] + positive[ind_maxi][0])
    for i in range(len(positive)):
        if i != ind_maxi:
            print(positive[i][2] + 1, end=' ')
    print(positive[ind_maxi][2] + 1, end=' ')
    print(*[x[2] + 1 for x in negative])
else:
    print(sm + negative[ind_maxi_neg][0])
    print(*([x[2] + 1 for x in positive]), end=' ')
    print(negative[ind_maxi_neg][2] + 1, end=' ')
    for i in range(len(negative)):
        if i != ind_maxi_neg:
            print(negative[i][2] + 1, end=' ')
