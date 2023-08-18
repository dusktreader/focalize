import sys
from time import sleep
from focalize import install_focalize
from loguru import logger

install_focalize(sys.stderr, level="DEBUG")

with logger.indented("demo loop"):
    for i in range(5):
        logger.info(f"Executing step {i+1} of 5")
        sleep(0.1)
