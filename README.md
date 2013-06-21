# tplser

## Version

0.1.8 (alpha)

## Description

A TPL pattern language parser for BMC's Atrium Discovery and Dependency Mapping (ADDM). Developed with Python 2.6, 2.7

Code is still alpha so...
- PDB debugging enabled, to run the script normally, press "c" + [Enter] at the `(Pdb)` prompt.
- Parsing is working for items listed, but may still be subject to some bugs and not everything is checked - please submit an issue with sample TPL in order to prioritise fix/implementation.

---

This program is provided under an Apache license and does not contain code from ADDM, the TKU or any other software belonging to BMC or its partners or customers. It works independently of ADDM and is designed for use with TPL pattern language files only.

## Usage

To run:

```
$ python tplser.py file.tpl
```

## Development

### Works:

* IF evaluation parsing
* FOR loop parsing
* Summary (counts of statements)
* Checks for initialised variables
* Identifies and checks for integrity of section headers (required/missing declarations)
* Rudimentary file handling
* Uninitialised variable warnings
* Trigger syntax
* If statement handling of else/elif on uninitialised variables
* ECA error check for concatenation of strings in a log statement
* Invocations after a `stop;`

### Will Eventually Work:

* Section headers: simple identities, business application instances
* Syntax: typo catching
* keyword checking
* table syntax
* discovery function syntax
* search syntax
* Code clean-up and OO optimisation
* CMDB cdm patterns
* Syntax causing ECA errors
* Remove superfluous characters warning

### Nice To Have:

* TPL versioning
* TPL Best practice suggestions
* Check imported tpl syntax (external tpl)
* Handle packages with multiple tpl files
* GUI
* Check for node syntax that require an attribute to output

## Licensing

Apache 2.0 License - see LICENSE file.

## Updates

### Alpha

| Release | Version | Description |
| --- | --- | --- |
| Alpha | 0.1.8 | Some more code cleanup and modules added.<br>Fixed false positive matches where mixed apostrophe/quotes used in line. |
| Alpha | 0.1.7 | Moved regexes to compile functions in order to simplify code and eliminate duplication. |
| Alpha | 0.1.6 | Bug fixes.<br>New code to evaluate multiple conditions in trigger statement. |
| Alpha | 0.1.5 | Check for syntax that would cause ECA Error - concatenation in a log statement.<br>Checks for invocations after a stop.<br>Fixed bug with configuration variable being assigned 0 length string.<br>Fixed imports not added to variable list. |
| Alpha | 0.1.4 | Exported functions to modules.<br>Corrected variable assignment count summary.<br>More bugfixes for syntax checking. |
| Alpha | 0.1.3 | Added PDB debugging.<br>Fixed further issues with assigned/uninitialised variables.<br>Fixed syntax error matching bugs.<br>Basic string checking added.<br>Simple Identities count added to summary. Bug fixes.<br>Parser handles variables declared after an 'else' statement, meaning no warning. |
| Alpha | 0.1.2 | Fixed issues with if evaluation blocks - should now be working as expected. |
| Alpha | 0.1.1 | Added support for older versions of python for args check.<br>Improved import parsing code.<br>Small improvements to syntax checking.<br>Improved code for uninitialised variable warning.<br>Added TPL version to summary. |
| Alpha | 0.1.0 | Improved matching variables inside brackets.<br>Fixed parsing of `end if;` statement where there is whitespace between `end if` and `;`.<br>Added regex parsing for `text` functions. |
| Alpha | 0.0.9 | Fixed issue where "notes" field on one line throws out section evaluations.<br>Added syntax check for trigger statement. |
| Alpha | 0.0.8 | Fixed imports on multiple lines, improved uninitialised variable matching. |
| Alpha | 0.0.7 | Added warnings for uninitialised variables (inside of if block) |
| Alpha | 0.0.6 | Added fileInfo, listDirectory, registryKey, definitions to summary.<br>Now evaluates list of definition variables correctly. |
| Alpha | 0.0.5 | Added exception handling for declarations (ignore variables for now).<br>Added more secion header identification.<br>Started on syntax recognition for variables. |
| Alpha | 0.0.4 | Committed to GitHub. |
