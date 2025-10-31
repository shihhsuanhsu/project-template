# Project Template

Managing script execution order in research projects is tedious and error-prone.
This project template delegates these tasks to [SCons](https://scons.org),
    a powerful [build tool](https://stackoverflow.com/questions/7249871/what-is-a-build-tool)
    that automatically handles dependencies and execution order.
Once you specify the dependencies, SCons determines the correct execution sequence.
When files change (e.g., data cleaning scripts or new data),
    SCons intelligently runs only the affected scripts instead of reprocessing everything.
This project template includes custom builders for executing Python, Stata, Julia, etc.
    (see [`docs/tutorials/scons.md#builders`](docs/tutorials/scons.md#builders)).

This template builds on [Jonathan Dingel's project template](https://github.com/jdingel/projecttemplate)
    but uses SCons instead of [GNU make](https://www.gnu.org/software/make/).
While both tools have merits, I think SCons provides better cross-platform compatibility.
I recommend avoiding command-line tools (`cp`, `grep`, `awk`, `wget`, etc.)
    and shell scripts in favor of Python scripts.
This ensures consistent behavior across different operating systems
    where command-line tools may be missing or behave differently.

**NOTE**: This template is actively developed and currently passes basic functionality tests
    on Ubuntu and MacOS.
I will test this on Windows in the future.
Please report bugs or request features through
    [GitHub Issues](https://github.com/shihhsuanhsu/project-template/issues).

## Infrastructure

### Project Organization

Following Dingel's approach, this template organizes work as a series of interconnected tasks
    that form an automated [data pipeline](https://www.geeksforgeeks.org/overview-of-data-pipeline/).

Each task follows a standardized structure:
```bash
task_name/
├── code/              # All executable scripts
│   └── main_script.py
├── input/             # Dependencies and data (optional)
├── output/            # Generated results (optional)
├── logs/              # Store the logs from code execution (optional)
├── README.md          # Task description
└── SConscript         # Dependency specification
```

**Key Principles:**
- **Dependencies**: Link required datasets in the `input` folder
- **Code Organization**: Store all executable scripts in `code`
- **Working Directory**: All file references assume `code` as the working directory
- **Output Management**: Save all results to the `output` folder
- **Dependencies**: Define relationships and commands to run the scripts in `SConscript`

**Execution**: Run `scons` from the `tasks` directory to execute all SConscripts.
See the `scons_demo` and `write_up` tasks for examples.

### Task Visualization

SCons automatically generates a task dependency graph each time you run it
    (if enabled in `tasks/SConstruct` and have Graphviz installed).
This visualization helps you understand task relationships and pipeline flow.
Find the graph at `tasks/task_graph/output/task_graph.png`.

## Quick Start Guide

1. **Install Dependencies**
    - Follow instructions in `requirements/README.md`
2. **Configure Integrations**
    - Set up Stata and Python integration per `tasks/common/README.md`
3. **Set Up Credentials (optional)**
    - Configure API keys as described in `secrets/README.md`
4. **Run the Pipeline**
    ```bash
    # Navigate to tasks directory
    cd tasks

    # Activate your Python environment
    conda <environment name>

    # Then run SCons with desired thread count
    scons -j <number_of_threads>
    # or just `scons`
    ```

**Note**: Initial execution may take significant time
    depending on your network speed and computational resources.

## Additional Resources

Some tutorials and documentation are available in [`docs/tutorials`](docs/tutorials).
