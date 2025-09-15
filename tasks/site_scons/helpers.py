"""
Shih-Hsuan Hsu
July 19, 2025
Helper functions for SCons environment.
"""

import os


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
