#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Functions and utilities for taking a complete list of a season's gamelogs and
converting it into a dataset where each row corresponds to 1 game. Each row
contains aggregated statistics for each team (denoted team and opponent) and
response variables that indicate the result of the game, e.g. whether or not team
won the game and what the total score was.

@author: David P. Fleming, 2024
"""

import pandas as pd
import numpy as np
import os
from . import parser


__all__ = ["process_game_logs"]


def __home_name(location : str, team : str, opponent : str) -> str:
    """
    Simple function to identify name of home team

    Parameters
    ----------
    location : str
        Home (H), Away (A), or neutral site (N)
    team : str
        Team name
    opponent : str
        Opponent name
    
    Returns
    -------
    home_name : str
        Name of home team
    """
    if location == "H" or location == "N":
        return team
    else:
        return opponent


def process_game_logs(df : pd.DataFrame, team : str, 
                      skip_first_n : str=10, verbose : bool=False) -> pd.DataFrame:
    """
    Process game_logs from df into a dataframe where each row
    corresponds to a single game from each team. The columns, or features, are
    the statistics for team and its opponent, aggregated over all prior games
    that season, ignoring the skip_first_n in the season.

    Parameters
    ----------
    df : pandas.DataFrame
        dataframe of gamelogs file loaded in via something like the following:
        df = os.path.join("../Data","allGamelogs20172018.csv", header=0, index_col=0)
    team : str
        name of D1 college basketball team
    skip_first_n : int (optional)
        Number of games to ignore before making records. Defaults to 10, that is,
        the 1st 10 games of each team are neglected. Starting with the 11th game,
        all prior stats are aggregated to make the features. The idea is that it takes
        some time, roughly skipFirstNGames, before a team's stats become representative
        of the team's actual ability. This is a quantity that can and should be
        further optimized.
    verbose : bool (optional)
        Whether or not to output debug and diagnostic information. Defaults to False.

    Returns
    -------
    df_agg : pandas.DataFrame
        data frame of processed/aggregated results such that each row containes
        the mean stats of team and opponent for a game given the previously
        played games, ignoring the first skipFirstNGames games. Returns None if
        given team did not play D1 basketball that season.
    """

    # First ensure team name is valid, catch errors, then normalize name if valid
    parsed_team = parser.name_normalizer(team, made_tourney=False,
                                         return_both=False, ignore_errors=False)

    # Figure out name of home team to help identify unique games
    df["home_name"] = df.apply(lambda x : __home_name(x["Location"], x["Team"], x["Opponent"]),
                               axis=1)

    # Add additional columns of interest
    df["team_at_home"] = pd.Series(df["Location"] == "H", index=df.index, dtype=int)
    df["neutral_site"] = pd.Series(df["Location"] == "N", index=df.index, dtype=int)
    df["total_score"] = df["TeamPoints"] + df["OpponentPoints"]
    df['Date'] =  pd.to_datetime(df['Date'], format="%Y-%m-%d")

    # Define features for each team
    featureCols = ['FGA', 'FG%', 'PF', '3P%', 'FT%', 'ORtg', 'DRtg', 'Pace',
                   'FTr', '3PAr', 'TS%', 'TRB%', 'AST%', 'STL%', 'BLK%',
                   'eFG%', 'TOV%', 'ORB%', 'FT/FGA', 'DRB%']

    # Make list for final dataframe columns
    team_cols = []
    opp_cols = []

    for col in feature_cols:
        # Save columns for team
        team_cols.append("team_" + col)

        # Save columns for opponent
        opp_cols.append("opp_" + col)

    # Add metadata, predictive features to finalCols
    final_cols = team_cols + opp_cols
    final_cols += ['team_name', 'opponent_name', 'team_at_home', 'neutral_site', "team_won",
                  "total_score", "Date", "Location", "home_name"]

    if verbose:
        print(parsed_team)

    # Get group corresponding to all gamelogs for team
    groups = df.groupby("Team")
    try:
        teamDf = groups.get_group(parsed_team)
    except KeyError as error:
        print(f"No data for {parsed_team}")
        return None

    # Loop over games, see if home team wins, skipping first 10 games (no previous statistics)
    games = []
    for ii in range(skip_first_n, len(team_tf)):
        # Figure out the opponent for the iith game
        opp = team_df.iloc[ii]["Opponent"]

        # Select all games team played prior to iith game
        # Just select feature columns treating tmp as team
        tmp = team_df[team_df["Date"] < team_df.iloc[ii]["Date"]].copy()

        # Now, loop through each game and for each opponent, do
        # a similar operation to get their aggregate statistics
        try:
            opp_df = groups.get_group(opp)
            opp_tmp = opp_df[opp_df["Date"] < team_df.iloc[ii]["Date"]].copy()
        except KeyError as error:
            print(f"No data for {opp}")
            continue

        # If no games have been played, cannot compute stats
        if opp_tmp.empty or tmp.empty:
            continue

        # Now aggregate both team and opponent's dataframes since team's
        # stats are in the home columns, and opp's are in away

        # Flatten tmp, oppTmp
        tmp = tmp[feature_cols].astype(float).aggregate(np.nanmean, axis=0)
        oppTmp = opp_tmp[feature_cols].astype(float).aggregate(np.nanmean, axis=0)

        # Team, then opponent aggregate stats
        game = list(tmp.values) + list(oppTmp.values)

        # Store team, opponent names
        game.append(parsed_team)
        game.append(opp)

        # Add indicator variable for if team is at home
        game.append(team_df.iloc[ii]["team_at_home"])

        # Add indicator variable for if game is played at a neutral site
        game.append(team_df.iloc[ii]["neutral_site"])

        # Add indicator variable for if team won
        game.append(team_df.iloc[ii]["team_won"])

        # Add float for total score
        game.append(team_df.iloc[ii]["total_score"])

        # Save date, location, names of winning and home teams
        game.append(team_df.iloc[ii]["Date"])
        game.append(team_df.iloc[ii]["Location"])

        # Save homeName to help identify games
        game.append(team_df.iloc[ii]["home_name"])

        # Save game
        games.append(game)

    # Make temporary dataframe from all games of team
    df_agg = pd.DataFrame.from_records(games, columns=final_cols)

    return df_agg