import requests
import json


#codes to know what did the player did
codes = {36: 'Goal', 37: 'Pen goal', 63: 'Assist', 43: 'Yellow card'}

#Player class no use for now


class Player:
    Players_goals = {}

    def __init__(self, Pname):
        self.Pname = Pname
        pass

    def get_goals(self):
        r = request(
            'https://prod-public-api.livescore.com/v1/api/react/match-x/soccer/469055/3.00?MD=1')
        goals_dict = json.loads(r.text)
        #Incs = goals_dict
        return

    def get_cards(self):
        pass

    def get_stat(self):
        pass

#store the players in json file


def store(players):
    teams = {}
    y = 0
    for k, kv in players.items():
        y += 1
        teams[f"team{y}"] = [{x: {'goals': 0, 'cards': '', 'stat': ''}}
                             for x in kv]
    with open('results.json', 'w') as file:
        file.write(json.dumps(teams, indent=4))
    return teams

#get the players from the GET request returns json file


def get_players(Pjson):
    teams = {}
    lst = []
    info = json.loads(Pjson.text)
    Lu = info['Lu']
    y = 0
    while y < 2:
        Ps = Lu[y]['Ps']
        for k in Ps:
            lst.append(k['Snm'])
        teams[f'team{y+1}'] = lst.copy()
        lst.clear()
        y += 1

    return teams

#request


def request(url):
    r = requests.get(url)
    return r


#for testing West Ham United vs Chelsea
pl = store(get_players(request(
    'https://prod-public-api.livescore.com/v1/api/react/match-x/soccer/469055/3.00?MD=1')))
