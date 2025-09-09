"""
This is the setup file to use pystata.
Please follow **Method 2** in
    https://www.stata.com/python/pystata17/install.html
    to install stata_setup, which is needed for pystata.
If you'd like to use pystata, please link this file to the code directory
    for the task, then put `from stata_config import stata_init` in the
    top the python script using pystata.
Use `stata_init()` to initialize a Stata session.
"""

import sys
import platform

# handles paths for Stata utilities in different platforms
platform_name = platform.platform().lower()
path_added = False
if "linux" in platform_name:
    sys.path.append("/usr/local/stata/utilities")
    path_added = True
if "macos" in platform_name:
    sys.path.append("/Applications/Stata/utilities")
    path_added = True
# handle paths for a specific machine
if platform.uname().node == "OVRW-ECON-P04":
    sys.path.append("C:\\Program Files\\Stata18\\utilities")
    path_added = True
assert path_added, (
    "Stata utilities path not found."
    "Please check your Stata installation add the path to this file."
)

# IMPORTANT: DO NOT MODIFY BELOW THIS LINE
import pystata  # pylint: disable=import-error disable=wrong-import-position

pystata.config.init("mp", splash=False)
from pystata import (
    stata,
)  # pylint: disable=import-error disable=wrong-import-position


def stata_init():
    """
    Initialize a Stata session and print 'Stata session initialized.'
        in the stdout.
    Since stata_setup.config() quits current execution
        when there are errors (e.g. expired license),
        the extra print statement makes debugging easier.
    """
    session = stata
    print("Stata session initialized.")
    return session
