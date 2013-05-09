# tplser

## Version

0.07 (alpha)

## Description

A TPL pattern language parser for BMC's Atrium Discovery and Dependency Mapping (ADDM).

Code is stil alpha - parsing works, but it won't catch everything, you may still be caught out when it comes to uploading to your appliance.

This program is provided under an Apache license and does not contain code from ADDM, the TKU or any other software belonging to BMC or its partners or customers. It works independently of ADDM and is designed for use with TPL pattern language files only.

## Usage

To run (Linux):

    $ ./tplser.py file.tpl

To run (Windows):

    $ python tplser.py file.tpl

## Updates

### Alpha

0.07 - Added warnings for uninitialised variables (inside of if block)<br>
0.06 - Added fileInfo, listDirectory, registryKey, definitions to summary. Now evaluates list of definition variables correctly.<br>
0.05 - Added exception handling for declarations (ignore variables for now). Added more secion header identifaction. Started on syntax recognition for variables.<br>
0.04 - Committed to GitHub.

## Development

### Works:

* IF evaluation parsing
* FOR loop parsing
* Summary (counts of statements)
* Checks for itialised variables
* Identifies and checks for integrity of section headers (required/missing declarations)
* Rudimentary file handling
* Uninitialised variable warnings (if blocks)

### Doesn't Do Yet:

* Section headers: simple identities, business application instances
* Individual statement syntax: typos, keywords, search, line declarations (e.g. regex extracts)
* Code clean-up and OO optimisation
* Uninitialised variable warnings (for blocks)

### Nice To Have and Feature Requests:

* TPL versioning
* TPL Best practice suggestions
* Check imported tpl syntax (external tpl)

## Licensing

Apache 2.0 License - see LICENSE file.
