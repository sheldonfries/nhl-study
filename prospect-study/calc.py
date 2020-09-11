###
# FUTURE WORK:
# - Use NHLe to find best comparisons across leagues?
# - Use nearest neighbours to classify prospect (first line, etc.) => requires labels for comparables
###

import sys
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas

NUM_PLAYERS_RETURNED = 5

if len(sys.argv) != 7:
    raise ValueError('Please provide the following arguments: League, Position (F/D), Age, GP, G, A')
    
player_gpp = (int(sys.argv[5]) + int(sys.argv[6])) / int(sys.argv[4])
df = pandas.read_csv(r'historical_prospect_stats.csv')
df = df[df.League == sys.argv[1]]
df = df[df.Pos == sys.argv[2]]
df = df[df.Age == int(sys.argv[3])]
comparables = df.to_numpy()

all_gpps = dict()
for comparable in comparables:
    all_gpps[comparable[0]] = comparable[8] / comparable[5]

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