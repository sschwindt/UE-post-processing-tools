#config.py

import os
import subprocess

import matplotlib.pyplot as plt
import numpy as np
import re
import pandas as pd

from matplotlib.gridspec import GridSpec
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import MultipleLocator


# Global configuration variables for the project

# Path to the log file
_file_path = os.path.join(os.path.dirname(__file__), 'TechnicalFishPassOneSectionC150KShort.log')

def get_file_path():
    return _file_path

def set_file_path(path):
    global _file_path
    _file_path = path


# Limits for the x-Axis of the plots per Cross-section
xs_limits = {
    11: (-1.1, 1.3), 12: (-1.1, 1.3),  # XS 1.1 and 1.2
    21: (-2.5, 1.4), 22: (-2.5, 1.4),  # XS 2.1 and 2.2
    31: (-2.5, 1.4), 32: (-2.5, 1.4),  # XS 3.1 and 3.2
    41: (-1.4, 1.3), 42: (-1.4, 1.3)  # XS 4.1 and 4.2
}

# Max velocity on the colorbar
vmax = 1.6

# Radius of each point on the scatterplot
radius = 10

# Whether to limit the data to particles above a given velocity threshold
limit_Data = False

# Velocity threshold limit for filtering particle data
limit = 0.03

#global var 1 for criteria
var1 = 27
#global var 2 for criteria
var2 = 28
#global var 3 for criteria
var3 = 29
