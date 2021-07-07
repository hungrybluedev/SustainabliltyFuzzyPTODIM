# Implementation of Pythagorean Fuzzy TODIM

## Overview

### Pythagorean Fuzzy Number Datatype

[pfn.py](Pythagorean_Fuzzy_TODIM/pfn.py) contains the implementation of the fuzzy number. Refer to the manuscript for the sources.

### Main Notebook

[Pythagorean Fuzzy TODIM](Pythagorean_Fuzzy_TODIM/Pythagorean%20Fuzzy%20TODIM%20Ranking.ipynb) is the jupyter notebook that contains the implementation of the Fuzzy variant of TODIM. It requires the data to be stored in a CSV format in the `data` folder.

### Additional Files

The rest of the files are for generating rankings in bulk under different parameters. This is useful for sensitivity analysis. The reports are included as PDF and the images as PNG.

## Requirements

1. Basic familiarity with the command prompt.
2. Python 3 must be installed. Preferably the latest version.
3. Ensure that the latest version of `pip` and `virtualenv` are installed.
4. Make sure that commands the previous commands can be executed by adding them to path or through `python -m pip ...`, etc.

## Instructions

### First Time Use

Follow all steps from 1 to 6.

### Second Time Onwards

Follow step 3, then step 5 onwards.

1. Navigate to the root folder of the cloned repository in the terminal.
2. Create a virtual environment: `virtualenv venv`
3. Activate the newly created virtual environment: `. venv/bin/activate`. The command maybe slightly different for Windows.
4. Install all dependencies: `pip install -r requirements.txt`.
5. Start the Jupyter Notebook Server: `jupyter notebook`
6. A Jupyter Environment will be opened in the default browser. Navigate to the desired notebook and run the cells to execute the code.
7. After work is complete, deactivate the virtual environment: `deactivate`. Or simple close the terminal.

## Contact

In case of any difficulties, please contact Subhomoy Haldar via [Twitter](https://twitter.com/hungrybluedev).