import requests
from pool import get_pool

leaderboard_url = 'http://samsandberg.com/themasters/'

def update_pool():
    leaderboard = fetch_leaderboard()
    pool = get_pool()

    pool_standings = []

    for member in pool:
        score = calculate_score(leaderboard, member)
        pool_standings.append({
            'pool_member': member,
            'score': score
        })

    return sorted(pool_standings, key=lambda member: member['score'])


def fetch_leaderboard():
    response = requests.get(url=leaderboard_url)
    return response.json()


def calculate_score(leaderboard, member):

    score = 0

    # Iterate through each player of a given pool member
    for player_pick in member['players']:
        # linear search for the player and add score
        for p in leaderboard['players']:
            if p['player'] == player_pick['name'] and p['to_par'] != 'CUT':
                score += int(p['to_par'])
                break

    return score