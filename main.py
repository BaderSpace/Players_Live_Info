import requests
import json
import time
codess = {'36': 'Goals', '37': 'Goals', '39': 'OG',
          '63': 'Assist', '43': 'Cards', '45': 'Cards'}
#codes to know what did the player did
codes = {'36': 1, '37': 1, '39': 1, '63': 1,
         '43': 'Yellow Card', '45': 'Red Card'}

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


def get_stat(url):
    r = request(url)
    data = json.loads(r.text)
    Incs = data["Incs"].items()
    for k, v in Incs:
        for x in v:
            try:
                id = str(x['Incs'][0]['ID'])
                id2 = str(x['Incs'][1]['ID'])
                if id not in IDs and id2 not in IDs:

                    Player_name = x['Incs'][0]['Pn']
                    Second_player_name = x['Incs'][1]['Pn']
                    Player_code = str(x['Incs'][0]['IT'])
                    Second_player_code = str(x['Incs'][1]['IT'])
                    apply_stat(Player_name, Player_code, id)
                    apply_stat(Second_player_name, Second_player_code, id2)
                    IDs.append(id)
                    IDs.append(id2)
                else:
                    pass

            except:
                id = str(x['ID'])
                if id not in IDs:

                    Player_name = x['Pn']
                    Player_code = str(x['IT'])
                    apply_stat(Player_name, Player_code, id)
                    IDs.append(id)
                else:
                    pass


def apply_stat(Pname, code, id):
    with open('results.json', 'r') as f:
        data = json.loads(f.read())
        for k, v in data.items():
            for i in v:
                for s, ss in i.items():
                    if s == Pname:
                        ss[codess[code]] += codes[code]
                        print(ss, Pname)
                    else:
                        pass
    with open('results.json', 'w') as f:
        f.write(json.dumps(data))


url = 'https://prod-public-api.livescore.com/v1/api/react/match-x/soccer/401155/3.00?MD=1'

store(get_players(request(url)))


def main():
    global IDs
    IDs = []
    r = request(url)
    data = json.loads(r.text)
    while data['Eps'] != 'FT':
        data = json.loads(request(url).text)
        try:
            get_stat(url)
            print(IDs)
        except:
            pass
        time.sleep(60)


main()
