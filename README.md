# Series Marker
> Simple script to track watched episodes of a series
<br/>

## `argparse` Module
Parses the arguments passed when the app is initially called
* The arguments are:
1. `-f, --folder`: specifies the folder to walk through and find files with extensions specified by `VALID_FORMATS` list
2. `-l, --list`: shows the saved tree of folders and files and shows their status (Watched or not)
3. `-m, --mark`: iterates through the saved list of unwatched episodes and asks if their status has changed or not

## `pathlib` Module
Gives the `Path` object which is used by: 
* `-f` argument conditional: to verify the existence of the passed folder
* `walk()` function: which walks through the directory tree and finds files with valid formats returning a dictionary of all the contents

## `json` Module
Uses `dump()` and `load()` to save to and load data from the json file specified with `DATA_FILE` constant
* `rwalk()` function: reverses the `walk()` function and gets the directory tree from the data file returning a string with the result ready for output to the terminal
* `scan()` function: similar to `rwalk()`, except it prompts the user for marking the unwatched episodes returning the modified directory tree

