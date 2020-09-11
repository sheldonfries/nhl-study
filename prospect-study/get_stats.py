import requests
import json
import pandas

def getAge(date, draftYear):
    date = date.split("-")
    year = int(date[0])
    #month = int(date[1])
    #day = int(date[2])
    age = int(draftYear) - year
    
    return age

def getPos(pos):
    if pos == 'D':
        return pos
    else:
        return 'F'

# Import player ids from csv
df = pandas.read_csv(r'historical_prospect_info.csv')
df = df[df.Pos != 'G']
df = df[df.PID != 'None']
df = df.drop_duplicates(subset=['PID'])
player_ids = df['PID'].to_list()

data = {'PID': [], 'Name': [], 'Pos': [], 'Age': [], 'League': [], 'GP': [], 'G': [], 'A': [], 'P': [], 'Year': [], 'Overall': []}
df_out = pandas.DataFrame(data)
df_name = df.set_index("PID", drop = False)

for id in player_ids:
    dump = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(id) + '/stats?stats=yearByYear')
    dump = json.loads(dump.content)
    if "stats" in dump:
        dump = dump["stats"]
    else:
        continue
    year = df_name.loc[id, "year"]
    birthdate = df_name.loc[id, "BirthDate"]
    age = getAge(birthdate, year)
    pos = getPos(df_name.loc[id, "Pos"])
    
    for stat in dump:
        for season in stat["splits"]:
            draft_season = str(year - 1) + str(year)
            if season["season"] == draft_season:
                data = season["stat"]
                if "games" in data and "goals" in data and "assists" in data:
                    row = {'PID': id, 'Name': df_name.loc[id, "name"], 'Pos': pos, 'Age': age, 'League': season["league"]["name"], 'GP': data["games"], 'G': data["goals"], 'A': data["assists"], 'P': data["goals"] + data["assists"], 'Year': year, 'Overall': df_name.loc[id, "overall"]}
                    df_out = df_out.append(row, ignore_index=True)

df_out.to_csv(r'historical_prospect_stats.csv', sep=",", index=False)