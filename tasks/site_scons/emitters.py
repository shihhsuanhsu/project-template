"""
Shih-Hsuan Hsu
July 30, 2024
This file contains all the emitters that can be used
    in the SConstruct/SConscript files.
"""

import os
import json
from helpers import create_log_file_path, create_md5_file_path
from actions import check_pdf_compiler_action


def add_log_to_target(target, source, env, ext):
    """
    This function adds the log file as a target.
    """
    log_file = create_log_file_path(env, source, ext)
    return target + [log_file], source


def python_emitter(target, source, env):
    """
    This function is used to add the log file as a target.
    """
    return add_log_to_target(target, source, env, "py")


def stata_emitter(target, source, env):
    """
    This function is used to add the log file as a target.
    """
    return add_log_to_target(target, source, env, "do")


def julia_emitter(target, source, env):
    """
    This function is used to add the log file as a target.
    """
    return add_log_to_target(target, source, env, "jl")


def matlab_emitter(target, source, env):
    """
    This function is used to add the log file as a target.
    """
    return add_log_to_target(target, source, env, "m")


def dynare_emitter(target, source, env):
    """
    This function is used to add the log file as a target.
    """
    return add_log_to_target(target, source, env, "mod")


def link_emitter(target, source, *_, **__):
    """
    This function checks the number of source files and target files.
    """
    if len(source) > 1:
        raise ValueError("The source file must be one file.")
    # check if the number of target files is the same as the number of source files
    if len(target) != len(source):
        raise ValueError(
            "The number of target files must be the same as the number of source files."
        )
    return target, source


def md5_emitter(target, source, env):
    """
    This function is used to create an MD5 hash file
        as an additional target for the given source file.
    """
    if env.get("STORE_MD5", False):
        md5_files = []
        for target_file in target:
            target_file = str(target_file)
            if "output" in target_file:
                # compute MD5 for output files
                md5_file_path = create_md5_file_path(env, target_file)
                md5_files.append(md5_file_path)
        target += md5_files
    return target, source


def pdf_emitter(target, source, env):
    """
    This function is used to remove the fls file,
        before running the PDF builder,
        and add the log and aux files as targets.
    If a latex file was compiled with other tools,
        such as LaTeX Workshop in VSCode,
        then the created fls file will cause the PDF builder to fail:
        ` Multiple ways to build the same target
        were specified for: output/sample.pdf`.
    """
    target_path = os.path.abspath(str(target[0])).replace(".pdf", "")
    source_path = os.path.abspath(str(source[0])).replace(".tex", "")
    # remove the fls file if it exists
    fls_path = f"{target_path}.fls"
    if os.path.exists(fls_path):
        os.remove(fls_path)
    if not check_pdf_compiler_action(env):
        # add log and aux files as targets
        target, source = add_log_to_target(target, source, env, "tex")
        # add aux, toc, and out files as targets
        add_targets = [f"{target_path}.aux", f"{target_path}.log"]
        # add optional targets
        for ext in [
            "bbl",
            "blg",
            "lof",
            "lot",
            "synctex.gz",
            "snm",
            "toc",
            "fls",
            "fdb_latexmk",
            "nav",
            "out",
            "vrb",
        ]:
            if os.path.exists(f"{target_path}.{ext}"):
                add_targets.append(f"{target_path}.{ext}")
        # handle minted folder
        minted_folder = source_path.split("code")[0] + "code/_minted"
        if os.path.exists(minted_folder):
            env.Clean(target, minted_folder)
        return target + add_targets, source
    else:
        return target, source
