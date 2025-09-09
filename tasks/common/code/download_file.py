"""
Shih-Hsuan Hsu
July 15, 2025
Download a file from a URL using wget.
"""

import sys
import wget

if len(sys.argv) < 3:
    raise ValueError("Usage: python download_file.py <URL> <output_path>")

URL = sys.argv[1]
output_path = sys.argv[2]

# download the file
wget.download(URL, output_path)
