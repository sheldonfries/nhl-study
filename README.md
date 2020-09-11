# NHL Player/Prospect Study

Scrapes data from NHL.com to be used in studies on NHL players and prospects.

## Setup

Run the following code for first-time use to set up the python3 virtual environment and install the requirements.

```sh
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r reqs.txt
```

If the requirements haven't been changed after the initial setup, the following command is enough.

```sh
$ source venv/bin/activate
```

## Player Study

This study aims to use the collected data in order to classify NHL players into specific "buckets" (e.g. first-liner, AHLer, etc.).

#### Collecting Data

Run the following code to collect data from NHL.com and store it in local csv files.

```sh
$ cd player-study
$ python3 get_player_ids.py
$ python3 get_player_data.py
```

The collected data will be stored in `player_data.csv`.

## Prospect Study

This study aims to use the collected data in order to classify NHL prospects into specific "buckets" (e.g. first-liner, AHLer, etc.) by using historical data to find player comparables.

#### Collecting Data

Run the following code to collect data from NHL.com and store it in local csv files.

```sh
$ cd prospect-study
$ python3 get_info.py
$ python3 get_stats.py
```

The collected data will be stored in `historical_prospect_stats.csv`.

#### Finding Comparables

Run the following code to generate the closest comparables for a given prospect.

```sh
$ python3 calc.py [League] [Position] [Age] [Games Played] [Goals] [Assists]
```

The script will output the five closest comparables based on the historical data. The number of comparables can be changed with the `NUM_PLAYERS_RETURNED` constant.

## Future Work
- Do more cleaning of the data in get_info/get_stats to ensure that league names are correct and consistent, and to avoid providing comparables with low GP.
- Use NHLe or a similar system to find best comparisons across leagues, rather than limiting comparables to the same league.
- Use nearest neighbours to classify prospect (first line, etc.) rather than just providing comparables => requires labels for comparables