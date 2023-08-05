import logging
import sys


def init(loglevel):
    """Configure console logging. Info and below go to stdout, others go to stderr.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(loglevel)

    handler_stdout = logging.StreamHandler(sys.stdout)
    handler_stdout.setLevel(logging.DEBUG)
    handler_stdout.addFilter(
        type(
            "",
            (logging.Filter,),
            {"filter": staticmethod(lambda r: r.levelno <= logging.INFO)},
        )
    )
    root_logger.addHandler(handler_stdout)

    handler_stderr = logging.StreamHandler(sys.stderr)
    handler_stderr.setLevel(logging.WARNING)
    root_logger.addHandler(handler_stderr)
