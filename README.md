# tplser

## Version

0.05 (alpha)

## Description

A TPL pattern language parser for BMC's Atrium Discovery and Dependency Mapping (ADDM).

Code is stil alpha - parsing works, but it won't catch everything, you may still be caught out when it comes to uploading to your appliance.

## Usage

To run:

    $ ./tplser.py file.tpl

## Updates

0.05 - Added exception handling for declarations (ignore variables for now). Added more secion header identifaction. Started on syntax recognition for variables.<br>
0.04 - Committed to GitHub.

## Development

### Works:

* IF evaluation parsing
* FOR loop parsing
* Summary (counts of statements)
* Checks for unitialised variables
* Identifies and checks for integrity of section headers (required/missing declarations)
* Rudimentary file handling

### Doesn't Do Yet:

* Section headers: simple identities, business application instances
* Individual statement syntax: typos, keywords, search, line declarations (e.g. regex extracts)
* Code clean-up and OO optimisation

### Nice To Have and Feature Requests:

* TPL versioning
* TPL Best practice suggestions

## Licensing

Apache 2.0 License - see LICENSE file.
