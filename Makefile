
demo:
	PREFECT_LOGGING_EXTRA_LOGGERS=jds \
	PREFECT_LOGGING_LEVEL=INFO \
	PREFECT_LOGGING_LOGGERS_PREFECT_EXTRA_LEVEL=INFO \
	PREFECT_LOGGING_TO_API_WHEN_MISSING_FLOW='ignore' \
	uv run --with-requirements requirements.txt -p python3.10 python silly_flow.py

clean:
	uv cache clean

versions:
	uv run --with-requirements requirements.txt -p python3.10 prefect version

