import requests
import json
from functools import cmp_to_key
from pool import get_pool

espn_url = 'https://www.espn.com/golf/leaderboard'

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
    response = requests.get(url=espn_url)

    return parse_espn_response(response)

def parse_espn_response(response):
    raw = response.text
    start_index = raw.find('\"competitors\":')
    end_index = raw.find(',\"rawText\":')

    raw_leaderboard = "{" + raw[start_index : end_index] + "}"

    return json.loads(raw_leaderboard)

def get_player_scores(leaderboard, member):

    # Iterate through each player of a given pool member
    i = 0
    for player_pick in member['players']:

        # linear search for the player and add score to member
        for p in leaderboard['competitors']:
            if p['name'] == player_pick['name']:
                member['players'][i]['curr_score'] = p['toPar']
                break
        
        i += 1

    return member


def calculate_member_score(member):
    scores = []
    for player in member['players']:
        score = 0
        try:
            if isInt(player['curr_score']):
                score = int(player['curr_score'])
        except:
            print('player unavailable:')
            print(player)
        
            
        scores.append(score)

    return sum(sorted(scores)[:4])


def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False