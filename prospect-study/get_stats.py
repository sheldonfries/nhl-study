import requests
import json
import pandas
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

def getAge(date, draftYear):
    draftDate = str(draftYear) + "-09-15"
    date1 = parse(draftDate)
    date2 = parse(date)
    rdelta = relativedelta(date1, date2)
    return rdelta.years

def getPos(pos):
    if pos == 'D':
        return pos
    else:
        return 'F'
    
def fixLeagueName(league):
    if league == "Czech":
        return "CzRep"
    elif league == "Czech2" or league == "Czech-2":
        return "CzRep-2"
    elif league == "Czech-Jr.":
        return "CzRep-Jr."
    elif league == "Liiga":
        return "Finland"
    elif league[0:4] == "High":
        return "HS"
    elif league == "KHL":
        return "Russia"
    elif league == "Big Ten" or league == "ECAC" or league == "H-East" or league == "NCHC" or league == "WCHA":
        return "NCAA"
    elif league == "NLA":
        return "Swiss"
    elif league == "Russia2":
        return "Russia-2"
    elif league == "Russia3":
        return "Russia-3"
    elif league == "SHL":
        return "Sweden"
    elif league == "SuperElit":
        return "Sweden-2"
    else:
        return league

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
                    row = {'PID': id, 'Name': df_name.loc[id, "name"], 'Pos': pos, 'Age': age, 'League': fixLeagueName(season["league"]["name"]), 'GP': data["games"], 'G': data["goals"], 'A': data["assists"], 'P': data["goals"] + data["assists"], 'Year': year, 'Overall': df_name.loc[id, "overall"]}
                    df_out = df_out.append(row, ignore_index=True)

df_out.to_csv(r'historical_prospect_stats.csv', sep=",", index=False)