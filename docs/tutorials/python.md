# Python Tutorial

## Environment Management (Conda)

I recommend using Miniconda to manage Python environments.
Using an environment allows us to specify package and software versions,
    which increases the likelihood of reproducing results.
Please follow the instructions on [this website](https://docs.anaconda.com/miniconda/miniconda-install/)
    to install Miniconda.
For a quick tutorial on how to use `conda`,
    see [Getting started with conda](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html).

### Create an environment

You can follow the instructions in
    [Getting started with conda](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html)
    to set up your own environment,
    or use our environment file
    (a template file for a basic Python environment) to create one.
To create an environment from our environment file,
    run `conda env create -f environment.yml`
    in the [`requirements` folder](../../requirements/).
The environment file, if loaded correctly,
    should install Python, SCons, and other commonly used packages.
To rename the Conda environment: `conda rename -n template <new name>`.

**NOTE:** Remember to activate the environment when running code for this project.

### Install a package/software

To install packages or other software,
    like GNU make or Julia,
    please do it **AFTER** activating the environment.
We recommend installing packages via `conda` whenever possible,
    and following the installation instructions on the package's website.

### Speed up 'solving environment'

If Conda takes a long time to solve for the environment,
    we recommend using `libmamba` as the solver. Do the following:

```bash
conda install -n base conda-libmamba-solver
conda config --set solver libmamba
```

## Coding in Python

### Tutorials

If you are not familiar with Python,
    we recommend reading [The Python Tutorial](https://docs.python.org/3.10/tutorial/index.html),
    which covers the basics of Python.
[Learn Python the Hard Way](https://learnpythonthehardway.org/python3/ex31.html)
    is also a good reference.
For more data science-focused usage,
    [Python Data Science Handbook](https://www.oreilly.com/library/view/python-data-science/9781491912126/)
    is a popular book,
    and [Computational Methods for Economists using Python](https://opensourceecon.github.io/CompMethods/index.html)
    is a free guide.

### General tips

Please use actual Python files (with extension `.py`)
    instead of Jupyter Notebooks (with extension `.ipynb`).
If you prefer the experience of coding in Jupyter Notebooks,
    VSCode provides Jupyter Code cells in `.py` files
    (see [this link](https://code.visualstudio.com/docs/python/jupyter-support-py)
    for more details).
Output should be saved with code
    rather than interactively saving them with mouse clicks.
Use 4 spaces instead of tab characters for indentations.
Even though Python files are executed from top to bottom,
    creating functions improves readability and portability.
For good coding practices, refer to [PEP 8](https://peps.python.org/pep-0008/).
This project template, by default,
    runs [`black` (code formatter)](https://black.readthedocs.io/en/stable/index.html)
    on all python scripts when building the project.

### Speed up estimators

To speed up estimators,
    we recommend coding them with [`JAX`](https://jax.readthedocs.io/en/latest/),
    [`Numbda`](https://numba.pydata.org),
    or [`PyTorch`](https://pytorch.org) instead of [`NumPy`](https://numpy.org).
They allow [just-in-time (JIT) compilation](https://en.wikipedia.org/wiki/Just-in-time_compilation).
Jax and PyTorch support GPU acceleration.

### Working with large data

#### On a local machine

When the dataset is large
    (millions of rows or exceeds the amount of RAM on your machine),
    operating on it with [`Pandas`](https://pandas.pydata.org)
    will likely result in poor performance.
If you prefer an experience similar to `Pandas`,
    I suggest using [`Polars`](https://pola.rs) instead.
For a short tutorial on `Polars`,
    see [Modern Polars](https://kevinheavey.github.io/modern-polars/).
Alternatively, if you are more proficient in SQL,
    you can use [`DuckDB`](https://duckdb.org).
Please refer to [`DuckDB's documentation`](https://duckdb.org/docs/guides/overview.html)
    for a quick start guide.

#### On a cluster

If you have access to a cluster,
    using [`Dask`](https://www.dask.org)
    or [`PySpark`](https://spark.apache.org/docs/latest/api/python/index.html)
    will scale better when extending to terabytes of data.
For tutorials on `Dask` and `PySpark`,
    please refer to their respective documentation.
