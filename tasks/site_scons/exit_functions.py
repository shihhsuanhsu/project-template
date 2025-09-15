"""
Shih-Hsuan Hsu
July 22, 2025
All the functions that can be registered to be called at exit go here.
"""

import sys
from pathlib import Path
import re
from SCons.Script import GetBuildFailures
from monkey_patches import WARNINGS


def print_fail_summary():
    """
    Print build failure summary in red color.
    """
    RED = "\033[91m"
    RESET = "\033[0m"
    first = True
    for bf in GetBuildFailures() or []:
        if first:
            first = False
            print(f"{RED}scons: Build failure(s):{RESET}", file=sys.stderr)
        if bf is not None:
            msg = "%s: %s" % (bf.node or bf.filename, bf.errstr)
            print(f"\t{RED}scons: {msg}{RESET}", file=sys.stderr)
            # extract the log file if it exists
            action = bf.command
            if action:
                log_files = re.findall(r"([a-zA-Z0-9_\.\/]+\.log)", action)
                if log_files:
                    print(
                        f"\t\t{RED}Log file(s): {log_files}{RESET}",
                        file=sys.stderr,
                    )
        else:
            print(
                f"\t{RED}scons: Unknown build failure{RESET}", file=sys.stderr
            )


def print_warning_summary():
    """
    Print warning summary in yellow color.
    """
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    first = True
    # remove warning with the same message
    unique_warnings = set(WARNINGS)
    for warning in unique_warnings:
        if first:
            first = False
            print(f"{YELLOW}scons: Warning(s):{RESET}", file=sys.stderr)

        if warning is not None:
            if hasattr(warning, "__class__"):
                warning_class = warning.__class__.__name__
                warning_msg = str(warning)
                msg = f"{warning_class}: {warning_msg}"
            else:
                msg = str(warning)

            print(f"\t{YELLOW}scons: {msg}{RESET}", file=sys.stderr)
            # print additional information if available
            if hasattr(warning, "filename") and warning.filename:
                print(
                    f"\t\t{YELLOW}File: {warning.filename}{RESET}",
                    file=sys.stderr,
                )
            if hasattr(warning, "lineno") and warning.lineno:
                print(
                    f"\t\t{YELLOW}Line: {warning.lineno}{RESET}",
                    file=sys.stderr,
                )
        else:
            print(f"\t{YELLOW}scons: Unknown warning{RESET}", file=sys.stderr)


def remove_locks():
    """
    Remove the project lock file if it exists.
    This is useful for cleaning up after a build.
    """
    lock_file = Path(".project_write.lock")
    if lock_file.exists():
        lock_file.unlink()
