# common

Code that are shared across tasks should go in this task.
Also, to enable Stata for SCons,
    please make a copy of [`code/stata_config_draft.py`](code/stata_config_draft.py)
    and rename `stata_config_draft.py` to `stata_config.py`.
Then modify `stata_config.py` according to Method 2 in the
    [documentation for pystata](https://www.stata.com/python/pystata17/install.html).

`plot_settings.py` use `Roboto` font, which might not be available by default.
Please install the font files in the code directory.
