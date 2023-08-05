'''
Due to problems with click not accepting multi line
arguments for country, the space is replaced with 
and underscore and removed when filtering dataframes

'''

import os
import sys
import re

def replace_arg_space(country_str):
    return country_str.replace(' ', '_')

def replace_arg_score(country_str):
    return country_str.replace('_', ' ')