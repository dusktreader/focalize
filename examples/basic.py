import sys
from time import sleep
from focalize import attach_focalize
from loguru import logger

attach_focalize(sys.stderr, level="DEBUG")

with logger.focus("demo loop"):
    for i in range(5):
        logger.info(f"Executing step {i+1} of 5")
        sleep(0.1)
