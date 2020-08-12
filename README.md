## Prerequisites

To run this application, you must have `Python 3` with `PyQt5`.

Install `PyQt5`:
```
pip3 install PyQt5
```

## Start

To start the application, run
```
python3 main.py
```
or, if you have Python interpreter at `/usr/bin/python3`, simply run
```
./main.py
```

## Key Code Items

File `taskfile_runner.py` is the entry point to actual task running. Place the implementation in the method `Run`.

File `task_definitions.py` holds the task type definitions.

File `sample_01.json` is an example of a valid task list. To play around you better copy it into another folder, as upon `Save` or `Run` the application rewrites the file.
