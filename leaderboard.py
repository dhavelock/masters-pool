import requests
from functools import cmp_to_key
from pool import get_pool

leaderboard_url = 'http://samsandberg.com/themasters/'

def update_pool():
    leaderboard = fetch_leaderboard()
    pool = get_pool()

    pool_standings = []

    for member in pool:
        member = get_player_scores(leaderboard, member)
        score = calculate_member_score(member)
        
        pool_standings.append({
            'pool_member': member,
            'score': score
        })

    return sorted(pool_standings, key=lambda member: member['score'])


def fetch_leaderboard():
    response = requests.get(url=leaderboard_url)
    return response.json()


def get_player_scores(leaderboard, member):

    # Iterate through each player of a given pool member
    i = 0
    for player_pick in member['players']:

        # linear search for the player and add score to member
        for p in leaderboard['players']:
            if p['player'] == player_pick['name']:
                member['players'][i]['curr_score'] = p['to_par']
                break
        
        i += 1

    return member


def calculate_member_score(member):
    scores = []
    for player in member['players']:
        score = 0
        if isInt(player['curr_score']):
            score = int(player['curr_score'])
            
        scores.append(score)

    return sum(sorted(scores)[:3])


def compare_players(p1, p2):
    if p2['to_par'] == 'CUT':
        return -1
    elif p1['to_par'] == 'CUT':
        return 1
    elif p1['to_par'] < p2['to_par']:
        return -1
    elif p1['to_par'] > p2['to_par']:
        return 1
    else:
        return 0


def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False