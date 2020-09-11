import requests
import json
import pandas

team_data = requests.get('https://statsapi.web.nhl.com/api/v1/teams')
team_data = json.loads(team_data.content)
team_data = team_data["teams"]
team_ids = []

for team in team_data:
    team_ids.append(team["id"])

player_ids = []
player_names = []
player_pos = []
for id in team_ids:
    team_players = requests.get('https://statsapi.web.nhl.com/api/v1/teams/'+ str(id) + '/roster')
    team_players = json.loads(team_players.content)
    team_players = team_players["roster"]
    
    for player in team_players:
        if player["position"]["code"] != "G":
            player_ids.append(player["person"]["id"])
            player_names.append(player["person"]["fullName"])
            player_pos.append(player["position"]["code"])

df = pandas.DataFrame(data={"id": player_ids, "name": player_names, "pos": player_pos})
df.to_csv("./player_ids.csv", sep=",", index=False)

