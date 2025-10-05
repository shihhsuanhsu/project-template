# Project Template

Version: 0.2.8

**NOTE:** Please do not modify this file.
Shih-Hsuan uses this file to track the project template version.

## Update log

### 0.2.8

- Remove unused functions
- Update packages in the conda environment file

### 0.2.7

- Use MD5 decider
- Improve handling for argument (escape spaces and allow for a non-list argument)

### 0.2.6

- Use `logs` dir

### 0.2.5

- Add sample code to download data from FRED

### 0.2.4

- Drop Pylnt related code (only use black)
- Simplify conda environment yaml file
    - Add `linearmodels`
    - Remove `scikit-learn`, `pep8`, `pylint`, and `sdmx1`
    - Remove `wget` (did not realize it does not support Windows)

### 0.2.2

- Improve docs

### 0.2.1

- Fix bugs related to task graph

### 0.2.0

- Clean up documentations

### 0.1.9

- Add more comments

### 0.1.8

- Replace `shutil.copy2` with system calls (attempt to deal with busy IO)

### 0.1.7

- Remove the project lock

### 0.1.6

- Add a lock to deal with busy IO when using LinkNow
- Did not test the lock on a Windows machine

### 0.1.5

- Disable default PDF scanner because it generates unnecessary warnings

### 0.1.4

- Run black to format code before build

### 0.1.3

- Store and summarize all SCons warnings at exit

### 0.1.2

- Report paths to log files if available in the build failure summary

### 0.1.1

- Add build failure summary
