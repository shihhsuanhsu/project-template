"""
Shih-Hsuan Hsu
July 27, 2025
Scanners that are used in the SCons environment.
"""

import copy


def remove_latex_scanner(scanner_obj):
    """
    Returns a new scanner object that does not include the LaTeX scanner.
    """
    cloned_obj = copy.copy(scanner_obj)
    cloned_obj.skeys = [
        skey
        for skey in cloned_obj.skeys
        if skey not in [".tex", ".ltx", ".latex"]
    ]
    return cloned_obj
