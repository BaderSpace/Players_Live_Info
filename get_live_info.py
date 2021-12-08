import requests
import json
from typing import Dict, Any
import hashlib
import time

#codes to know what did the player did

codess = {'36': 'Goals', '37': 'Goals', '39': 'OG',
          '63': 'Assist', '43': 'Cards', '45': 'Cards', '44': 'Cards'}

codes = {'36': 1, '37': 1, '39': 1, '63': 1,
         '43': 'Yellow Card', '45': 'Red Card', '44': 'Red Card (2 Yellows)'}

#store the players in json file


def store(players):
    teams = {}
    y = 0
    for k, kv in players.items():
        y += 1
        teams[f"team{y}"] = [{x: {'OG': 0, 'Goals': 0, 'Assist': 0, 'Cards': ''}}
                             for x in kv]
    with open('results.json', 'w') as file:
        file.write(json.dumps(teams))
    return teams

#get the players from the GET request returns json file


def get_players(Pjson):
    global Players_shortcuts
    pn = ''
    Players_shortcuts = {}
    teams = {}
    lst = []
    info = json.loads(Pjson.text)
    Lu = info['Lu']
    y = 0
    while y < 2:
        Ps = Lu[y]['Ps']
        for k in Ps:
            try:
                pn = k['Snm']
                lst.append(pn)
                Players_shortcuts[k['Snm'][0].capitalize(
                ) + '. ' + pn.split(' ')[1]] = pn
            except:
                try:
                    pn += k['Fn'] + ' ' + k['Ln']
                    lst.append(pn)
                    Players_shortcuts[k['Fn']
                                      [0].capitalize() + '. ' + k['Ln']] = pn
                except:
                    pn = k['Ln']
                    Players_shortcuts[k['Ln']] = pn
                    lst.append(pn)

            pn = ''
        teams[f'team{y+1}'] = lst.copy()
        lst.clear()
        y += 1

    return teams

#request


def request(url):
    r = requests.get(url)
    return r


def hashing(dict):
    strs = ""
    for k, v in dict.items():
        strs += str(v)
    return hash(strs)


def get_stat(url):
    r = request(url)
    data = json.loads(r.text)
    Incs = data["Incs"].items()
    for k, v in Incs:
        for x in v:
            try:
                ha = hashing(x['Incs'][0])
                ha2 = hashing(x['Incs'][1])
                if ha not in Hashes and ha2 not in Hashes:
                    try:
                        Player_name = Players_shortcuts[x['Incs'][0]['Pn']]
                        Second_player_name = Players_shortcuts[x['Incs'][1]['Pn']]
                    except:
                        Player_name = x['Incs'][0]['Pn']
                        Second_player_name = x['Incs'][1]['Pn']
                    Player_code = str(x['Incs'][0]['IT'])
                    Second_player_code = str(x['Incs'][1]['IT'])
                    apply_stat(Player_name, Player_code)
                    apply_stat(Second_player_name, Second_player_code)
                    Hashes.append(ha)
                    Hashes.append(ha2)
                else:
                    pass

            except:
                ha = hashing(x)
                if ha not in Hashes:
                    try:
                        Player_name = Players_shortcuts[x['Pn']]
                    except:
                        Player_name = x['Pn']
                    Player_code = str(x['IT'])
                    apply_stat(Player_name, Player_code)
                    Hashes.append(ha)
                else:
                    pass


def apply_stat(Pname, code):
    with open('results.json', 'r') as f:
        data = json.loads(f.read())
        for k, v in data.items():
            for i in v:
                for s, ss in i.items():
                    if s == Pname:
                        if code == '44':
                            ss[codess[code]] = ""
                        else:
                            pass
                        ss[codess[code]] += codes[code]
                        print(ss, Pname)
                    else:
                        pass
    with open('results.json', 'w') as f:
        f.write(json.dumps(data))


url = 'https://prod-public-api.livescore.com/v1/api/react/match-x/soccer/534916/3.00?MD=1'
try:
    store(get_players(request(url)))
except Exception as e:
    print('store: ', e)
    pass


def main():
    global Hashes
    Hashes = []
    r = request(url)
    data = json.loads(r.text)
    while data['Eps'] != 'FT':
        data = json.loads(request(url).text)
        try:
            print(data['Eps'])
            get_stat(url)
        except Exception as e:
            print("get: ", e)
            pass
        time.sleep(60)


try:
    main()
except KeyboardInterrupt:
    print('Done')
