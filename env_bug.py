from pathlib import Path
from prefect import flow, task
import logging
import os
from pydantic import BaseModel, Field, field_validator, field_serializer
from typing import Any, Callable


def setup_logging(output_dir):
    """Simulate what jds is doing for logging - there are two handlers,
    one for the terminal and one for the file
    """

    logger = logging.getLogger("jds")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    file_handler = logging.FileHandler((output_dir/"my_logfile.log").resolve(), mode="a")
    formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)


def get_logger(who):
    """
    Parameters
    -----------
    who: str
        Log a message of the state of the logger returned based on who called this function

    Note
    ----
    Logs a warning to see what handlers exist at this point in the process...
    """
    logger = logging.getLogger("jds")
    # Let's see what's registered on this logger...
    logger.warning("%s logger handlers are %s", who, logger.handlers)
    return logger


@task
def tasker() -> None:
    log = get_logger(who="tasker")

    log.debug("tasker: debug")
    log.info("tasker: info")
    log.warning("tasker: warning")
    log.error("tasker: error")


@flow
def flow_main( ) -> None:
    """This flow represents the first part of my existing program that I want to
    turn into a series of prefect tasks
    """
    this_file = Path(__file__)
    output_dir = this_file.parent.resolve()
    setup_logging(output_dir)

    log = get_logger(who="flow_main")

    log.debug("flow_main: debug")
    log.info("flow_main: info")
    log.warning("flow_main: warning")
    log.error("flow_main: error")

    tasker()


def main():
    """This function represents a CLI that is going to parse some args
    and then set up a deployment accordingly"""

    this_file = Path(__file__)

    flow_main.from_source(
        source=str(this_file.parent.resolve()),
        entrypoint=f"{this_file.name}:flow_main",
    ).serve(
        name="env-bug",
        version="1.0.0",
    )


if __name__ == "__main__":
    main()
