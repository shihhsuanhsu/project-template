"""
Shih-Hsuan Hsu
July 30, 2024
This file contains all the build actions that can be used
    in the SConstruct/SConscript files.
"""

import os
import subprocess
from pathlib import Path
from helpers import create_log_file_path, parse_args
from custom_warnings import (
    no_symlink_permission,
    no_pdf_compiler,
    file_not_found_warning,
)


def copy_file_with_metadata(src, dst):
    """
    This function copies a file from `src` to `dst` while preserving metadata.
    """

    if os.name == "nt":
        # windows: 'copy' command (metadata copy options on Windows are limited)
        # replace forward slashes with backslashes for Windows compatibility
        src = src.replace("/", "\\")
        dst = dst.replace("/", "\\")
        cmd = ["cmd", "/c", "copy", "/Y", src, dst]
    else:
        # unix-like: use 'cp -p' to preserve metadata (permissions, timestamps)
        cmd = ["cp", "-p", src, dst]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError("Copy failed: " + result.stderr.decode())


def symlink_build_action(
    target, source, env, copy=False, no_copy_warning=False
):
    """
    This function is used to create a symbolic link to the source file.

    Args:
        target: The target file to create the link to.
        source: The source file to link to.
        copy: If True, copy the source file instead of creating a link.
        no_copy_warning: If True, do not raise a warning if the source file is copied
            instead of linked.
            Can also be set in the SCons environment (NO_COPY_WARNING).
    Returns:
        0 if the link is created successfully, 1 if the link already exists.
    """

    # check for copy flag
    copy = copy or env.get("COPY", False)
    # check if always copy instead
    copy_always = env.get("ALWAYS_COPY", False)
    if copy or copy_always:
        # get the absolute paths for the source and target files
        t = os.path.abspath(str(target[0]))
        s = os.path.abspath(str(source[0]))
        # copy the file
        no_copy_warning = env.get("NO_COPY_WARNING", False) or no_copy_warning
        if not no_copy_warning:
            no_symlink_permission(f"Copying {s} to {t} instead of linking.")
        copy_file_with_metadata(s, t)
    else:
        # get relative paths for the source and target files
        t = os.path.relpath(str(target[0]))
        s = os.path.relpath(str(source[0]), start=os.path.dirname(t))
        # create a symbolic link
        os.symlink(s, t, os.path.isdir(s))
    # return success
    return 0


def copy_build_action(target, source, env, no_copy_warning=False, *_, **__):
    """
    This function is used to copy the source file to the target file.
    Args:
        target: The target file to copy to.
        source: The source file to copy from.
        no_copy_warning: If True, do not raise a warning if the source file is copied
            instead of linked.
            Can also be set in the SCons environment (NO_COPY_WARNING).
    Returns:
        0 if the link is created successfully, 1 if the link already exists.
    """
    return symlink_build_action(
        target=(target),
        source=(source),
        env=env,
        copy=True,
        no_copy_warning=no_copy_warning,
    )


def stata_build_action(source, env, *_, **__):
    """
    This function is used to execute the first Stata file in the source.
    Any print statements in the source files will be redirected to a log file
    with the same name as the source file, but with a `.log` extension.
    """
    # get directory and filename
    dir_name, filename = os.path.split(str(source[0]))
    # get stata runner location
    run_stata_path = os.path.abspath("site_scons/run_do_file.py")
    # get log file path
    log_file_path = create_log_file_path(env, source, "do")
    # add the path to the Stata configuration file
    os.environ["STATA_CONFIG_PATH"] = os.path.abspath(
        "common/code/stata_config.py"
    )
    with open(log_file_path, "w", encoding="utf-8") as log_file:
        runner = subprocess.run(
            ["python", run_stata_path, filename] + parse_args(env, True),
            cwd=dir_name,
            stdout=log_file,
            stderr=log_file,
            check=True,
        )
    # scan the log file for errors
    with open(log_file_path, "r", encoding="utf-8") as log_file:
        log = log_file.read()
        if "ERROR RUNNING DO FILE:" in log:
            return 1
    return runner.returncode


def generic_build_action(source, env, program, ext, *_, **__):
    """
    This function is used to execute the first `program` file in the source.
    Any print statements in the source files will be redirected to a log file
    with the same name as the source file, but with a `.log` extension.
    """
    # get directory and filename
    dir_name, filename = os.path.split(str(source[0]))
    log_file_path = create_log_file_path(env, source, ext)
    with open(log_file_path, "w", encoding="utf-8") as log_file:
        runner = subprocess.run(
            [program, filename] + parse_args(env),
            cwd=dir_name,
            stdout=log_file,
            stderr=log_file,
            check=True,
        )
    return runner.returncode


def python_build_action(target, source, env):
    """
    This function is used to execute the first Python file in the source.
    Any print statements in the source files will be redirected to a log file
    with the same name as the source file, but with a `.log` extension.
    """
    return generic_build_action(
        target=target, source=source, env=env, program="python", ext="py"
    )


def julia_build_action(target, source, env):
    """
    This function is used to execute the first Julia file in the source.
    Any print statements in the source files will be redirected to a log file
    with the same name as the source file, but with a `.log` extension.
    """
    return generic_build_action(
        target=target, source=source, env=env, program="julia", ext="jl"
    )


def dynare_build_action(target, source, env):
    """
    This function is used to execute the first Dynare file in the source.
    Any print statements in the source files will be redirected to a log file
    with the same name as the source file, but with a `.log` extension.

    **NOTE**: Matlab (Dynare) scripts do not take arguments,
    so the arguments are passed as a environmental variable named `ARGS`.
    """
    return matlab_build_action(target, source, env, dynare=True)


def matlab_build_action(target, source, env, dynare=False):
    """
    This function is used to execute the first Matlab file in the source.
    Any print statements in the source files will be redirected to a log file
    with the same name as the source file, but with a `.log` extension.

    **NOTE**: Matlab scripts do not take arguments,
    so the arguments are passed as a environmental variable named `ARGS`.
    """
    # parse arguments as environmental variables,
    # because matlab scripts do not take arguments
    arguments = parse_args(env)
    env_vars = {**os.environ}  # prevent modifying the original environment
    if arguments:
        env_vars["ARGS"] = f"{arguments}"
    # get directory and filename
    dir_name, filename = os.path.split(str(source[0]))
    if dynare:
        log_file_path = create_log_file_path(env, source, "mod")
    else:
        log_file_path = create_log_file_path(env, source, "m")
    # check if Dynare is used
    if dynare:
        executor = f"try, dynare {filename}, catch error, disp(getReport(error,'extended')), exit(1), end, exit(0);"
    else:
        executor = f"try, run('{filename}'), catch ERROR, display(ERROR), exit(1), end, exit(0);"
    with open(log_file_path, "w", encoding="utf-8") as log_file:
        runner = subprocess.run(
            ["matlab", "-nodesktop", "-nosplash", "-r", executor],
            cwd=dir_name,
            stdout=log_file,
            stderr=log_file,
            check=True,
            env=env_vars,
        )
    return runner.returncode


def touch_target_action(target, source, env):
    """
    This function is used to update the timestamp of the target file.
    """
    target_file = os.path.abspath(str(target[0]))
    Path(target_file).touch()
    return 0


def check_pdf_compiler_action(env):
    """
    This function is used to check if the PDF compiler is available.
    """
    pdf_compiler = env.get("PDF_COMPILER", "lualatex")
    runner = subprocess.run(
        [pdf_compiler, "--version"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )
    return runner.returncode


def pdf_build_action(target, source, env):
    """
    This function is used to compile a LaTeX file to a PDF.
    """
    if not check_pdf_compiler_action(env):
        # get the PDF compiler
        pdf_compiler = env.get("PDF_COMPILER", "lualatex")
        # set the output directory
        otuput_dir = os.path.relpath(
            os.path.split(str(target[0]))[0],
            start=os.path.split(str(source[0]))[0],
        )
        # set the arguments
        pdf_env = env.Clone()
        pdf_env["ARGS"] = parse_args(env)
        pdf_env["ARGS"] += [
            "-interaction=nonstopmode",
            "--file-line-error",
            "--shell-escape",
            f"--output-directory={otuput_dir}",
        ]
        if pdf_compiler in ["latexmk", "pdflatex"]:
            pdf_env["ARGS"] += ["-pdf"]
        # set the log file path
        dir_name, filename = os.path.split(str(source[0]))
        log_file_path = create_log_file_path(env, source, "tex")
        # compile
        with open(log_file_path, "w", encoding="utf-8") as log_file:
            runner = subprocess.run(
                [pdf_compiler] + pdf_env.get("ARGS", []) + [filename],
                cwd=dir_name,
                stdout=log_file,
                stderr=log_file,
                check=True,
            )
        return runner.returncode
    else:
        # no PDF compiler found
        no_pdf_compiler()
        return touch_target_action(target, source, env)


def check_target_exist_action(target, source, env, ignore_missing_target=True):
    """
    this function is used to check if the target file exists.
    """
    ignore_missing_target = (
        env.get("IGNORE_MISSING_TARGET", True) and ignore_missing_target
    )
    status = 0
    for t in target:
        path = str(t)
        if not Path(path).exists():
            file_not_found_warning(path)
            status = 1 if not ignore_missing_target else 0
    return status


def no_action(target, source, env):
    """
    This function does nothing.
    It is used to create a target that does not require any action.
    Returns the status code in the environment variable `STATUS`.
    """
    return int(env.get("STATUS", 0))
