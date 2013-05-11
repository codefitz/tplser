# tplser

## Version

0.08 (alpha)

## Description

A TPL pattern language parser for BMC's Atrium Discovery and Dependency Mapping (ADDM).

Code is still alpha so...
- Parsing works, but it won't catch everything, you may still be caught out when it comes to uploading to your appliance.
- Parser treats all variables embedded in if blocks as potential uninitialised variables so you will get a warning for `var` in code like this:

```
    if true then
        var := true;
    else
        var := false;
    end if;
    
    something := var;
```

Even though `something` will still be assigned `var`, ADDM will not warn you(?), but the parser will - just in case. It's not a bug and so will not be treated as something to fix right now.

---

This program is provided under an Apache license and does not contain code from ADDM, the TKU or any other software belonging to BMC or its partners or customers. It works independently of ADDM and is designed for use with TPL pattern language files only.

## Usage

To run:

```
$ python tplser.py file.tpl
```

## Updates

### Alpha

0.08 - Fixed imports on multiple lines, improved uninitialised variable matching.<br>
0.07 - Added warnings for uninitialised variables (inside of if block)<br>
0.06 - Added fileInfo, listDirectory, registryKey, definitions to summary. Now evaluates list of definition variables correctly.<br>
0.05 - Added exception handling for declarations (ignore variables for now). Added more secion header identification. Started on syntax recognition for variables.<br>
0.04 - Committed to GitHub.

## Development

### Works:

* IF evaluation parsing
* FOR loop parsing
* Summary (counts of statements)
* Checks for initialised variables
* Identifies and checks for integrity of section headers (required/missing declarations)
* Rudimentary file handling
* Uninitialised variable warnings (if blocks)

### Getting to Work:

* Section headers: simple identities, business application instances
* Individual statement syntax: typos, keywords, search, line declarations (e.g. regex extracts)
* Code clean-up and OO optimisation
* Uninitialised variable warnings (for blocks)

### Nice To Have:

* TPL versioning
* TPL Best practice suggestions
* Check imported tpl syntax (external tpl)

## Licensing

Apache 2.0 License - see LICENSE file.
