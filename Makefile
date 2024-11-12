
SET_ENV = PREFECT_LOGGING_EXTRA_LOGGERS=jds \
	PREFECT_LOGGING_LEVEL=INFO \
	PREFECT_LOGGING_LOGGERS_PREFECT_EXTRA_LEVEL=INFO \
	PREFECT_LOGGING_TO_API_WHEN_MISSING_FLOW='ignore' \
	$(1)


demo:
	-rm .env
	$(call SET_ENV, uv run --with-requirements requirements.txt -p python3.10 python silly_flow.py)

demo2:
	-rm .env
	$(call SET_ENV, uv run --with-requirements requirements.txt -p python3.10 python silly_flow.py)

env_bug_file:
	echo PREFECT_LOGGING_EXTRA_LOGGERS=jds > .env
	echo PREFECT_LOGGING_LEVEL=INFO  >> .env
	echo PREFECT_LOGGING_LOGGERS_PREFECT_EXTRA_LEVEL=INFO  >> .env
	echo PREFECT_LOGGING_TO_API_WHEN_MISSING_FLOW='ignore'  >> .env
	uv run --with-requirements requirements.txt -p python3.10 prefect config view --show-sources | grep LOG
	uv run --with-requirements requirements.txt -p python3.10 python env_bug.py 

env_bug_env:
	-rm .env
	$(call SET_ENV, uv run --with-requirements requirements.txt -p python3.10 prefect config view --show-sources) | grep LOG
	$(call SET_ENV, uv run --with-requirements requirements.txt -p python3.10 python env_bug.py)

clean:
	uv cache clean


versions:
	uv run --with-requirements requirements.txt -p python3.10 prefect version

