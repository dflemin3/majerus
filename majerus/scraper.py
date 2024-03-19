#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: David P. Fleming, 2024

This file contains routines for downloading, parsing, and restructuring
data from men's college basketball reference: https://www.sports-reference.com/cbb/
"""

# Imports
import requests
import pandas as pd
import numpy as np
import unicodedata
import string
import os
import re
from datetime import datetime
from . import parser
import numpy as np


__all__ = ["scrape_team_game_logs_basic", "scrape_team_game_logs_adv",
           "scrape_team_game_logs"]


def scrape_team_game_logs_basic(team : str, season : int, verbose : bool=False,
                                normalize_names : bool=True, headers : dict=None,
                                proxies : dict=None) -> pd.DataFrame:
    """
    Scrape all basic gamelogs for the (season-1 - season) season, e.g.
    2014-2015 season, from https://www.sports-reference.com/cbb/ for team. URL
    is something like the following given a team, season:
    https://www.sports-reference.com/cbb/schools/team/season-gamelogs.html

    Parameters
    ----------
    team : str
        team name
    season : int
        season year where season is the (season-1, season) season. For example,
        if season = 2015, data is scraped for the 2014-2015 season.
    verbose : bool (optional)
        Whether or not to output diagnostics. Defaults to False.
    normalizeNames : bool (optional)
        Whether or not to normalize names. Defaults to True.
    headers : dict (optional)
        dictionary of headers for request
    proxies : dict (optional)
        dictionary of proxies for request

    Returns
    -------
    df : pd.DataFrame
        dataframe containing all basic gamelogs for team in the specified season.
        Returns None if request fails 
    """

    # Validate season - only a small allowable range that I've validated
    if season > 2024:
        raise IOError("ERROR: Can't scrape data from the future!")
    if season < 2011:
        raise IOError("ERROR: Haven't validated scraping for seasons < 2010-2011!")

    # Parse team name
    parsed_team = parser.name_normalizer(team, ignore_errors=False)

    if verbose:
        print(f"Scraping all basic gamelogs for {parsed_team} for the {season-1}-{season} season.")

    # Initialize gamelog
    url = f"http://www.sports-reference.com/cbb/schools/{parsed_team}/{season}-gamelogs.html"

    # Scrape using requests
    try: 
        r = requests.get(url, proxies=proxies, headers=headers)
        if r.status_code < 400:
            # Parse response data using pandas after successful request
            df = pd.read_html(r.content, parse_dates=True, attrs={'id': 'sgl-basic_NCAAM'},
                                header=1, index_col=1)[0]
        else: 
            print(f"Failed request with status code {r.status_code}") 
            return None
    except Exception as e: 
        print(f"Failed request with exception {e}")
        return None 

    # Remove NaN and junk indices that correspond to delimiter rows
    df = df[df.index.notnull()].copy()
    df = df[df.index != "Date"].copy()

    # Explicitely make date index a datetime
    df.index = pd.to_datetime(df.index, format="%Y-%m-%d")

    # Rename, drop junk columns
    df.drop(columns=["Unnamed: 23", "G"], inplace=True)
    df["location"] = df["Unnamed: 2"].copy()
    df.drop(columns=["Unnamed: 2"], inplace=True)

    # Parse location to be H, A, or N for home, away, or neutral
    df["location"] = df["location"].fillna("H")
    df["location"] = df["location"].apply(lambda x : "A" if x == "@" else x)

    # Set team, opponent names and drop NaNs (aka non-D1 teams)
    if normalize_names:
        df["team"] = pd.Series([parsed_team for _ in range(len(df))], index=df.index)
        df["Opp"] = df["Opp"].apply(parser.name_normalizer, **{"ignore_errors" : True})
    else:
        df["team"] = pd.Series([team for _ in range(len(df))], index=df.index)
    df.dropna(subset=["Opp"], axis=0, inplace=True)

    # Change W/L column to be 0/1 indicator variable for if Team won
    df["team_won"] = df["W/L"].copy()
    df.drop(columns=["W/L"], axis=0, inplace=True)

    # Correct data type of the data frame
    dtypes = {'Opp' : str, 'team_won' : str, 'Tm' : np.float64, 'Opp.1' : np.float64, 'FG' : np.float64,
            'FGA' : np.float64, 'FG%' : np.float64, '3P' : np.float64, '3PA' : np.float64,
            '3P%' : np.float64, 'FT' : np.float64, 'FTA' : np.float64, 'FT%' : np.float64, 'ORB' : np.float64,
            'TRB' : np.float64, 'AST' : np.float64, 'STL' : np.float64, 'BLK' : np.float64, 'TOV' : np.float64,
            'PF' : np.float64, 'FG.1' : np.float64, 'FGA.1' : np.float64, 'FG%.1' : np.float64, '3P.1' : np.float64,
            '3PA.1' : np.float64, '3P%.1' : np.float64, 'FT.1' : np.float64, 'FTA.1' : np.float64, 'FT%.1' : np.float64,
            'ORB.1' : np.float64, 'TRB.1' : np.float64, 'AST.1' : np.float64, 'STL.1' : np.float64, 'BLK.1' : np.float64,
            'TOV.1' : np.float64, 'PF.1' : np.float64, "location" : str, "team" : str}
    df = df.astype(dtypes)

    # Disregard OT results, only whether Team won or lost. Convert W/L to bool
    df["team_won"] = df["team_won"].apply(lambda x : str(x).split()[0])
    df["team_won"] = df["team_won"].apply(lambda x : 1 if x == "W" else 0)

    # Map column names for opponent to be more intuitive
    col_map_dict = {'Opp' : "opponent", 'Tm' : "team_points",
                    'Opp.1' : "opponent_points", 'FG.1' : "opp_fg", 'FGA.1' : "opp_fga",
                    'FG%.1' : "opp_fg%", '3P.1' : "opp_3p", '3PA.1' : "opp_3pa",
                    '3P%.1' : "opp_3p%", 'FT.1' : "opp_ft", 'FTA.1' : "opp_fta",
                    'FT%.1' : "opp_ft%", 'ORB.1' : "opp_orb", 'TRB.1' : "opp_trb",
                    'AST.1' : "opp_ast", 'STL.1' : "opp_stl", 'BLK.1' : "opp_blk",
                    'TOV.1' : "opp_tov", 'PF.1' : "opp_pf"}
    df.rename(columns=col_map_dict, inplace=True)

    return df


def scrape_team_game_logs_adv(team : str, season : int, verbose : bool=False, 
                              normalize_names : bool=True, headers : dict=None,
                              proxies : dict=None) -> pd.DataFrame:
    """
    Scrape all advanced gamelogs for the (season-1 - season) season, e.g.
    2014-2015 season, from https://www.sports-reference.com/cbb/ for team. URL
    is something like the following, given a team and season:
    https://www.sports-reference.com/cbb/schools/team/season-gamelogs-advanced.html

    Parameters
    ----------
    team : str
        team name
    season : int
        season year where season is the (season-1, season) season. For example,
        if season = 2015, data is scraped for the 2014-2015 season.
    verbose : bool (optional)
        Whether or not to output diagnostics. Defaults to False.
    normalizeNames : bool (optional)
        Whether or not to normalize names. Defaults to True.
    headers : dict (optional)
        dictionary of headers for request
    proxies : dict (optional)
        dictionary of proxies for request

    Returns
    -------
    df : pd.DataFrame
        dataframe containing all adv gamelogs for team in the specified season
    """

    # Validate season - only a small allowable range that I've validated
    if season > 2024:
        raise IOError("ERROR: Can't scrape data from the future!")
    if season < 2011:
        raise IOError("ERROR: Haven't validated scraping for seasons < 2010-2011!")

    # Parse team name
    parsed_team = parser.name_normalizer(team, ignore_errors=False)

    if verbose:
        print(f"Scraping all advanced gamelogs for {parsed_team} for the {season-1}-{season}.")

    # Initialize gamelog
    url = f"http://www.sports-reference.com/cbb/schools/{parsed_team}/{season}-gamelogs-advanced.html"

    # Scrape the data using pandas
    df = pd.read_html(url, parse_dates=True, attrs = {'id': 'sgl-advanced'},
                    header=1, index_col=1)[0]

    # Remove NaN and junk indices that correspond to delimiter rows
    df = df[df.index.notnull()].copy()
    df = df[df.index != "Date"].copy()

    # Explicitely make date index a datetime
    df.index = pd.to_datetime(df.index, format="%Y-%m-%d")

    # Rename, drop junk columns
    df.drop(columns=["Unnamed: 17", "Unnamed: 22", "G"], inplace=True)
    df["location"] = df["Unnamed: 2"].copy()
    df.drop(columns=["Unnamed: 2"], inplace=True)

    # Parse location to be H, A, or N for home, away, or neutral
    df["location"] = df["location"].fillna("H")
    df["location"] = df["location"].apply(lambda x : "A" if x == "@" else x)

    # Set team, opponent names and drop NaNs (aka non-D1 teams)
    if normalize_names:
        df["team"] = pd.Series([parsed_team for _ in range(len(df))], index=df.index)
        df["Opp"] = df["Opp"].apply(parser.name_normalizer, **{"ignore_errors" : True})
    else:
        df["team"] = pd.Series([team for _ in range(len(df))], index=df.index)
    df.dropna(subset=["Opp"], axis=0, inplace=True)

    # Change W/L column to be 0/1 indicator variable for if Team won
    df["team_won"] = df["W/L"].copy()
    df.drop(columns=["W/L"], axis=0, inplace=True)

    # Correct data type of the data frame
    dtypes = {'Opp' : str, 'Tm' : np.float64, 'Opp.1' : np.float64, 'ORtg' : np.float64,
            'DRtg' : np.float64, 'Pace' : np.float64, 'FTr' : np.float64, '3PAr' : np.float64,
            'TS%' : np.float64, 'TRB%' : np.float64, 'AST%' : np.float64, 'STL%' : np.float64, 'BLK%' : np.float64,
            'eFG%' : np.float64, 'TOV%' : np.float64, 'ORB%' : np.float64, 'FT/FGA' : np.float64, 'eFG%.1' : np.float64,
            'TOV%.1' : np.float64, 'DRB%' : np.float64, 'FT/FGA.1' : np.float64, "location" : str, "team" : str,
            'team_won' : str}
    df = df.astype(dtypes)

    # Disregard OT results, only whether Team won or lost. Convert W/L to bool
    df["team_won"] = df["team_won"].apply(lambda x : str(x).split()[0])
    df["team_won"] = df["team_won"].apply(lambda x : 1 if x == "W" else 0)

    col_map_dict = {'Opp' : "opponent", 'Tm' : "team_points",
                    'Opp.1' : "opponent_points", 'eFG%.1' : "opponent_efg%",
                    'TOV%.1' : "opponent_tov%", 'FT/FGA.1' : "opponent_ft_per_fga"}
    df.rename(columns=col_map_dict, inplace=True)

    return df


def scrape_team_game_logs(team : str, season : int, verbose : bool=False,
                          normalize_names : bool=True, headers : dict=None,
                          proxies : dict=None) -> pd.DataFrame:
    """
    Scrape all gamelogs for the (season-1 - season) season, e.g.
    2014-2015 season, from https://www.sports-reference.com/cbb/ for team. This
    function scrapes both basic and advanced game logs and joins them ensuring
    that there are no duplicated columns.

    Parameters
    ----------
    team : str
        team name
    season : int
        season year where season is the (season-1, season) season. For example,
        if season = 2015, data is scraped for the 2014-2015 season.
    verbose : bool (optional)
        Whether or not to output diagnostics. Defaults to False.
    normalize_names : bool (optional)
        Whether or not to normalize names. Defaults to True.
    headers : dict (optional)
        dictionary of headers for request
    proxies : dict (optional)
        dictionary of proxies for request

    Returns
    -------
    df : pd.DataFrame
        dataframe containing all gamelogs for team in the specified season
    """

    # Scrape basic gamelogs
    df_basic = scrape_team_game_logs_basic(team, season, verbose=verbose,
                                           normalize_names=normalize_names)
    # Scrape advanced gamelogs
    df_adv = scrape_team_game_logs_adv(team, season, verbose=verbose,
                                       normalize_names=normalize_names)

    # Join, discard duplicated columns
    df = df_basic.join(df_adv, how="left", rsuffix="_dup")

    drop_cols = [x for x in df if x.endswith('_dup')]
    df.drop(drop_cols, axis=1, inplace=True)

    return df


