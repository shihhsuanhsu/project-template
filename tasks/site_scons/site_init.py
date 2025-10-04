"""
Shih-Hsuan Hsu
July 30, 2024
This file is provide an initialization function for a SCons environment,
    which includes builders for Python, Stata, Julia, and copying/linking files.
"""

import os
from custom_warnings import no_symlink_permission
from actions import (
    python_build_action,
    stata_build_action,
    symlink_build_action,
    copy_build_action,
    julia_build_action,
    matlab_build_action,
    dynare_build_action,
    pdf_build_action,
    check_target_exist_action,
    no_action,
)
from emitters import (
    python_emitter,
    stata_emitter,
    julia_emitter,
    link_emitter,
    matlab_emitter,
    dynare_emitter,
    pdf_emitter,
)
from methods import make_link_now, make_links, download_file, download_files
from scanners import remove_latex_scanner

# load builders
python_bld = Builder(
    action=python_build_action, src_suffix=".py", emitter=python_emitter
)
stata_bld = Builder(
    action=stata_build_action, src_suffix=".do", emitter=stata_emitter
)
julia_bld = Builder(
    action=julia_build_action, src_suffix=".jl", emitter=julia_emitter
)
matlab_bld = Builder(
    action=matlab_build_action, src_suffix=".m", emitter=matlab_emitter
)
dynare_bld = Builder(
    action=dynare_build_action, src_suffix=".mod", emitter=dynare_emitter
)
link_bld = Builder(action=symlink_build_action, emitter=link_emitter)
copy_bld = Builder(action=copy_build_action, emitter=link_emitter)
pdf_builder = Builder(action=pdf_build_action, emitter=pdf_emitter)
no_action_builder = Builder(
    action=no_action,
)


def check_symlink_permission():
    """
    This function is used to check if the user has permission to create symlinks.
    """
    permission = True
    try:
        with open("_test.txt", "w") as f:
            f.write("test")
        os.symlink("_test.txt", "_test_link.txt")
    except OSError as e:
        # handle no symlink permission on Windows machines
        if (
            "[WinError 1314] A required privilege is not held by the client"
            in str(e)
        ):
            no_symlink_permission()
        else:
            raise e
        permission = False
    finally:
        # clean up
        try:
            os.remove("_test.txt")
            os.remove("_test_link.txt")
        except FileNotFoundError:
            pass
    return permission


def add_post_action_to_all(env):
    """
    This function adds a post action to all builders in the environment.
    """
    original_builders = {}

    # store original builder methods
    for builder_name in env["BUILDERS"]:
        original_builders[builder_name] = env["BUILDERS"][builder_name]

    # create wrapper that adds PostAction
    def create_wrapper(original_builder):
        def wrapper(*args, **kwargs):
            result = original_builder(*args, **kwargs)
            env.AddPostAction(result, check_target_exist_action)
            return result

        return wrapper

    # apply wrapper to all builders
    for builder_name, builder in original_builders.items():
        env["BUILDERS"][builder_name] = create_wrapper(builder)


def init_env():
    """
    Returns an environment with builders
        for Python, Stata, Julia, and copying/linking files.
    """
    # create an environment
    env = Environment()
    # use MD5 for the decider
    env.Decider("MD5")
    # set ALWAYS_COPY to True if no symlink permission
    env["ALWAYS_COPY"] = not check_symlink_permission()
    env.Append(
        BUILDERS={
            "Python": python_bld,
            "Stata": stata_bld,
            "Julia": julia_bld,
            "Matlab": matlab_bld,
            "Dynare": dynare_bld,
            "Copy": copy_bld,
            "Link": link_bld,
            "PDF": pdf_builder,
            "NoAction": no_action_builder,
        }
    )
    # remove latex scanner
    env["SCANNERS"] = [
        remove_latex_scanner(scanner) for scanner in env["SCANNERS"]
    ]
    # add the make_link_now function
    env.AddMethod(make_link_now, "LinkNow")
    # attach the make_links function
    env.AddMethod(make_links, "Links")
    # attach the download_file function
    env.AddMethod(download_file, "Download")
    # attach the download_files function
    env.AddMethod(download_files, "Downloads")
    # add post action to all builders
    add_post_action_to_all(env)
    return env
