import subprocess

#TESTING
lst = ['https://prod-public-api.livescore.com/v1/api/react/match-x/soccer/534928/3.00?MD=1',
       'https://prod-public-api.livescore.com/v1/api/react/match-x/soccer/535468/3.00?MD=1']

for i in lst:
    subprocess.Popen(
        f'python get_live_info.py {i}', creationflags=subprocess.CREATE_NEW_CONSOLE)
