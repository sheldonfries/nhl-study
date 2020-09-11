import requests
import json
import pandas

# Import player ids from csv
df = pandas.read_csv(r'player_ids.csv')
player_ids = df['id'].to_list()


data = {'id': [], 'name': [], 'pos': [], 'evenTimeOnIce': [], 'evenPoints': []}
df_out = pandas.DataFrame(data)
df_name = df.set_index("id", drop = False)

for id in player_ids:
    dump = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(id) + '/stats?stats=statsSingleSeason&season=20192020')
    dump = json.loads(dump.content)
    if dump["stats"][0]["splits"]:
        dump = dump["stats"][0]["splits"][0]["stat"]
        row = {'id': id, 'name': df_name.loc[id, "name"], 'pos': df_name.loc[id, "pos"], 'evenTimeOnIce': dump["evenTimeOnIce"], 'evenPoints': dump["points"] - dump["powerPlayPoints"] - dump["shortHandedPoints"]}
        df_out = df_out.append(row, ignore_index=True)

df_out.to_csv(r'player_data.csv', sep=",")
