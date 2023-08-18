import sys
from focalize import install_focalize
from loguru import logger

logger.info("info message")
logger.debug("debug message")
install_focalize(sys.stderr, level="DEBUG")
logger.info("info message")
logger.debug("debug message")
