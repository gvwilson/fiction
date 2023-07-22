# By default, show available commands (by finding '##' comments).
.DEFAULT: commands

## commands: show available commands
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} \
	| sed -e 's/## //g' \
	| column -t -s ':'

## status: create table showing status
status:
	@python bin/status.py --info _data/info.csv --status _data/status.csv
