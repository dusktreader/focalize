import sys
from focalize import attach_focalize
from loguru import logger

logger.info("info message")
logger.debug("debug message")
attach_focalize(sys.stderr, level="DEBUG")
logger.info("info message")
logger.debug("debug message")
