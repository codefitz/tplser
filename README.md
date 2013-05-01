# tplser

## Version

0.04 Alpha

## Description

A tpl pattern language parser for BMC's Atrium Discovery and Dependency Mapping (ADDM).

Code is partially complete - most of it works, but will misidentify some syntax, please feel free to fork and contribute.

## Usage

To run:
    $ ./tplser.py file.tpl

## Updates

0.04 - Committed to GitHub.

## Development

### Works

* IF evaluation parsing
* FOR loop parsing
* Summary (counts of statements)
* Section headers: module, metadata, imports, tables, log statements, discovery commands, software instances, details, pattern, dev notes, overview, tags, constants, triggers
* Checks for unitialised variables (misidentifies definitions)

### To Implement

* Section headers: definitions, configurations, simple identities, business application instances
* Individual statement syntax: typos, keywords, search, line declarations (e.g. regex extracts)
* Code clean-up and OO optimisation

### Nice To Have and Feature Requests

* TPL versioning
* TPL Best practice suggestions
