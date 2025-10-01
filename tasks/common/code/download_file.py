"""
Shih-Hsuan Hsu
October 1, 2025
Download a file from the given URL to the specified location.
"""

import sys
from urllib.request import urlretrieve

# check number of arguments
assert len(sys.argv) == 3, "Usage: python download_file.py <URL> <target_path>"

# download the file
urlretrieve(sys.argv[1], sys.argv[2])
