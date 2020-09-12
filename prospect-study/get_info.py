import requests
import json
import pandas

draft_url = 'https://statsapi.web.nhl.com/api/v1/draft/'
prospect_ids = []
prospect_names = []
prospect_draft_years = []
prospect_overalls = []

for i in range(1990, 2016):
    draft_data = requests.get(draft_url + str(i))
    draft_data = json.loads(draft_data.content)
    draft_data = draft_data["drafts"]

    for draft in draft_data:
        for round in draft["rounds"]:
            for pick in round["picks"]:
                if "id" in pick["prospect"]:
                    prospect_ids.append(pick["prospect"]["id"])
                    prospect_names.append(pick["prospect"]["fullName"])
                    prospect_draft_years.append(pick["year"])
                    prospect_overalls.append(pick["pickOverall"])

prospect_url = 'https://statsapi.web.nhl.com/api/v1/draft/prospects/'
prospect_positions = []
player_ids = []
player_birth_dates = []

for id in prospect_ids:
    prospect_data = requests.get(prospect_url + str(id))
    prospect_data = json.loads(prospect_data.content)
    prospect_data = prospect_data["prospects"]

    for prospect in prospect_data:
        prospect_positions.append(prospect["primaryPosition"]["code"])
        #player_birth_dates.append(prospect["birthDate"].split("-")[0])
        player_birth_dates.append(prospect["birthDate"])
        if "nhlPlayerId" in prospect:
            player_ids.append(prospect["nhlPlayerId"])
        else:
            player_ids.append("None")

df = pandas.DataFrame(data={"id": prospect_ids, "name": prospect_names, "year": prospect_draft_years, "overall": prospect_overalls, "Pos": prospect_positions, "BirthDate": player_birth_dates, "PID": player_ids})
df.to_csv("./historical_prospect_info.csv", sep=",", index=False)
