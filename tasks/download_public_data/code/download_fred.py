"""
Shih-Hsuan Hsu
Feb. 7, 2025
Download data from FRED
This scrip accepts two command line arguments:
1. series_to_download: the series to download from FRED
2. output_filename: the filename to save the data (without the extension)
"""

import sys
from fred_api import get_series

# verify the number of arguments
num_argv = len(sys.argv)
assert (
    num_argv == 3
), f"Expect 2 arguments (series to download then output filename) but got {num_argv}."

# parse command line arguments
series_to_download = sys.argv[1]
output_filename = sys.argv[2]

# download gdp data
res = get_series(series_to_download)
res.to_csv(f"../output/{output_filename}.csv", header=False)
