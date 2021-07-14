import sys
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas

NUM_PLAYERS_RETURNED = 5
MIN_GP = 20
AGE_MULTIPLIER = 0.8
OTHER_LEAGUE_MULTIPLIER = 0.1
EQUIVALENT_LEAGUES = ['OHL', 'WHL', 'QMJHL']


def getScoringRate(gp, p, league):
    if league in nhle:
        return (p / gp) * nhle[league]
    else:
        return (p / gp) * OTHER_LEAGUE_MULTIPLIER


if len(sys.argv) != 7:
    raise ValueError('Please provide the following arguments: League, Position (F/D), Age, GP, G, A')
    
nhle_csv = pandas.read_csv(r'nhl_translations.csv')
nhle = dict(zip(nhle_csv["League"], nhle_csv["Era-Adjusted"]))

# Use NHLe just for CHL leagues
if sys.argv[1] not in EQUIVALENT_LEAGUES:
    player_gpp = (int(sys.argv[5]) + int(sys.argv[6])) / int(sys.argv[4])
else:
    player_gpp = getScoringRate(int(sys.argv[4]), (int(sys.argv[5]) + int(sys.argv[6])), sys.argv[1])

df = pandas.read_csv(r'historical_prospect_stats.csv')

if sys.argv[1] not in EQUIVALENT_LEAGUES:
    df = df[df.League == sys.argv[1]]

df = df[df.Pos == sys.argv[2]]
df = df[df.Age == int(sys.argv[3])]
df = df[df.GP >= MIN_GP]
comparables = df.to_numpy()

all_gpps = dict()
for comparable in comparables:
    # Use NHLe just for CHL leagues
    if sys.argv[1] not in EQUIVALENT_LEAGUES:
        all_gpps[comparable[0]] = comparable[8] / comparable[5]
    else:
        all_gpps[comparable[0]] = getScoringRate(comparable[5], comparable[8], comparable[4])

for i in range(NUM_PLAYERS_RETURNED):
    comp, value = min(all_gpps.items(), key = lambda x: abs(x[1] - player_gpp))
    all_gpps.pop(comp, None)
    print(df.loc[df['PID'] == comp])


#train = np.array([sys.argv[3], sys.argv[4], sys.argv[5]])
#train = train.reshape(1, -1)

#df = pandas.read_csv(r'historical_prospect_stats.csv')
#df = df[df.League == sys.argv[1]]
#df = df[df.Pos == sys.argv[2]]
#df = df[["GP", "G", "A"]]
#test = df.to_numpy()
#nbrs = NearestNeighbors(n_neighbors=5, algorithm='auto').fit(test)
#distances, indices = nbrs.kneighbors(train)
#print(indices)