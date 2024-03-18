#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: David P. Fleming, 2024

Script to scrape game logs for each CBB team in a given set of years

"""
import os
import pandas as pd
import numpy as np
import majerus as mj
from time import sleep

# Top level params
verbose = False
data_dir = 'data'

# Make rng for random sleep times
rng = np.random.default_rng()

# Get list of unique team names
teams = mj.parser.get_all_teams()

# Loop over years
#years = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2023, 2023]
years = [2019]
for year in years:

    season_df = None

    # Loop over teams
    for team in teams:

        # Wait random time
        sleep(rng.uniform(low=0.0, high=3.0))

        try:
            print(team)

            # Get data for team in given season
            df = mj.scraper.scrape_team_game_logs(team, year, verbose=verbose,
                                                  normalize_names=True)

            # Combine dataframes
            if season_df is None:
                season_df = df.copy()
            else:
                season_df = pd.concat([season_df, df], axis=0, ignore_index=True)
        except:
            print(f"{team} did not play D1 basketball in the {year}-{year+1} season.")

    # Scraped for all teams in given season - save
    season_df.to_csv(os.path.join(data_dir, f"all_gamelogs_{year}_{year+1}.csv"), na_rep='NAN')