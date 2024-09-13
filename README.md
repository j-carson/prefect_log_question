# Background

I am porting a command line based data pipeline to prefect and am trying to 
set up logging.

The current program - reads a bunch of command line args, validates them,
generates a pydantic model, and calls a "driver" function with that model result.
Goal is that the driver function will be broken down in prefect tasks that can run 
in parallel, greatly increasing my efficiency.

The driver program logs stuff as it goes. The logger has two handlers: One that
sends stuff to the terminal a log-level INFO and one that sends lots of extra
stuff to a log file at DEBUG level.

I'm trying to do the same thing in my new deployment. I want the INFO and above
log data to show up in the prefect UI but leave the DEBUG stuff down in the
log file (there is a lot of it and no need to upload it to the cloud).

# Setup and run

```bash
pip install uv
make demo
```

Be sure to look at the logging environment as set up in the Makefile.

# Observed behavior

In the terminal I see:

- Validator logs are output twice: Once before the flow starts and once in the flow.
  (I can just live with that for now)
- Before the flow starts, the rich highlighting works, but not afterwards.
- Debug logs are suppressed as desired.

In the log file I see:

- Validator logs are output once, debug messages are there as expected

In the prefect UI I see:

- Debug message from flow_main is output. I do not want that.
- No messages from validator come out. I don't expect the one from before the flow
  starts, just for when the flow is running. Not sure how to get the logging set up
  before the flow "officially" starts though?


# Second attempt

```bash
make demo2
```

This is silly_flow_v2.py

Since there was this odd state where the validators wanted to log stuff
but weren't in a flow, I decided to make the "main" of my python program do
as little as possible -- now a precheck-flow validates the structures and then
calls the main flow.

The good news is that the validator messages now show up in the UI, in the 
precheck-flow.

The bad news is that the logs to the terminal and the file from the "main"
flow show up twice. And the debug logs going to the UI remains a problem.

