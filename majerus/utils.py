#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains routines for utility functions, values, key dates
over CBB seasons

@author: David P. Fleming, 2024
"""

# Imports
import numpy as np
from itertools import zip_longest
from datetime import datetime


__all__ = ["median_unequal_arr", "start_reg_20102011", "end_reg_20102011",
           "start_tourney_20102011", "end_tourney_20102011", "start_reg_20112012",
           "end_reg_20112012", "start_tourney_20112012", "end_tourney_20112012",
           "start_reg_20122013", "end_reg_20122013", "start_tourney_20122013",
           "end_tourney_20122013", "start_reg_20132014", "end_reg_20132014",
           "start_tourney_20132014", "end_tourney_20132014", "start_reg_20142015",
           "end_reg_20142015",  "start_tourney_20142015", "end_tourney_20142015",
           "start_reg_20152016", "end_reg_20152016",  "start_tourney_20152016",
           "end_tourney_20152016", "start_reg_20162017", "end_reg_20162017",
           "start_tourney_20162017",  "end_tourney_20162017", "start_reg_20172018",
           "end_reg_20172018", "start_tourney_20172018",  "end_tourney_20172018",
           "start_reg_20182019", "end_reg_20182019", "start_tourney_20182019",
           "end_tourney_20182019", "start_reg_20192020", "end_reg_20192020",
           "start_tourney_20192020", "end_tourney_20192020", "start_reg_20202021",
           "end_reg_20202021", "start_tourney_20202021", "end_tourney_20202021",
           "start_reg_20212022", "end_reg_20212022", "start_tourney_20212022",
           "end_tourney_20212022", "start_reg_20222023", "end_reg_20222023", 
           "start_tourney_20222023", "end_tourney_20222023", "start_reg_20232024", 
           "end_reg_20232024", "start_tourney_20232024", "end_tourney_20232024"]


################################################################################
#
# Define start and end dates for regular seasons, March Madness
#
################################################################################

# 2010-2011
start_reg_20102011 = datetime(2010, 11, 8)
end_reg_20102011 = datetime(2011, 3, 13)
start_tourney_20102011 = datetime(2011, 3, 15)
end_tourney_20102011 = datetime(2011, 4, 4)

# 2011-2012
start_reg_20112012 = datetime(2011, 11, 7)
end_reg_20112012 = datetime(2012, 3, 11)
start_tourney_20112012 = datetime(2012, 3, 13)
end_tourney_20112012 = datetime(2012, 4, 2)

# 2012-2013
start_reg_20122013 = datetime(2012, 11, 9)
end_reg_20122013 = datetime(2013, 3, 17)
start_tourney_20122013 = datetime(2013, 3, 19)
end_tourney_20122013 = datetime(2013, 4, 8)

# 2013-2014
start_reg_20132014 = datetime(2013, 11, 8)
end_reg_20132014 = datetime(2014, 3, 16)
start_tourney_20132014 = datetime(2014, 3, 18)
end_tourney_20132014 = datetime(2014, 4, 7)

# 2014-2015
start_reg_20142015 = datetime(2014, 11, 14)
end_reg_20142015 = datetime(2015, 3, 15)
start_tourney_20142015 = datetime(2015, 3, 17)
end_tourney_20142015 = datetime(2015, 4, 6)

# 2015-2016
start_reg_20152016 = datetime(2015, 11, 13)
end_reg_20152016 = datetime(2016, 3, 13)
start_tourney_20152016 = datetime(2016, 3, 15)
end_tourney_20152016 = datetime(2016, 4, 4)

# 2016-2017
start_reg_20162017 = datetime(2016, 11, 11)
end_reg_20162017 = datetime(2017, 3, 12)
start_tourney_20162017 = datetime(2017, 3, 14)
end_tourney_20162017 = datetime(2017, 4, 3)

# 2017-2018
start_reg_20172018 = datetime(2017, 11, 10)
end_reg_20172018 = datetime(2018, 3, 11)
start_tourney_20172018 = datetime(2018, 3, 13)
end_tourney_20172018 = datetime(2018, 4, 2)

# 2018-2019
start_reg_20182019 = datetime(2018, 11, 6)
end_reg_20182019 = datetime(2019, 3, 17)
start_tourney_20182019 = datetime(2019, 3, 19)
end_tourney_20182019 = datetime(2019, 4, 8)

# 2019-2020
start_reg_20192020 = datetime(2019, 11, 5)
end_reg_20192020 = datetime(2020, 3, 8)
start_tourney_20192020 = datetime(2020, 3, 17)
end_tourney_20192020 = datetime(2020, 4, 6)

# 2020-2021
start_reg_20202021 = datetime(2020, 11, 25)
end_reg_20202021 = datetime(2021, 3, 14)
start_tourney_20202021 = datetime(2021, 3, 18)
end_tourney_20202021 = datetime(2021, 4, 5)

# 2021-2022
start_reg_20212022 = datetime(2021, 11, 9)
end_reg_20212022 = datetime(2022, 3, 13)
start_tourney_20212022 = datetime(2022, 3, 15)
end_tourney_20212022 = datetime(2022, 4, 4)

# 2022-2023
start_reg_20222023 = datetime(2021, 11, 7)
end_reg_20222023 = datetime(2022, 3, 12)
start_tourney_20222023 = datetime(2022, 3, 14)
end_tourney_20222023 = datetime(2022, 4, 3)

# 2023-2024
start_reg_20232024 = datetime(2021, 11, 6)
end_reg_20232024 = datetime(2022, 3, 17)
start_tourney_20232024 = None
end_tourney_20232024 = None

################################################################################
#
# Math utility functions
#
################################################################################


def __median(x):
    """
    Compute the simple median of an array

    Parameters
    ----------
    x : iterable
        array

    Returns
    -------
    avg : float
        average
    """
    x = [i for i in x if i is not None]
    return np.nanmedian(x)
# end function


def median_unequal_arr(x):
    """
    Compute the median over rows of a list of lists/iterables where the inner
    most iterables are not necessarily the same length

    Parameters
    ----------
    x : iterable
        list of iterables

    Returns
    -------
    avg : iterable
        array of mean values whose length is equal to the length of the longest
        iterable in x
    """

    return list(map(__median, zip_longest(*x)))