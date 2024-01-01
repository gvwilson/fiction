# By default, show available commands (by finding '##' comments).
.DEFAULT: commands

## commands: show available commands
.PHONY: commands
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} \
	| sed -e 's/## //g' \
	| column -t -s ':'

## build: rebuild site
.PHONY: build
build:
	@jekyll build

## serve: run a local server
.PHONY: serve
serve:
	@jekyll serve

## status: create table showing status
.PHONY: status
status:
	@python bin/status.py --chart status.svg --info _data/info.csv --status _data/status.csv

## count: count words
.PHONY: count
ifeq (${book},)
count:
	@echo "'book' not defined"
else
count:
	@python bin/count.py --details $${book}/index.md ${base}
endif

## spell: check spelling
.PHONY: spell
ifeq (${book},)
spell:
	@echo "'book' not defined"
else
spell:
	aspell list < ${book}/index.md | python bin/diffset.py - ${book}/words.txt
endif
