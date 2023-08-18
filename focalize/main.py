import contextlib
from loguru import logger
import pendulum
import sys


class Focalize:

    indent_count: int
    local_timestamps: bool

    def __init__(self, local_timestamps=False):
        self.indent_count = 0
        self.local_timestamps = local_timestamps

    def _format(self, record) -> str:
        if self.indent_count > 0:
            record["extra"]["indentation"] = ("| " * (self.indent_count - 1)) + "|-"
        else:
            record["extra"]["indentation"] = ""

        time_fmt_str: str = "YYYY-MM-DD hh:mm:ss.SSS zz"
        if not self.local_timestamps:
            time_fmt_str += "!UTC"

        fmt: str = " | ".join(
            [
                f"<green>{{time:{time_fmt_str}}}</green>",
                "<level>{level: ^9}</level>",
                "<yellow>{extra[indentation]}</yellow>{message}",
            ]
        )

        if record["level"].name == "DEBUG":
            fmt += "  <blue>-> ({name}:{function}:{line})</blue>"

        fmt += "\n"

        return fmt

    @contextlib.contextmanager
    def indented(self, indent_label: str, context_level: str = "INFO"):
        """
        Provides a context manager so that indentation may be activated for a
        block of code

        Args:
            indent_label:     An optional level describing the process contained within
                              this context. This label will be printed at the beginning
                              and end of each indented block
            label_log_levell: The logging level at which to log the context lines
                              (if not specified, defaults to self.info)
        """

        if indent_label is None:
            indent_label = "indented block"

        logger.opt(ansi=True).log(
            context_level,
            f"<yellow>commenced {indent_label}</yellow>",
        )

        moment_commenced = pendulum.now()
        self.indent_count += 1
        try:
            yield
        finally:
            self.indent_count -= 1
            moment_completed = pendulum.now()
            duration = (moment_completed - moment_commenced).in_words()
            if sys.exc_info() == (None, None, None):
                final_status = "completed"
                status_color = "yellow"
            else:
                final_status = 'failed'
                status_color = "red"
            if indent_label is not None:
                logger.opt(ansi=True).log(
                    context_level,
                    (
                        f"<{status_color}>{final_status} "
                        f"{indent_label}</{status_color}> "
                        f"<yellow>(in {duration})</yellow>"
                    ),
                )


def install_focalize(
    *logger_add_args,
    remove_other_handlers=True,
    local_timestamps=False,
    **logger_add_kwargs,
) -> Focalize:
    """
    Install the Focalize handler to the loguru logger.

    Args:
        logger_add_args:       Arguments to pass along to `logger.add()`
        remove_other_handlers: If True, other handlers will be removed from the loguru logger
        local_timestamps:      If True, timestamps will be shown in the local timezone
        logger_add_kwargs:     Keyword arguments to pass along to `logger.add()`
    """
    instance: Focalize = Focalize(local_timestamps=local_timestamps)
    if remove_other_handlers:
        logger.remove()
    logger.add(*logger_add_args, format=instance._format, **logger_add_kwargs)
    logger.__class__.indented = instance.indented  # type: ignore
    return instance
