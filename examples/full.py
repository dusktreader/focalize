import sys
from time import sleep

from loguru import logger
from focalize import attach_focalize

from examples.sub_demo import sub_run


def run():
    attach_focalize(sys.stderr, level="DEBUG")

    logger.info("Starting logging")

    with logger.focus("outer block"):
        logger.info("Something inside first nest level")
        sleep(0.5)
        logger.info("Something else at first nest level")
        sleep(0.5)
        with logger.focus(
            "doing nested things",
            context_level="DEBUG",
        ):
            logger.debug("Something inside second nest level")
            sleep(0.25)
            logger.debug("Something else at second nest level")
            sleep(0.25)
            try:
                sub_run()
            except Exception:
                logger.debug("Handled exception from submodule")
    logger.info("Finished logging")
