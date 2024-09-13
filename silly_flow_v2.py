from pathlib import Path
from prefect import flow
from rich.logging import RichHandler
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

    # Side note: The RichHandler highlighting works before the flow runs,
    # but inside flow-main the highlighting is stripped.
    shell_handler = RichHandler()
    shell_handler.setLevel(logging.INFO)
    logger.addHandler(shell_handler)

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


class FlowArg(BaseModel):
    """This class represents the inputs to my deployment/flow, which are calculated
    from the command line args passed to "main" before the deployment runs
    """
    my_arg: int
    output_dir: Path

    @field_validator("my_arg", mode="after")
    @classmethod
    def log_a_status_message(cls, v):
        log = get_logger(who="validator")
        log.info("validator: A whole bunch of complicated checks passed!")
        log.debug("validator: This is supposed to be in the file, but not the terminal or the Prefect UI")
        return v

    @field_serializer("output_dir", when_used="json")
    def serialize_path(self, path: Path) -> str:
        return str(path.resolve())


@flow
def flow_main(
    dataset: FlowArg,
) -> None:
    """This flow represents the first part of my existing program that I want to
    turn into a series of prefect tasks
    """
    # When the flow starts, the previous log setup seems to be blown away -- 
    # recreate it here
    setup_logging(dataset.output_dir)
    
    log = get_logger(who="flow_main")

    log.info("flow_main: The flow ran successfully!")
    log.debug("flow_main: This is supposed to be in the file, but not the terminal or the prefect UI")

@flow
def flow_precheck(
    output_dir: str,
    my_arg: int
):
    output_path = Path(output_dir)
    setup_logging(output_path)

    log = get_logger(who="precheck")
    log.info("precheck: the precheck flow is running now")
    log.debug("precheck: This is supposed to be in the logfile, but not the terminal or the prefect UI")

    my_arg = FlowArg(output_dir=output_path, my_arg=42)
    flow_main(my_arg)


def main():
    """This function represents a CLI that is going to parse some args
    and then set up a deployment accordingly"""
    
    this_file = Path(__file__)
    flow_main.from_source(
        source=str(this_file.parent.resolve()),
        entrypoint=f"{this_file.name}:flow_precheck",
    ).serve(
        name="a-silly-flow",
        version="1.2.3",
        parameters = {
            "output_dir": str(this_file.parent.resolve()),
            "my_arg": 42,
        }
    )


if __name__ == "__main__":
    main()
