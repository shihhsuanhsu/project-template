"""
Shih-Hsuan Hsu
July 19, 2025
This file stores the methods for the SCons environment.
"""

import os
from pathlib import Path
from itertools import chain
import filecmp
from actions import symlink_build_action
from helpers import convert_scons_path


def make_link_now(self, target, source, COPY=False, SUBS: dict = {}):
    """
    Immediately create a symbolic link to or copy the source file.
    If SUBS is not None and COPY is True, the target file will be modified in place.
    Args:
        target: The target file to create the link to.
        source: The source file to link to.
        COPY: If True, copy the source file instead of creating a link.
        SUBS: A dictionary of substitutions to apply to the target file.
    Returns:
        A SCons dependency object that links the target and source files.
    Raises:
        ValueError: If SUBS is not None and COPY is False.
        TypeError: If SUBS is not a dictionary.
    """
    if SUBS and not COPY:
        raise ValueError("SUBS are not allowed for symbolic links.")
    if type(SUBS) is not dict:
        raise TypeError("SUBS must be a dictionary.")
    # convert '#' to project root path
    source = os.path.abspath(convert_scons_path(self, source))
    target = os.path.abspath(convert_scons_path(self, target))
    status = 0
    # do not rebuild if the target file is the same as the source file
    if not (
        Path(str(target)).exists()
        and filecmp.cmp(str(target), str(source), shallow=False)
    ):
        status = symlink_build_action(
            target=[target],
            source=[source],
            env=self,
            copy=COPY,
            no_copy_warning=True,
        )
        if SUBS is not None:
            # apply SUBS to the target file
            with open(str(target), "r") as f:
                content = f.read()
            for old, new in SUBS.items():
                content = content.replace(old, new)
            with open(str(target), "w") as f:
                f.write(content)
    # still preserves the dependency
    return self.NoAction(target=target, source=source, STATUS=status)


def make_links(
    self,
    target: list,
    source: list,
    COPY: bool = False,
    NOW: bool = False,
    SUBS: dict = {},
):
    """
    Create links between the target and source files.
    Order of the target and source files must match.
    If SUBS is not None and COPY is True, the target file will be modified in place.
    Args:
        target: A list of target files to create links to.
        source: A list of source files to link to.
        COPY: If True, copy the source files instead of creating links.
        NOW: If True, create the links immediately.
    Returns:
        A list of SCons dependency objects that link the target and source files.
    Raises:
        ValueError: If the number of target files is not the same as the number of source files.
        ValueError: If SUBS is not None and COPY is False.
        TypeError: If SUBS is not a dictionary.
    """
    # type conversion
    if not isinstance(target, list):
        target = [target]
    if not isinstance(source, list):
        source = [source]
    # check if the number of target files is the same as the number of source files
    if len(target) != len(source):
        raise ValueError(
            "The number of target files must be the same as the number of source files."
        )
    if NOW:
        return list(
            chain(
                *[
                    make_link_now(
                        self=self, target=t, source=s, COPY=COPY, SUBS=SUBS
                    )
                    for t, s in zip(target, source)
                ]
            )
        )
    else:
        return list(
            chain(
                *[
                    self.Link(
                        target=t,
                        source=s,
                        COPY=COPY,
                    )
                    for t, s in zip(target, source)
                ]
            )
        )


def download_file(self, target, source):
    """
    Download a file from a URL (source) to the target path.
    """

    # convert '#' to project root path
    target = convert_scons_path(self, target)
    target_abspath = Path(os.path.abspath(target))
    # use target name as the log file name
    log_file = self.get("LOG_FILE", None)
    log_dir = self.get("LOG_DIR", "logs")
    if log_file is None:
        parts = target_abspath.with_suffix(".log").parts
        log_file = Path(*[part.replace("output", log_dir) for part in parts])

    return self.Python(
        target=target,
        source="#/common/code/download_file.py",
        ARGS=[source, str(target_abspath)],
        LOG_FILE=str(log_file),
    )


def download_files(self, target: list, source: list):
    """
    Download multiple files from URLs to the target paths.
    The order of the target and source files must match.
    """
    # type conversion
    if not isinstance(target, list):
        target = [target]
    if not isinstance(source, list):
        source = [source]
    # check if the number of target files is the same as the number of source files
    if len(target) != len(source):
        raise ValueError(
            "The number of target files must be the same as the number of source files."
        )
    return list(
        chain(
            *[
                self.Download(
                    target=t,
                    source=s,
                )
                for t, s in zip(target, source)
            ]
        )
    )
