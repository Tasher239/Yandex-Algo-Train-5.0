from sys import stdin
from collections import OrderedDict
import re


class Statistics:
    def __init__(self):
        self.total_goal = 0
        self.cnt_games = 0
        self.mean_goal = 0
        self.open_goal = 0
        self.gol_minutes = OrderedDict()

    def add_total_goal(self, value):
        self.total_goal += value
        if self.cnt_games != 0:
            self.mean_goal = self.total_goal / self.cnt_games

    def get_total_goal(self):
        return self.total_goal

    def add_cnt_games(self):
        self.cnt_games += 1
        if self.cnt_games != 0:
            self.mean_goal = self.total_goal / self.cnt_games

    def set_cnt_games(self, value):
        self.cnt_games = value
        if self.cnt_games != 0:
            self.mean_goal = self.total_goal / self.cnt_games


    def add_open_goal(self):
        self.open_goal += 1

    def get_open_goal(self):
        return self.open_goal

    def get_cnt_games(self):
        return self.cnt_games

    def get_mean_goal(self):
        return self.mean_goal

    def add_minute_goal(self, minute):
        self.gol_minutes[minute] = self.gol_minutes.get(minute, 0) + 1
        self.gol_minutes = OrderedDict(sorted(self.gol_minutes.items(), key=lambda x: x[0]))

    def get_minute_goal(self):
        return self.gol_minutes

    def __repr__(self):
        return f'total goals: {self.total_goal}\n cnt games: {self.cnt_games}\n' \
               f' mean goal: {self.mean_goal}\n open goal: {self.open_goal}\n goal minutes: {self.gol_minutes}'


team_dict = {}
player_dict = {}
player_in_team = {}

lst = stdin.readlines()
i = 0
while i < len(lst):
    tmp = lst[i].strip().split()
    if tmp[0][0] == '"':
        pattern = r'("[^"]+")\s*-\s*("[^"]+")\s*(\d+):(\d+)'

        # Find matches in the string
        match = re.search(pattern, ' '.join(tmp))

        # Extract team names and scores
        team1 = match.group(1)
        team2 = match.group(2)
        score1 = int(match.group(3))
        score2 = int(match.group(4))

        # Create the list with team names and scores
        score_list = [team1, team2, score1, score2]

        # названия команд и счет
        team1 = score_list[0]
        team2 = score_list[1]
        goal_by_team1 = score_list[2]
        goal_by_team2 = score_list[3]

        team_dict[team1] = team_dict.get(team1, Statistics())
        team_dict[team2] = team_dict.get(team2, Statistics())
        # увеличиваем кол-во игр и кол-во забитых мячей
        st1 = team_dict[team1]
        st1.add_cnt_games()
        st1.add_total_goal(goal_by_team1)

        st2 = team_dict[team2]
        st2.add_cnt_games()
        st2.add_total_goal(goal_by_team2)

        # словарь списков игроков в командах
        player_in_team[team1] = player_in_team.get(team1, set())
        player_in_team[team2] = player_in_team.get(team2, set())

        # считываем голеодоров
        goleadors1 = []
        goleadors2 = []

        already_score = set()
        for _ in range(goal_by_team1):
            i += 1
            goal = (' '.join(lst[i].split()[:-1]), int(lst[i].split()[-1][:-1]))
            player_in_team[team1].add(goal[0])
            player_stat = player_dict.get(goal[0], Statistics())
            player_stat.add_total_goal(1)
            player_stat.add_minute_goal(goal[-1])
            player_dict[goal[0]] = player_stat
            goleadors1.append(goal)

        for player in player_in_team[team1]:
            player_dict[player].set_cnt_games(st1.get_cnt_games())

        for _ in range(goal_by_team2):
            i += 1
            goal = (' '.join(lst[i].split()[:-1]), int(lst[i].split()[-1][:-1]))
            player_in_team[team2].add(goal[0])
            player_stat = player_dict.get(goal[0], Statistics())
            player_stat.add_total_goal(1)
            player_stat.add_minute_goal(goal[-1])
            player_dict[goal[0]] = player_stat
            goleadors2.append(goal)

        for player in player_in_team[team2]:
            player_dict[player].set_cnt_games(st2.get_cnt_games())

        # выясняем какая команда, игрок первая забила в матче
        # print(goleadors1, goleadors2)
        if goal_by_team1 != 0 and goal_by_team2 != 0:
            if goleadors1[0][-1] < goleadors2[0][-1]:
                st1.add_open_goal()
                player_dict[goleadors1[0][0]].add_open_goal()
            else:
                st2.add_open_goal()
                player_dict[goleadors2[0][0]].add_open_goal()
        elif goal_by_team1 != 0:
            st1.add_open_goal()
            player_dict[goleadors1[0][0]].add_open_goal()
        elif goal_by_team2 != 0:
            st2.add_open_goal()
            player_dict[goleadors2[0][0]].add_open_goal()
        # print(player_dict)
        # print(team_dict)

    elif ' '.join(tmp[:3]) == 'Total goals for':
        target_team = ' '.join(tmp[3:])
        # print(target_team)
        if target_team in team_dict:
            # print('Total goals for', end=' ')
            print(team_dict[target_team].get_total_goal())
        else:
            print(0)
    elif ' '.join(tmp[:5]) == 'Mean goals per game for':
        target_team = ' '.join(tmp[5:])
        # print(target_team)
        if target_team in team_dict:
            # print('Mean goals per game for', end=' ')
            print(team_dict[target_team].get_mean_goal())
        else:
            print(0)
    elif ' '.join(tmp[:3]) == 'Total goals by':
        target_player = ' '.join(tmp[3:])
        if target_player in player_dict:
            # print('Total goals by', end=' ')
            print(player_dict[target_player].get_total_goal())
        else:
            print(0)
    elif ' '.join(tmp[:5]) == 'Mean goals per game by':
        target_player = ' '.join(tmp[5:])
        # print(target_player)
        if target_player in player_dict:
            # print('Mean goals per game by', end=' ')
            print(player_dict[target_player].get_mean_goal())
        else:
            print(0)
    elif ' '.join(tmp[:3]) == 'Goals on minute':
        target_player = ' '.join(tmp[5:])
        if target_player in player_dict:
            target_minute = int(tmp[3])
            if target_minute in player_dict[target_player].get_minute_goal():
                # print('Goals on minute', end=' ')
                print(player_dict[target_player].get_minute_goal()[target_minute])
            else:
                print(0)
        else:
            print(0)
    elif ' '.join(tmp[:3]) == 'Goals on first':
        target_player = ' '.join(tmp[6:])
        target_minute = int(tmp[3])
        if target_player in player_dict:
            cnt = 0
            goal_minute_dict = player_dict[target_player].get_minute_goal()
            for minute in goal_minute_dict:
                if minute <= target_minute:
                    cnt += goal_minute_dict[minute]
                else:
                    break
            # print('Goals on first', end=' ')
            print(cnt)
        else:
            print(0)

    elif ' '.join(tmp[:3]) == 'Goals on last':
        target_player = ' '.join(tmp[6:])
        target_minute = int(tmp[3])
        if target_player in player_dict:
            cnt = 0
            goal_minute_dict = player_dict[target_player].get_minute_goal()
            for minute in goal_minute_dict:
                if 90 >= minute >= 91 - target_minute:
                    cnt += goal_minute_dict[minute]
            # print('Goals on last', end=' ')
            print(cnt)
        else:
            print(0)

    elif ' '.join(tmp[:3]) == 'Score opens by':
        target = ' '.join(tmp[3:])
        # print(target)
        if target in team_dict:
            # print('Score opens by', end=' ')
            print(team_dict[target].get_open_goal())
        elif target in player_dict:
            # print('Score opens by', end=' ')
            print(player_dict[target].get_open_goal())
        else:
            print(0)
    i += 1

"""
First team:
A [87, 89]
B [88]

Second Team: 
AA [10]
CC [20, 77, 90



"team1" - "team2" 2:0
messi 5'
suarez 10'
"team1"-"team3" 3:1
messi 25'
neymar 40'
alba 55'
ronaldo 1'
Total goals for "team1"
Total goals for "team2"
Mean goals per game for "team1"
Mean goals per game for "team3"
Total goals by messi
Total goals by busects
Mean goals per game by messi
Mean goals per game by ronaldo
Goals on minute 1 by ronaldo
Goals on minute 1 by messi
Goals on first 25 minutes by messi
Goals on last 10 minutes by messi
Score opens by "team1"
Score opens by messi
Score opens by ronaldo
"""
