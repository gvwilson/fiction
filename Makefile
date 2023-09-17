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

## chapters: make a release
.PHONY: chapters
ifeq (${book},)
chapters:
	@echo "'book' not defined"
else
chapters:
	@python bin/chapters.py $${book}/index.md
endif
