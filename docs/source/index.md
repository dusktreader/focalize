# Focalize

**You can't depend on your eyes when your imagination is out of focus _--Mark Twain_**

![focalize-demo](images/focalize-demo.gif)


## Overview

Focalize provide context within logs for blocks of code that are encircled by a
context manager. This helps contextualize log lines within deeply nested call chains or
within complex operations where many logical steps are taken.


## Quickstart

### Requirements

* Python 3.8 or greater


### Installation

This will install the latest release of py-buzz from pypi via pip:

```bash
pip install py-buzz
```

### Basic Usage

The `Focalize` class needs only to be installed on the loguru logger. All subsequent
invocation of logging will use the `Focalize` format. This includes some coloration.
This also makes the `focus()` context manager available on the logger instance.

To install the formatter, simply call the `attach_focalize()` function with the
arguments you would pass to any new `loguru` handler:

```python
from focalize import install_focalize
attach_focalize(sys.stderr, level="DEBUG")
```

Note that this will remove any other installed handlers by default. If you do not wish
to remove other handlers, pass the `remove_other_handlers=False` keyword argument.

To designate that a part of your code should be indented with a `Focalize` indented
block, use the `focus()` context manager that is added to the `logger`:

```python
from time import sleep
from loguru import logger

with logger.focus("demo loop"):
    for int i in range(5):
        logger.info(f"Executing step {i+1} of 5")
        sleep(0.1)
```

The logging output from such a block will look like:

```
2023-08-17T15:44:03.595308-0700 |   INFO    | commenced demo loop
2023-08-17T15:44:03.598173-0700 |   INFO    | |-Executing step 1 of 5
2023-08-17T15:44:03.698453-0700 |   INFO    | |-Executing step 2 of 5
2023-08-17T15:44:03.798922-0700 |   INFO    | |-Executing step 3 of 5
2023-08-17T15:44:03.899576-0700 |   INFO    | |-Executing step 4 of 5
2023-08-17T15:44:04.000146-0700 |   INFO    | |-Executing step 5 of 5
2023-08-17T15:44:04.101024-0700 |   INFO    | completed demo loop (in 0.50 second)
```

### Format Changes

In order to keep the logging within the context blocks aligned, `Focalize` changes the
default formatting used by `loguru`. In particular, the meta data for _where_ the
log lines are generated is put after the message instead of before it. Also, the
location metadata is only included for lines using the `DEBUG` level.

Additionally, `Focalize` logs all lines in the UTC timezone. This can be disabled by
passing `local_timestamps` to the `__init__()` method or the `attach_focalize()`
function.

Default log format:
```
2023-08-17 16:22:12.942 | INFO     | __main__:<module>:5 - info message
2023-08-17 16:22:12.942 | DEBUG    | __main__:<module>:6 - debug message
```

Focalize log format:
```
2023-08-17 11:22:12.944 UTC |   INFO    | info message
2023-08-17 11:22:12.945 UTC |   DEBUG   | debug message  -> (__main__:<module>:9)
```
