# tplser

## Version

0.1.3 (alpha)

## Description

A TPL pattern language parser for BMC's Atrium Discovery and Dependency Mapping (ADDM). Developed with Python 2.6, 2.7

Code is still alpha so...
- PDB debugging enabled, to run the script normally, press "c" + [Enter] at the `(Pdb)` prompt.
- Parsing works, but it won't catch everything, you may still be caught out when it comes to uploading to your appliance.

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

### Getting to Work:

* Section headers: simple identities, business application instances
* Syntax: typo catching
* keyword checking
* table syntax
* discovery function syntax
* search syntax
* Uninitialised variable warnings (for blocks)
* Code clean-up and OO optimisation
* CMDB cdm patterns
* Needs function for splitting up of text strings and variable declarations for accidental false positive matches

### Nice To Have:

* TPL versioning
* TPL Best practice suggestions
* Check imported tpl syntax (external tpl)
* Handle packages with multiple tpl files
* GUI

## Licensing

Apache 2.0 License - see LICENSE file.

## Updates

### Alpha

| Release | Version | Description |
| --- | --- | --- |
| Alpha | 0.1.3 | Added PDB debugging.<br>Fixed further issues with assigned/uninitialised variables.<br>Fixed syntax error matching bugs.<br>Basic string checking added.<br>Simple Identities count added to summary. Bug fixes. |
| Alpha | 0.1.2 | Fixed issues with if evaluation blocks - should now be working as expected.<br>Parser handles variables declared after an 'else' statement, meaning no warning. |
| Alpha | 0.1.1 | Added support for older versions of python for args check.<br>Improved import parsing code.<br>Small improvements to syntax checking.<br>Improved code for uninitialised variable warning.<br>Added TPL version to summary. |
| Alpha | 0.1.0 | Improved matching variables inside brackets.<br>Fixed parsing of `end if;` statement where there is whitespace between `end if` and `;`.<br>Added regex parsing for `text` functions. |
| Alpha | 0.0.9 | Fixed issue where "notes" field on one line throws out section evaluations.<br>Added syntax check for trigger statement. |
| Alpha | 0.0.8 | Fixed imports on multiple lines, improved uninitialised variable matching. |
| Alpha | 0.0.7 | Added warnings for uninitialised variables (inside of if block) |
| Alpha | 0.0.6 | Added fileInfo, listDirectory, registryKey, definitions to summary.<br>Now evaluates list of definition variables correctly. |
| Alpha | 0.0.5 | Added exception handling for declarations (ignore variables for now).<br>Added more secion header identification.<br>Started on syntax recognition for variables. |
| Alpha | 0.0.4 | Committed to GitHub. |
