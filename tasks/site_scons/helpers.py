"""
Shih-Hsuan Hsu
July 19, 2025
Helper functions for SCons environment.
"""

import os
import hashlib
from pathlib import Path
from datetime import datetime
from custom_warnings import space_in_arg_warning


def convert_scons_path(env, path_str):
    """
    Convert SCons '#' syntax to actual project directory path.
    Args:
        env: SCons environment object
        path_str (str): Path string that may contain '#' prefix
    Returns:
        str: Absolute path with '#' converted to project root
    """
    if path_str.startswith("#"):
        # Remove the '#' and get the project root directory
        project_root = env.Dir("#").abspath
        # Handle both '#/path' and '#path' formats
        relative_path = path_str[1:].lstrip("/")
        if relative_path:
            return os.path.join(project_root, relative_path)
        else:
            return project_root
    return path_str


def create_log_file_path(env, source, ext):
    """
    This function creates a log file path based on the source file and extension.
    """
    log_file = env.get("LOG_FILE", "")
    log_dir = env.get("LOG_DIR", "logs")
    if log_file == "":
        # no log file given, use the source file name
        log_file = (
            str(source[0]).replace(f".{ext}", ".log").replace("code", log_dir)
        )
    else:
        # use absolute path to avoid path issues
        if not os.path.isabs(log_file):
            log_file = os.path.join(env.Dir(".").srcnode().abspath, log_file)
        # only modify $LOG_FILE if it was given to avoid modifying env
        env["LOG_FILE"] = log_file
    return log_file


def parse_args(env, wrap_in_quotes=False):
    """
    This function is used to parse the command line arguments.
    It sets the `ARGS` variable in the environment.
    """
    # retrieve the arguments from the environment
    args = env.get("ARGS", [])
    # if args is not a list, convert it to a list
    if not isinstance(args, list):
        args = [args]
    # loop through each argument and escape spaces
    parsed_args = []
    for arg in args:
        if not isinstance(arg, str):
            # convert non-string arguments to string
            arg = str(arg)
        if " " in arg and wrap_in_quotes:
            space_in_arg_warning(arg, parse_arg=True)
            arg = f'"{arg}"'
        parsed_args.append(arg)
    return parsed_args


def calculate_md5(filepath: str | Path) -> dict[str, str]:
    """
    Calculate MD5 hash of a file.
    Args:
        filepath (str or Path): Path to the file.
    Returns:
        dict[str, str]: Dictionary containing the file path, MD5 hash, and timestamp.
    """
    # calculate MD5 hash
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    # capture timestamp
    timestamp = datetime.now().astimezone().strftime("%B-%d-%Y %H:%M:%S %Z")
    # convert filepath to relative path relative to the project root
    filepath = "tasks/".join(str(Path(filepath).resolve()).split("tasks/")[1:])
    # store the results
    results = {
        "file": str(filepath),
        "md5": hash_md5.hexdigest(),
        "timestamp": timestamp,
    }
    return results


def create_md5_file_path(env, target):
    """
    This function creates a md5 file path based on the target file and extension.
    """
    md5_file_path = env.get("MD5_FILE", "")
    md5_dir = env.get("MD5_DIR", "md5")
    target = target[0] if isinstance(target, list) else target
    if md5_file_path == "":
        # no md5 file given, use the target file name
        md5_file_path = str(target).replace("output", md5_dir) + "_md5.json"
    else:
        # use absolute path to avoid path issues
        if not os.path.isabs(md5_file_path):
            md5_file_path = os.path.join(
                env.Dir(".").srcnode().abspath, md5_file_path
            )
        # only modify $MD5_FILE if it was given to avoid modifying env
        env["MD5_FILE"] = md5_file_path
    return md5_file_path
