from collections import OrderedDict

n, k = map(int, input().split())
devices_dict =  {}
frequency_of_piece_in_system = {}
devices_dict[0] = [1] * k
for i in range(1, n):
    devices_dict[i] = [0] * (k+1)

for i in range(k):
    frequency_of_piece_in_system[i] = 1

worth_dict = {}
for i in range(n):
    worth_dict[i] = {}
    for j in range(n):
        if i != j:
            worth_dict[i][j] = 0
time_ready_lst = [-1] * n
t = 1
ready_set = {0}
rt = 0
while len(ready_set) < n:
    # 1. choice most rare piece with min number
    choice_dict = {}
    for dev in devices_dict:
        min_cur_freq = float('inf')
        for i in range(k):
            if devices_dict[dev][i] == 0 and frequency_of_piece_in_system[i] < min_cur_freq:
                choice_dict[dev] = i
                min_cur_freq = frequency_of_piece_in_system[i]

    # 2. Request chosen piece
    request_dev = {}
    for dev in choice_dict:
        need_piece = choice_dict[dev]
        min_cnt_updates = float('inf')
        final_receiver = -1
        for receiver in devices_dict:
            if devices_dict[receiver][need_piece] == 1 and devices_dict[receiver][-1] < min_cnt_updates:
                min_cnt_updates = devices_dict[receiver].count(1)
                final_receiver = receiver
        request_dev[final_receiver] = request_dev.get(final_receiver, []) + [(dev, need_piece)]

    # 3. satisfaction of the request
    stisfact_req = {}
    for receiver in request_dev:
        # chose maximum worth from requests
        final_load = -1
        cnt_loads_in_final = float('inf')
        lst_requests = request_dev[receiver]
        max_worth = -float('inf')
        for req in lst_requests:
            if worth_dict[receiver][req[0]] == max_worth:
                if devices_dict[req[0]][-1] < cnt_loads_in_final:
                    cnt_loads_in_final = devices_dict[req[0]][-1]
                    final_load = req
            elif worth_dict[receiver][req[0]] > max_worth:
                final_load = req
                max_worth = worth_dict[receiver][req[0]]
                cnt_loads_in_final = devices_dict[req[0]][-1]
        stisfact_req[receiver] = final_load

    for receiver in stisfact_req:
        req = stisfact_req[receiver]
        devices_dict[req[0]][req[1]] = 1
        devices_dict[req[0]][-1] += 1
        frequency_of_piece_in_system[req[1]] += 1
        worth_dict[req[0]][receiver] += 1

    for dev in devices_dict:
        if dev != 0 and devices_dict[dev][-1] == k and time_ready_lst[dev] == -1:
            time_ready_lst[dev] = t
            ready_set.add(dev)
    t += 1
    rt += 1

print(*time_ready_lst[1:])
