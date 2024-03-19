#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Functions and mapping dictionaries for standardizing NCAA men's college
basketball team and conference names. I use the sportsreference CBB naming
standard as my standard.

These mappings have been validated for the 2010-2011 season onwards for both
kenpom and sportsference names.

@author: David P. Fleming, 2024

"""

import re
import unicodedata
import string
import numpy as np
from typing import Union


__all__ = ["name_normalizer", "conf_name_normalizer", "get_all_teams", "get_all_confs"]


### Dictionary of all NCAA men's basketball team names from 2010-2011-present ###
__team_names = {"abilene-christian" : "abilene-christian",
                "air-force" : "air-force",
                "akron" : "akron",
                "alabama-am" : "alabama-am",
                "alabama-birmingham" : "alabama-birmingham",
                "uab" : "alabama-birmingham",
                "alabama-state" : "alabama-state",
                "alabama" : "alabama",
                "albany-ny" : "albany-ny",
                "albany" : "albany-ny",
                "alcorn-state" : "alcorn-state",
                "american" : "american",
                "appalachian-state" : "appalachian-state",
                "arizona-state" : "arizona-state",
                "arizona" : "arizona",
                "little-rock" : "arkansas-little-rock",
                "arkansas-little-rock" : "arkansas-little-rock",
                "arkansas-pine-bluff" : "arkansas-pine-bluff",
                "arkansas-state" : "arkansas-state",
                "arkansas" : "arkansas",
                "army" : "army",
                "auburn" : "auburn",
                "austin-peay" : "austin-peay",
                "ball-state" : "ball-state",
                "baylor" : "baylor",
                "belmont" : "belmont",
                "bethune-cookman" : "bethune-cookman",
                "binghamton" : "binghamton",
                "boise-state" : "boise-state",
                "boston-college" : "boston-college",
                "boston-university" : "boston-university",
                "bowling-green-state" : "bowling-green-state",
                "bowling-green" : "bowling-green-state",
                "bradley" : "bradley",
                "byu" : "brigham-young",
                "brigham-young" : "brigham-young",
                "brown" : "brown",
                "bryant" : "bryant",
                "bucknell" : "bucknell",
                "buffalo" : "buffalo",
                "butler" : "butler",
                "california-baptist" : "california-baptist",
                "cal-baptist" : "california-baptist",
                "cal-poly" : "cal-poly",
                "cal-state-bakersfield" : "cal-state-bakersfield",
                "cal-st-bakersfield" : "cal-state-bakersfield",
                "cal-state-fullerton" : "cal-state-fullerton",
                "cal-st-fullerton" : "cal-state-fullerton",
                "cal-state-northridge" : "cal-state-northridge",
                "cal-st-northridge" : "cal-state-northridge",
                "cal-state-long-beach" : "long-beach-state",
                "california-baptist" : "california-baptist",
                "california-davis" : "california-davis",
                "california-irvine" : "california-irvine",
                "california-riverside" : "california-riverside",
                "california-santa-barbara" : "california-santa-barbara",
                "university-of-california" : "california",
                "california" : "california",
                "campbell" : "campbell",
                "canisius" : "canisius",
                "centenary" : "centenary-la",
                "centenary (la)" : "centenary-la",
                "centenary-la" : "centenary-la",
                "central-arkansas" : "central-arkansas",
                "central-connecticut-state" : "central-connecticut-state",
                "central-connecticut" : "central-connecticut-state",
                "central-florida" : "central-florida",
                "ucf" : "central-florida",
                "central-michigan" : "central-michigan",
                "charleston-southern" : "charleston-southern",
                "charlotte" : "charlotte",
                "chattanooga" : "chattanooga",
                "chicago-state" : "chicago-state",
                "cincinnati" : "cincinnati",
                "citadel" : "citadel",
                "the-citadel" : "citadel",
                "clemson" : "clemson",
                "cleveland-state" : "cleveland-state",
                "coastal-carolina" : "coastal-carolina",
                "colgate" : "colgate",
                "charleston" : "college-of-charleston",
                "college-of-charleston" : "college-of-charleston",
                "colorado-state" : "colorado-state",
                "colorado" : "colorado",
                "columbia" : "columbia",
                "connecticut" : "connecticut",
                "coppin-state" : "coppin-state",
                "cornell" : "cornell",
                "creighton" : "creighton",
                "dartmouth" : "dartmouth",
                "davidson" : "davidson",
                "dayton" : "dayton",
                "delaware-state" : "delaware-state",
                "delaware" : "delaware",
                "denver" : "denver",
                "depaul" : "depaul",
                "detroit-mercy" : "detroit-mercy",
                "detroit" : "detroit-mercy",
                "drake" : "drake",
                "drexel" : "drexel",
                "duke" : "duke",
                "duquesne" : "duquesne",
                "east-carolina" : "east-carolina",
                "east-tennessee-state" : "east-tennessee-state",
                "etsu" : "east-tennessee-state",
                "eastern-illinois" : "eastern-illinois",
                "eastern-kentucky" : "eastern-kentucky",
                "eastern-michigan" : "eastern-michigan",
                "eastern-washington" : "eastern-washington",
                "elon" : "elon",
                "evansville" : "evansville",
                "fairfield" : "fairfield",
                "fairleigh-dickinson" : "fairleigh-dickinson",
                "florida-am" : "florida-am",
                "florida-atlantic" : "florida-atlantic",
                "fau" : "florida-atlantic",
                "florida-gulf-coast" : "florida-gulf-coast",
                "fgcu" : "florida-gulf-coast",
                "florida-international" : "florida-international",
                "fiu" : "florida-international",
                "florida-state" : "florida-state",
                "florida" : "florida",
                "fordham" : "fordham",
                "fresno-state" : "fresno-state",
                "furman" : "furman",
                "gardner-webb" : "gardner-webb",
                "george-mason" : "george-mason",
                "george-washington" : "george-washington",
                "georgetown" : "georgetown",
                "georgia-southern" : "georgia-southern",
                "georgia-state" : "georgia-state",
                "georgia-tech" : "georgia-tech",
                "georgia" : "georgia",
                "gonzaga" : "gonzaga",
                "grambling-state" : "grambling",
                "grambling" : "grambling",
                "grand-canyon" : "grand-canyon",
                "green-bay" : "green-bay",
                "hampton" : "hampton",
                "hartford" : "hartford",
                "harvard" : "harvard",
                "hawaii" : "hawaii",
                "high-point" : "high-point",
                "hofstra" : "hofstra",
                "holy-cross" : "holy-cross",
                "houston-baptist" : "houston-baptist",
                "houston" : "houston",
                "howard" : "howard",
                "idaho-state" : "idaho-state",
                "idaho" : "idaho",
                "uic" : "illinois-chicago",
                "illinois-chicago" : "illinois-chicago",
                "illinois-state" : "illinois-state",
                "illinois" : "illinois",
                "incarnate-word" : "incarnate-word",
                "indiana-state" : "indiana-state",
                "indiana" : "indiana",
                "iona" : "iona",
                "iowa-state" : "iowa-state",
                "iowa" : "iowa",
                "purdue-fort-wayne" : "ipfw",
                "fort-wayne" : "ipfw",
                "ipfw" : "ipfw",
                "iupui" : "iupui",
                "jackson-state" : "jackson-state",
                "jacksonville-state" : "jacksonville-state",
                "jacksonville" : "jacksonville",
                "james-madison" : "james-madison",
                "kansas-state" : "kansas-state",
                "kansas" : "kansas",
                "kennesaw-state" : "kennesaw-state",
                "kent-state" : "kent-state",
                "kentucky" : "kentucky",
                "la-salle" : "la-salle",
                "lafayette" : "lafayette",
                "lamar" : "lamar",
                "lehigh" : "lehigh",
                "liberty" : "liberty",
                "lipscomb" : "lipscomb",
                "long-beach-state" : "long-beach-state",
                "long-island-university" : "long-island-university",
                "liu" : "long-island-university",
                "liu-brooklyn" : "long-island-university",
                "longwood" : "longwood",
                "louisiana" : "louisiana-lafayette",
                "louisiana-lafayette" : "louisiana-lafayette",
                "louisiana-monroe" : "louisiana-monroe",
                "louisiana-state" : "louisiana-state",
                "lsu" : "louisiana-state",
                "louisiana-tech" : "louisiana-tech",
                "louisville" : "louisville",
                "loyola-il" : "loyola-il",
                "loyola-chicago" : "loyola-il",
                "loyola-marymount" : "loyola-marymount",
                "loyola-md" : "loyola-md",
                "maine" : "maine",
                "manhattan" : "manhattan",
                "marist" : "marist",
                "marquette" : "marquette",
                "marshall" : "marshall",
                "maryland-baltimore-county" : "maryland-baltimore-county",
                "umbc" : "maryland-baltimore-county",
                "maryland-eastern-shore" : "maryland-eastern-shore",
                "maryland" : "maryland",
                "massachusetts-lowell" : "massachusetts-lowell",
                "umass-lowell" : "massachusetts-lowell",
                "massachusetts" : "massachusetts",
                "umass" : "massachusetts",
                "mcneese-state" : "mcneese-state",
                "memphis" : "memphis",
                "mercer" : "mercer",
                "miami-fl" : "miami-fl",
                "miami-oh" : "miami-oh",
                "michigan-state" : "michigan-state",
                "michigan" : "michigan",
                "middle-tennessee" : "middle-tennessee",
                "milwaukee" : "milwaukee",
                "minnesota" : "minnesota",
                "mississippi-state" : "mississippi-state",
                "mississippi-valley-state" : "mississippi-valley-state",
                "mississippi" : "mississippi",
                "ole-miss" : "mississippi",
                "missouri-kansas-city" : "missouri-kansas-city",
                "umkc" : "missouri-kansas-city",
                "missouri-state" : "missouri-state",
                "missouri" : "missouri",
                "monmouth" : "monmouth",
                "montana-state" : "montana-state",
                "montana" : "montana",
                "morehead-state" : "morehead-state",
                "morgan-state" : "morgan-state",
                "mount-st-marys" : "mount-st-marys",
                "murray-state" : "murray-state",
                "navy" : "navy",
                "omaha" : "nebraska-omaha",
                "nebraska-omaha" : "nebraska-omaha",
                "nebraska" : "nebraska",
                "nevada-las-vegas" : "nevada-las-vegas",
                "unlv" : "nevada-las-vegas",
                "nevada" : "nevada",
                "new-hampshire" : "new-hampshire",
                "new-mexico-state" : "new-mexico-state",
                "new-mexico" : "new-mexico",
                "new-orleans" : "new-orleans",
                "niagara" : "niagara",
                "nicholls-state" : "nicholls-state",
                "njit" : "njit",
                "norfolk-state" : "norfolk-state",
                "north-alabama" : "north-alabama",
                "unc-asheville" : "north-carolina-asheville",
                "north-carolina-asheville" : "north-carolina-asheville",
                "north-carolina-at" : "north-carolina-at",
                "north-carolina-central" : "north-carolina-central",
                "north-carolina-greensboro" : "north-carolina-greensboro",
                "unc-greensboro" : "north-carolina-greensboro",
                "north-carolina-state" : "north-carolina-state",
                "n.c.-state" : "north-carolina-state",
                "nc-state" : "north-carolina-state",
                "north-carolina-wilmington" : "north-carolina-wilmington",
                "unc-wilmington" : "north-carolina-wilmington",
                "north-carolina" : "north-carolina",
                "unc" : "north-carolina",
                "north-dakota-state" : "north-dakota-state",
                "north-dakota" : "north-dakota",
                "north-florida" : "north-florida",
                "north-texas" : "north-texas",
                "northeastern" : "northeastern",
                "northern-arizona" : "northern-arizona",
                "northern-colorado" : "northern-colorado",
                "northern-illinois" : "northern-illinois",
                "northern-iowa" : "northern-iowa",
                "northern-kentucky" : "northern-kentucky",
                "northwestern-state" : "northwestern-state",
                "northwestern" : "northwestern",
                "notre-dame" : "notre-dame",
                "oakland" : "oakland",
                "ohio-state" : "ohio-state",
                "ohio" : "ohio",
                "oklahoma-state" : "oklahoma-state",
                "oklahoma" : "oklahoma",
                "old-dominion" : "old-dominion",
                "oral-roberts" : "oral-roberts",
                "oregon-state" : "oregon-state",
                "oregon" : "oregon",
                "pacific" : "pacific",
                "penn-state" : "penn-state",
                "pennsylvania" : "pennsylvania",
                "penn" : "pennsylvania",
                "pepperdine" : "pepperdine",
                "pittsburgh" : "pittsburgh",
                "pitt" : "pittsburgh",
                "portland-state" : "portland-state",
                "portland" : "portland",
                "prairie-view" : "prairie-view",
                "prairie-view-am" : "prairie-view",
                "presbyterian" : "presbyterian",
                "princeton" : "princeton",
                "providence" : "providence",
                "purdue" : "purdue",
                "quinnipiac" : "quinnipiac",
                "radford" : "radford",
                "rhode-island" : "rhode-island",
                "rice" : "rice",
                "richmond" : "richmond",
                "rider" : "rider",
                "robert-morris" : "robert-morris",
                "rutgers" : "rutgers",
                "sacramento-state" : "sacramento-state",
                "sacred-heart" : "sacred-heart",
                "saint-francis-pa" : "saint-francis-pa",
                "saint-josephs" : "saint-josephs",
                "st-josephs" : "saint-josephs",
                "saint-louis" : "saint-louis",
                "saint-marys-ca" : "saint-marys-ca",
                "saint-marys" : "saint-marys-ca",
                "saint-peters" : "saint-peters",
                "sam-houston-state" : "sam-houston-state",
                "samford" : "samford",
                "san-diego-state" : "san-diego-state",
                "san-diego" : "san-diego",
                "san-francisco" : "san-francisco",
                "san-jose-state" : "san-jose-state",
                "santa-clara" : "santa-clara",
                "savannah-state" : "savannah-state",
                "seattle" : "seattle",
                "seton-hall" : "seton-hall",
                "siena" : "siena",
                "south-alabama" : "south-alabama",
                "south-carolina-state" : "south-carolina-state",
                "south-carolina-upstate" : "south-carolina-upstate",
                "usc-upstate" : "south-carolina-upstate",
                "south-carolina" : "south-carolina",
                "south-dakota-state" : "south-dakota-state",
                "south-dakota" : "south-dakota",
                "south-florida" : "south-florida",
                "southeast-missouri-state" : "southeast-missouri-state",
                "southeastern-louisiana" : "southeastern-louisiana",
                "southern-california" : "southern-california",
                "usc" : "southern-california",
                "siu-edwardsville" : "southern-illinois-edwardsville",
                "southern-illinois-edwardsville" : "southern-illinois-edwardsville",
                "southern-illinois" : "southern-illinois",
                "smu" : "southern-methodist",
                "southern-methodist" : "southern-methodist",
                "southern-miss" : "southern-mississippi",
                "southern-mississippi" : "southern-mississippi",
                "southern-utah" : "southern-utah",
                "southern" : "southern",
                "saint-bonaventure" : "st-bonaventure",
                "st-bonaventure" : "st-bonaventure",
                "st-francis-ny" : "st-francis-ny",
                "saint-francis-ny" : "st-francis-ny",
                "saint-johns" : "st-johns-ny",
                "st-johns-ny" : "st-johns-ny",
                "saint-johns-ny" : "st-johns-ny",
                "stanford" : "stanford",
                "stephen-f-austin" : "stephen-f-austin",
                "stetson" : "stetson",
                "stony-brook" : "stony-brook",
                "syracuse" : "syracuse",
                "temple" : "temple",
                "tennessee-martin" : "tennessee-martin",
                "tennessee-state" : "tennessee-state",
                "tennessee-tech" : "tennessee-tech",
                "tennessee" : "tennessee",
                "texas-am-corpus-christi" : "texas-am-corpus-christi",
                "texas-am-corpus-chris" : "texas-am-corpus-christi",
                "texas-am" : "texas-am",
                "ut-arlington" : "texas-arlington",
                "texas-arlington" : "texas-arlington",
                "tcu" : "texas-christian",
                "texas-christian" : "texas-christian",
                "texas-el-paso" : "texas-el-paso",
                "utep" : "texas-el-paso",
                "texas-rio-grande-valley" : "texas-pan-american",
                "ut-rio-grande-valley" : "texas-pan-american",
                "texas-pan-american" : "texas-pan-american",
                "texas-san-antonio" : "texas-san-antonio",
                "utsa" : "texas-san-antonio",
                "texas-southern" : "texas-southern",
                "texas-state" : "texas-state",
                "texas-tech" : "texas-tech",
                "texas" : "texas",
                "toledo" : "toledo",
                "towson" : "towson",
                "troy" : "troy",
                "tulane" : "tulane",
                "tulsa" : "tulsa",
                "ucla" : "ucla",
                "utah-state" : "utah-state",
                "utah-valley" : "utah-valley",
                "utah" : "utah",
                "valparaiso" : "valparaiso",
                "vanderbilt" : "vanderbilt",
                "vermont" : "vermont",
                "villanova" : "villanova",
                "virginia-commonwealth" : "virginia-commonwealth",
                "vcu" : "virginia-commonwealth",
                "vmi" : "virginia-military-institute",
                "virginia-military-institute" : "virginia-military-institute",
                "virginia-tech" : "virginia-tech",
                "virginia" : "virginia",
                "wagner" : "wagner",
                "wake-forest" : "wake-forest",
                "washington-state" : "washington-state",
                "washington" : "washington",
                "weber-state" : "weber-state",
                "west-virginia" : "west-virginia",
                "western-carolina" : "western-carolina",
                "western-illinois" : "western-illinois",
                "western-kentucky" : "western-kentucky",
                "western-michigan" : "western-michigan",
                "wichita-state" : "wichita-state",
                "william-mary" : "william-mary",
                "winthrop" : "winthrop",
                "wisconsin" : "wisconsin",
                "wofford" : "wofford",
                "wright-state" : "wright-state",
                "wyoming" : "wyoming",
                "xavier" : "xavier",
                "yale" : "yale",
                "youngstown-state" : "youngstown-state"}


### Dictionary for conference names valid for 2010-2011 season to present ###
__conf_name = {"mid-eastern athletic conference" : "meac",
              "meac" : "meac",
              "mid-american conference" : "mac",
              "mac" : "mac",
              "mountain west conference" : "mwc",
              "mwc" : "mwc",
              "atlantic 10 conference" : "atlantic-10",
              "a-10" : "atlantic-10",
              "a10" : "atlantic-10",
              "atlantic-10" : "atlantic-10",
              "missouri valley conference" : "mvc",
              "mvc" : "mvc",
              "southern conference" : "southern",
              "sc" : "southern",
              "southern" : "southern",
              "ivy group" : "ivy",
              "ivy" : "ivy",
              "sun belt conference" : "sun-belt",
              "sun belt" : "sun-belt",
              "sb" : "sun-belt",
              "sun-belt" : "sun-belt",
              "conference usa" : "cusa",
              "cusa" : "cusa",
              "western athletic conference" : "wac",
              "wac" : "wac",
              "horizon league" : "horizon",
              "horizon" : "horizon",
              "horz" : "horizon",
              "colonial athletic association" : "colonial",
              "caa" : "colonial",
              "colonial" : "colonial",
              "big west conference" : "big-west",
              "bw" : "big-west",
              "big west" : "big-west",
              "big-west" : "big-west",
              "atlantic sun conference" : "atlantic-sun",
              "a-sun" : "atlantic-sun",
              "asun" : "atlantic-sun",
              "atlantic-sun" : "atlantic-sun",
              "summit league" : "summit",
              "summit" : "summit",
              "sum" : "summit",
              "patriot league" : "patriot",
              "patriot" : "patriot",
              "pat" : "patriot",
              "ohio valley conference" : "ovc",
              "ovc" : "ovc",
              "big south conference" : "big-south",
              "big south" : "big-south",
              "big-south" : "big-south",
              "bsth" : "big-south",
              "america east conference" : "america-east",
              "aec" : "america-east",
              "ae" : "america-east",
              "america-east" : "america-east",
              "big sky conference" : "big-sky",
              "big sky" : "big-sky",
              "big-sky" : "big-sky",
              "bsky" : "big-sky",
              "metro atlantic athletic conference" : "maac",
              "maac" : "maac",
              "southland conference" : "southland",
              "southland" : "southland",
              "slnd" : "southland",
              "northeast conference" : "northeast",
              "nec" : "northeast",
              "northeast" : "northeast",
              "southwest athletic conference" : "swac",
              "swac" : "swac",
              "big ten conference" : "big-ten",
              "big ten" : "big-ten",
              "b10" : "big-ten",
              "big-ten" : "big-ten",
              "big 12 conference" : "big-12",
              "b12" : "big-12",
              "big 12" : "big-12",
              "big-12" : "big-12",
              "atlantic coast conference" : "acc",
              "acc" : "acc",
              "southeastern conference" : "sec",
              "sec" : "sec",
              "big east conference" : "big-east",
              "be" : "big-east",
              "big east" : "big-east",
              "big-east" : "big-east",
              "pacific-12 conference" : "pac-12",
              "pac 12" : "pac-12",
              "p12" : "pac-12",
              "pac-12" : "pac-12",
              "pacific-10 conference" : "pac-10",
              "pac 10" : "pac-10",
              "pac-10" : "pac-10",
              "p10" : "pac-10",
              "american athletic conference" : "aac",
              "amer" : "aac",
              "aac" : "aac",
              "west coast conference" : "wcc",
              "wcc" : "wcc",
              "great west conference" : "great-west",
              "great-west" : "great-west",
              "gwc" : "great-west",
              "ind" : "ind"}


def name_normalizer(name : str, made_tourney : bool=False,
                    return_both : bool=False, ignore_errors : bool=False) -> Union[str, bool]:
    """
    Convert MCBB to a standardized name for using with scraping and interacting
    with data from https://www.sports-reference.com/cbb. Since NCAA is present
    in a team's name string if they made the tourney, this function can also
    be used to the parsed name, if they made the tourney, or both.

    Parameters
    ----------
    name : str
        CBB team name, like Duke
    made_tourney : bool (optional)
        Whether or not team made the NCCA tourney. Defaults to False. If True,
        returns 1 if team made the tourney, 0 if not, after parsed_name
    return_both : bool (optional)
        Whether or not to return both the parsed_name and whether or not that
        team made the tourney. Defaults to False.
    ignore_errors : bool (optional)
        Whether or not to ignore name errors and replace unknown teams with NaN.
        Defaults to False so invalid names will throw a KeyError

    Returns
    -------
    parsed_name : str (optional)
        cleaned name
    made_tourney : bool (optional)
    """

    # Clean up team name
    parsed_team = unicodedata.normalize("NFKD", str(name)).lower().strip()

    # Special case: "st." - replace in "saint" or "state" depending on context
    if "st." in parsed_team:
        tmp = parsed_team.split()
        if tmp[0] == "st.":
            parsed_team = parsed_team.replace("st.", "saint")
        elif tmp[-1] == "st.":
            parsed_team = parsed_team.replace("st.", "state")
        # Weird cases where st in middle can be state or saint
        else:
            pass

    # Remove junk characters not present in team url
    for char in ["&", "(", ")", "'", "."]:
        parsed_team = parsed_team.replace(char, "")

    # Special case: - between name and location
    parsed_team = parsed_team.replace("-", " ")

    # Tokenize
    parsed_team = parsed_team.split(" ")

    # Convert UC -> California since there's a lot of UCs in D1
    parsed_team = ["california" if wd == "uc" else wd for wd in parsed_team]

    # Remove blank characters
    parsed_team = [el for el in parsed_team if el]

    # Did they make the tourney?
    if "ncaa" in parsed_team:
        b_march_madness = 1
        parsed_team = "-".join(parsed_team[:-1])
    else:
        b_march_madness = 0
        parsed_team = "-".join(parsed_team)

    # Now correctly map name to url form and ensure it's valid
    try:
        parsed_team = __team_names[parsed_team]
    except KeyError:
        # Ignore error -> set to NaN
        if ignore_errors:
            parsed_team = np.nan
        else:
            err_msg = f"Incorrect team name: {parsed_team}. See this function's docs for valid names."
            raise KeyError(err_msg)

    # Return correct info
    if return_both:
        return parsed_team, b_march_madness
    else:
        if not made_tourney:
            return parsed_team
        else:
            return b_march_madness


def conf_name_normalizer(name : str,
                         ignore_errors : bool=False) -> str:
    """
    Convert men's college basketball conference name to a standardized name.
    See the following link for a list of valid conferences:
    https://www.sports-reference.com/cbb/conferences/.

    Example: Athletic Coast Conference -> acc

    Parameters
    ----------
    name : str
        Conference team name, like Athletic Coast Conference, or acc
    ignore_errors : bool (optional)
        Whether or not to ignore name errors and replace unknown teams with NaN.
        Defaults to False so invalid names will throw a KeyError

    Returns
    -------
    parsed_conf : str (optional)
        cleaned name
    """

    # Clean up team name
    parsed_conf = unicodedata.normalize("NFKD", name).lower().strip()

    # If (east) or (west) is after conference name, remove it
    if "(east)" in parsed_conf or "(west)" in parsed_conf or "(south)" in parsed_conf or "(north)" in parsed_conf:
        parsed_conf = "-".join(parsed_conf.split(" ")[:-1])

    # Now correctly map name to url form and ensure it's valid
    try:
        parsed_conf = __conf_name[parsed_conf]
    except KeyError:
        # Ignore error -> set to NaN
        if ignore_errors:
            parsed_conf = np.nan
        else:
            err_msg = "Incorrect conference name: {parsed_conf}. See this function's docs for valid names."
            raise KeyError(err_msg)

    return parsed_conf


def get_all_teams() -> list:
    """
    Return a parsed, ordered list of all unique NCAAB team names.

    Parameters
    ----------

    Returns
    -------
        all_teams : list
            List of team names
    """

    return list(np.sort(list(set(__team_names.values()))))


def get_all_confs() -> list:
    """
    Return a parsed, ordered list of all unique NCAAB conference names.

    Parameters
    ----------

    Returns
    -------
        all_confs : list
            List of conference names
    """

    return list(np.sort(list(set(__conf_name.values()))))