# const teams = [
#   {
#     name: JSS,
#     roster: ['Rory', 'Collin', 'Brooks', 'Tommy'],
#     // score
#   },
# ];

import json 

raw_teams = []
teams = []

with open('raw_poolinfo.csv', 'r') as file:
    for line in file:
        raw_teams.append(line.split(','))

for j in range(len(raw_teams[0])):
    team_obj = {
        "name": raw_teams[0][j]
    }

    roster = []
    for i in range(1, 9):
        roster.append(raw_teams[i][j])

    team_obj['roster'] = roster
    teams.append(team_obj)


result = open('poolinfo.json', 'w')
result.write(json.dumps(teams))
    