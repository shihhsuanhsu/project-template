# Tutorials

This directory contains tutorials on technologies used in this project.

## Getting Started

Please make sure you are familiar with Git and Github
    (see [`git_and_github.md](git_and_github.md) for help).
Follow [`python.md`](python.md) to set up the Conda environment.
If you need a text editor,
    we strongly recommend [VSCode](https://code.visualstudio.com).

This project is organized into a collection of tasks
    (e.g. download data, clean dataset x, clean dataset y,
    reg y on x, plot z, etc.).
Each task is a separate folder in the `tasks` directory.
In a task folder there are usually the following:

- `code` directory: code used by this task to create the outputs
- `input` directory: files needed to create the output (e.g. datasets)
- `output` directory: outputs (e.g. cleaned datasets, plots, tables, etc.)
- `README.md`: a simple description of what this task does
- `SConscript`: SCons script for build automation
    (tracking file decencies and building outputs).

The `input` directory should be filled by SCons,
    and the `output` directory should be filled by code in the code directory.
You should not be manually filling them to ensure reproducibility.
Please see [`scons.md`](scons.md) on how to use SCons.

## Credentials

All API keys and credentials should be stored
    in the [`secrets`](../../secrets/) directory.
To use them, please use relative paths in the code referencing them.
You should not link them in the `input` directory.
Also, they should not be committed and pushed to GitHub for security.

## Coding Style

When writing code (also applies to Markdown and Latex),
    please keep the length of each line under 100 characters
    (preferably, under 80 characters).
This enhances the readability when having code files side by side
    (e.g. during code review).
For Markdown and Latex,
    please break long lines according to clauses/phrases.
Exceptions are made when there are URLs (or other long strings of text).\
**IMPORTANT:** Please always use
    [relative path](https://www.geeksforgeeks.org/absolute-relative-pathnames-unix/).
