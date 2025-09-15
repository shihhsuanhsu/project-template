"""
Shih-Hsuan Hsu
July 30, 2024
This file requires stata_config to be configured.
This file contains a function that runs a Stata do file.
"""

import sys
import os

# run the Stata configuration (stata_config.py)
with open(os.environ["STATA_CONFIG_PATH"], "r", encoding="utf-8") as f:
    exec(f.read())


def run_do_file(stata_file: str, stata_args: str) -> int:
    """
    This function is used to run a Stata do file.
    stata_file (str): the path to the Stata do file.
    stata_args (str): the arguments to pass to the Stata do file.
    """
    # initialize a Stata session
    stata = stata_init()
    # convert list of arguments to a string
    if isinstance(stata_args, list):
        stata_args = " ".join(stata_args)
    # run the do file
    try:
        stata.run(f"do {stata_file} {stata_args}")
    except SystemError as e:
        print("ERROR RUNNING DO FILE:", e)
        return 1
    # return success
    return 0


if __name__ == "__main__":
    # get the do file and arguments
    do_file = sys.argv[1]
    args = sys.argv[2:]
    # run the do file
    sys.exit(run_do_file(do_file, args))
