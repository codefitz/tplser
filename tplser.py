#!/usr/bin/env python
#
# Version 0.1.4 (alpha)
#
# Author: Wes Fitzpatrick (github@wafitz.net)
#
# Source: 
# http://github.com/codefitz/tplser
#

# Local modules
from tplser import *

# Standard modules
import pdb
import re
import sys

pyver = sys.version_info

if pyver >= (2,7,0):
    import argparse
    parser = argparse.ArgumentParser()
    tpl_file = tplfile.tplfile
    parser.add_argument('*.tpl', type=tpl_file)
    args = parser.parse_args()
else:
    if len(sys.argv) < 2:
        sys.exit("You must specify a *tpl file!\n")

print "\nNow parsing " + str(sys.argv[1]) + "...\n"

parsing, rev_parsing, patt_parse, rev_patt_parse, tpl_parsing, fwd = [False] * 6
pattern_name = ""

#pdb.set_trace()

with open(sys.argv[1]) as tpl_file:

    ##########################
    #== Read Lines Forward ==#
    ##########################

    module_num, endpattern_num, pattern_num, line_num, body_num, endbody_num, if_block = [0]*7
    patt_eval, if_eval, for_eval, ov_eval, trig_eval, body_eval, meta_eval, table_eval, config_eval, defins_eval, warn_count = [0]*11
    logs, runcmds, filegets, open_notes, comments, sis, details, imported, listdirs, fileinfos, regkeys = [0]*11
    if_count, endif_count, for_count, endfor_count, ov_count, endov_count, trig_count, endtrig_count, table_count, unterminated_count, define_count = [0]*11
    ov_err, endov_err, tags_err, trig_err, endtrig_err, trig_on_err, endtable_count, sids_err = [0]*8
    patt_err, if_err, for_err, body_err, table_err, sid_err = ([] for i in range(6))
    lines, mod_line = ([] for i in range(2))
    ov_pattern, trig_pattern = ([] for i in range(2))
    missing_trig, missing_endtrig, missing_trigon = ([] for i in range(3))
    has_trigger, has_ov, initlist, used, imports, unterminated, var_warn, warn_list, for_warn_list, syntax_errs = ([] for i in range(10))
    missing_ov, missing_endov, missing_tags, missing_sid, missing_sids = ([] for i in range(5))
    ov_tags, trig_on, ignore_text, constants, defins, open_bracket = [False]*6
    config_var, defins_var, ob_line, trig_line, import_line, var_line = [""]*6
    end_imports, trigger = [False]*2
    assign_eval, var_warning, else_clause, sid_tags, for_block, open_assignment = [False]*6
    sid_eval, sid_count, endsid_count, sid_found = [0]*4
    has_sid = []

    # For storing custom variables declared in pattern, predefined keywords added here:
    global_vars, varlist = ([ 'model', 'regex', 'discovery', 'search', 'table', 'time', 'false', 'true', 'process', 'function', 'sql_discovery', 'size', 'number', 'xpath', 'none', 'raw', 'expand', 'vsphere_discovery', 'from_id', 'vcenter_discovery', 'in' ] for i in range(2))
    # temporary fix to get correct number in summary
    keywords = len(global_vars)

    for full_line in tpl_file:
        lines.append(full_line.strip())
        line_num += 1
        fwd = True
        
        # Count of comments
        if re.match("^\s*//", full_line):
            comments += 1
        
        # Strip comments
        if "//" in full_line:
            values = re.findall("[\"\'].*[\"\']", full_line)
            if values: # if "//" is not a comment
                for val in values:
                    if "//" in val:
                        line = full_line
                    else:
                        line = full_line.split("//")[0]
            else:
                line = full_line.split("//")[0]
        else:
            line = full_line

		# Ignore developer notes block
        if re.match("^\s*[\"\'][\"\'][\"\']", line):
            if open_notes > 0:
                ignore_text = False
                open_notes -= 1
            else:
                ignore_text = True
                open_notes += 1
            if re.search("[\"\'][\"\'][\"\'].*[\"\'][\"\'][\"\']", line):
                ignore_text = False
                open_notes -= 1

        if ignore_text:
            continue
		
        if not ignore_text:

            # Module Evaluation
            if re.match("tpl\s\d\.\d\smodule\s\S+;", line):
                module_num += 1
                mod_line.append(str(line_num) + ": " + line)
                tpl_ver = re.match("tpl\s+(\d+\.\d)", line).group(1)

            # Metadata Evaluation
            if re.match("^\s*metadata\s*$", line):
                meta_eval += 1
        
            if re.match("^\s*end\smetadata;", line):
                meta_eval -= 1

            # Imports - Join all import lines
            end_imports = False
            import_dec = re.search("^\s*from\s+\S+\s+import\s+(\w+)", line)
            if import_dec:
                imported += 1
                import_ln = line_num
                import_line = line
                if not ";" in import_line:
                    import_line += " " + str.strip(line)
                else:
                    end_imports = True

            # Import line complete, get all variables
            if end_imports:
                import_vars = re.findall("(\w+)\s+\d+\.\d", import_line)
                for var in import_vars:
                    global_vars.append(var)

            # Table evaluations
            table = re.search("^\s*table\s+\w+\s+\d+\.\d", line)
            if table:
                tab_var = re.search("^\s*table\s+(\w+)\s+\d+\.\d", line).group(1)
                global_vars.append(tab_var)
                table_count, table_eval = sections.open_match(table_count, table_eval)

            end_table = re.search("^\s*end\stable;", line)
            if end_table:
                endtable_count, table_eval = sections.close_match(endtable_count, table_eval)
                table_eval = loops.loop_eval(table_eval, table_err, line_num)

            # Configuration evaluation
            config = re.search("^\s*configuration\s+\w+\s+\d+\.\d", line)
            if config:
                config_eval += 1
                config_var = re.match("^\s*configuration\s+(\w+)\s+\d+\.\d", line).group(1)
                global_vars.append(config_var)
                tpl_parsing = True

            end_config = re.search("^\s*end\sconfiguration;", line)
            if end_config:
                config_eval -= 1
                tpl_parsing = False

            # Definitions evaluation
            definitions = re.search("^\s*definitions\s+\w+\s+\d+\.\d", line)
            if definitions:
                defins = True
                defins_eval += 1
                defins_var = re.match("^\s*definitions\s+(\w+)\s+\d+\.\d", line).group(1)
                if defins_var:
                    global_vars.append(defins_var)
                tpl_parsing = True

            end_defins = re.search("^\s*end\sdefinitions;", line)
            if end_defins:
                defins = False
                defins_eval -= 1
                tpl_parsing = False

            # Definition statements
            if defins:
                define = line
                define_var = re.search("^\s*define\s+(\w+)\(", define)
                if define_var:
                    define_count += 1
                    def_vars = re.search("\((.*)\)", define)
                    def_returns = re.search("->\s*(.*)\s*$", define)
                    if def_vars:
                        split_def = str(def_vars.group(1)).split(',')
                        for split_var in split_def:
                            var = str.strip(split_var)
                            global_vars.append(var)
                    if def_returns:
                        split_return = str(def_returns.group(1)).split(',')
                        for split_var in split_return:
                            var = str.strip(split_var)
                            global_vars.append(var)

            # Count of logs
            if re.match("\s*log\.\w+\(", line):
                logs += 1
            
            # Count of run commands
            if re.search("\s*discovery\.runCommand\(", line):
                runcmds += 1

            # Count of filegets
            if re.search("\s*discovery\.fileGet\(", line):
                filegets += 1
            
            # Count of listdirs
            if re.search("\s*discovery\.listDirectory\(", line):
                listdirs += 1
            
            # Count of file infos
            if re.search("\s*discovery\.fileInfo\(", line):
                fileinfos += 1

            # Count of registry key lookups
            if re.search("\s*discovery\.registryKey\(", line):
                regkeys += 1
                
            # Count of SIs
            if re.search("\s*model\.SoftwareInstance\(", line):
                sis += 1

            # Count of Details
            if re.search("\s*model\.Detail\(", line):
                details += 1

            # Count of simple ids
            if re.match("\s*identify\s+", line):
                sid_count, sid_eval, has_sid, sid_tags = attributes.open_requireds(pattern_name, line, sid_count, sid_eval, has_sid, sid_tags)
            
            # Count of simple ids
            if sid_eval > 0:
                if "simple_identity;" in line:
                    pass # guide line
                elif "->" in line:
                    sid_found += 1

            if re.search("^\s*end\s*identify;", line):
                endsid_count, sid_eval, missing_sid, sid_err, missing_sids, sids_err = attributes.close_requireds(
                    pattern_name, line, endsid_count, sid_eval, missing_sid, sid_err, sid_tags, missing_sids, sids_err)
            
            trig_complete = False

            if trig_eval > 0:
                trig_ln = line_num
                if not ";" in trig_line:
                    trig_line += " " + str.strip(line)
                else:
                    trig_complete = True

            if trig_complete:
                if "created" in trig_line or "confirmed" in trig_line:
                    trig_trim = trig_line.replace("created", "")
                    trig_trim = trig_trim.replace("confirmed", "")
                    trig_trim = trig_trim.replace(",", "")
                else:
                    trig_trim = trig_line

                trig_statement = re.search("^\s*on\s+\w+\s+:=\s*(\w+)\s+\w+\s+\(?\w+\s+(\S+)(\s+\w+)?\s*[\"\']", trig_trim)

                if not trig_statement:
                    trig_statement = re.search("^\s*on\s+\w+\s+:=\s*(\w+)\s*;", trig_trim)
                
                if not trig_statement:
                    syntax_errs.append(str(trig_ln) + ": " + str.strip(trig_line))

            # Pattern evaluation
            pattern_name, pattern_num, endpattern_num, patt_eval, patt_parse, patt_err, pattern_list = pattern.pattern_parse(
                pattern_name, fwd, line, pattern_num, endpattern_num, patt_eval, patt_parse, patt_err, line_num)

        # If inside pattern
        if patt_parse:

            # Overview evaluation
            if re.match("^\s*overview\s*$", line):
                ov_count, ov_eval, has_ov, ov_tags = attributes.open_requireds(pattern_name, line, ov_count, ov_eval, has_ov, ov_tags)

            # Count of tags
            if re.match("\s*tags\s+\S+", line):
                ov_tags = True

            if re.search("^\s*end\soverview;", line):
                endov_count, ov_eval, missing_ov, ov_err, missing_tags, tags_err = attributes.close_requireds(
                    pattern_name, line, endov_count, ov_eval, missing_ov, ov_err, ov_tags, missing_tags, tags_err)

            # Constants
            if re.match("^\s*constants\s*$", line):
                constants = True

            # This is just a quick var grab, we're not checking the integrity of constants right now
            if constants and re.search("\S+\s*:=", line):
                global_vars.append(re.search("(\S+)\s*:=", line).group(1))

            if re.match("^\s*end\sconstants;", line):
                constants = False

            # Trigger evaluation
            if re.match("^\s*triggers\s*$", line):
                trig_count, trig_eval, has_trigger, trig_on = attributes.open_requireds(pattern_name, line, trig_count, trig_eval, has_trigger, trig_on)

            # Check for trigger condition
            if re.match("\s*on\s+\S+\s*:=", line):
                trig_on = True
                global_vars.append(re.search("(\S+)\s*:=", line).group(1))

            if re.search("^\s*end\striggers;", line):
                endtrig_count, trig_eval, missing_trig, trig_err, missing_trigon, trig_on_err = attributes.close_requireds(
                    pattern_name, line, endtrig_count, trig_eval, missing_trig, trig_err, trig_on, missing_trigon, trig_on_err)

            # Body evaluation
            body_num, endbody_num, body_eval, parsing, body_err = body.body_parse(
                fwd, line, body_num, endbody_num, body_eval, parsing, body_err, line_num)

            # If inside body
            if parsing:

                # Check end ov
                ov_eval, missing_endov, endov_err = attributes.closing_decs(ov_eval, missing_endov, pattern_name, endov_err)
                # Check end trigger
                trig_eval, missing_endtrig, endtrig_err = attributes.closing_decs(trig_eval, missing_endtrig, pattern_name, endtrig_err)

                # Set general TPL parsing
                tpl_parsing = True

            else:
                tpl_parsing = False
                # Reset variables warnings based on if evaluations
                if_block = 0
                warn_list = []
                else_clause = False

        # General TPL parsing for Definitions and Body
        if tpl_parsing:
        
            # Check IF evaluations
            if re.match("^\s*if\s+", line):
                if_count, if_eval = sections.open_match(if_count, if_eval)
            if re.match("^\s*end\sif\s*;", line):
                endif_count, if_eval = sections.close_match(endif_count, if_eval)
                if_eval = loops.loop_eval(if_eval, if_err, line_num)
            # Check FOR evaluations
            if re.match("^\s*for\s.*do", line):
                for_count, for_eval = sections.open_match(for_count, for_eval)
            if re.match("^\s*end\sfor\s*;", line):
                endfor_count, for_eval = sections.close_match(endfor_count, for_eval)
                for_eval = loops.loop_eval(for_eval, for_err, line_num)

            ############################
            # Variable initialisations #
            ############################
            
            var_ln = line_num
            
            # For warning variables inside of if evaluations
            if if_eval == 1 and re.match("^\s*if\s+", line):
                if_block += 1
                #print "if_block " + str(if_block) + ": " + str(line)
                #print ("pattern: " + str(pattern_name) + ", if_block: " + str(if_block))
             
            if if_eval == 1 and re.match("^\s*else\s*$", line):
                else_clause = True
            
            if ";" in line:
                #print line
                open_assignment = False
                
                # Check line syntax errors
                no_quotes = re.sub("[\"']([^\']*)[\"']", "", line)
                #print no_quotes
                #print "================="
                if re.search("^\s*\S+\s*=",no_quotes): # missing colon (:)
                    syntax_errs.append(str(line_num) + ": " + str.strip(line))
                        
            if ":=" in line:
                open_assignment = True
            
            if config_var in line:
                conf = re.compile("%s\.(\w+)"%config_var)
                var = re.search(conf, line)
                if var:
                    used.append(var.group(1))

            if open_assignment and not ";" in line:
                #print "line " + str(var_ln) + " ';' not found"
                if re.search("^\s*if.*then\s*$", line):
                    var_declared = True
                else:
                    #print "line " + str(var_ln) + ": " + str(var_line)
                    var_line += " $" + str(line_num) + "$ " + str.strip(line)
                    var_declared = False
            else:
                open_assignment = False
                var_line += line
                var_declared = True

            if var_declared:
            
                # var_line clean
                if re.match("^\s*\$\d+\$", var_line):
                    var_line = re.match("^\s*\$\d+\$(.*)", var_line).group(1)
                    #print "line " + str(var_ln) + ": " + str(var_line)
                
                assigner = var_line.count(':=')
                
                # Getting string between "/'  characters
                quotes = re.findall("[\"']([^\"']*)[\"']", var_line)
                if quotes:
                    for quote in quotes:
                        if ":=" in quote:
                            assigner -= 1 # Remove an := chars between quotes
                
                # Check to see if it belongs to a function, multiple assigners are expected
                if assigner > 1:
                    if re.search("^\s*log\.", var_line):
                        pass
                    elif re.search("^\s*list\.", var_line):
                        pass
                    elif re.search("^\s*xpath\.", var_line):
                        pass
                    elif re.search("(^|:=)\s*model\.", var_line):
                        pass
                    elif re.search("^\s*inference\.", var_line):
                        pass
                    elif re.search("no_match\s*:=", var_line):
                        pass
                    elif re.search(":=\s*time\.", var_line):
                        pass
                    else:
                        #print "line " + str(var_ln) + ": " + str(var_line)
                        #print "=========================================="
                        syntax_errs.append(str(var_ln) + ": " + str.strip(var_line))
                
                # Get variables assigned
                
                var = ""
                #print "line " + str(var_ln) + ": " + str(var_line)
                if re.search("^\s*\S+\s*:=", var_line):
                    var = re.search("^\s*(\S+)\s*:=", var_line).group(1)
                    #print ("var = " + str(var) + " (" + str(var_ln) + ")")
                    if "." in var:
                        var = re.search("^\s*(\S+)\.", var_line).group(1)
                    varlist.append(var)
                    #print "appended " + str(var) + " to varlist (" + str(var_ln) + ")"

                if re.search("^\s*for\s*\w+\s*in", var_line):
                    var = re.search("^\s*for\s*(\w+)\s*in", var_line).group(1)
                    for_block = True
                    varlist.append(var)

                if var:
                    # Check if variable has already been declared, if not then it is a genuine warning
                
                    if (if_eval > 0) and not else_clause and not for_block:
                        warn = if_block, var
                        #print ("assigning warn var = " + str(warn) + " (" + str(var_ln) + ")")
                        warn_list.append(warn)
                        for_block = False
                    else:
                        global_vars.append(var)
                        #print ("assigning global var = " + str(var) + " (" + str(var_ln) + ")")

                ######################
                # Variables utilised #
                ######################
                
                in_brackets = re.search("\((.*)\)", var_line)
                
                # Handle multiple assignments such as in model declarations
                if in_brackets:
                    vars = re.findall(":=\s*(\w+),?", in_brackets.group(1))
                    for var in vars:
                        if re.search("%\w+%", var):
                            subs = re.findall("%(\w+)%", var) # multiple substitutions
                            if subs:
                                for sub in subs:
                                    used.append(sub)
                        else:
                            used.append(var)
                            
                    # Handle embedded functions and quotes
                    embed_line = re.sub("[\"']([^\']*)[\"']", "", var_line)
                    embed_line = re.sub("[\"']([^\"]*)[\"']", "", embed_line)
                    embeds = embed_line.count('(')
                    if re.search("(^|:=)\s*model\.", var_line):
                        pass
                    elif re.search("^\s*log\.", var_line):
                        pass
                    elif embeds > 0:
                        vars = re.findall("\(\s*(\w+),?", embed_line)
                        for var in vars:
                            if var == "text":
                                pass # text function
                            elif var == "not":
                                pass # not evaluation
                            else:
                                used.append(var)

                if re.search(":=\s*(regex\.extract|discovery.*)\s*\((\w+),", var_line):
                    cond = re.search("\((\w+),", var_line).group(1)
                    if "[" in cond:
                        used.append(re.search("(\w+)\[", cond).group(1))
                    if "." in cond:
                        used.append(re.search("(\w+)\.", cond).group(1))
                    else:
                        used.append(cond)

                    subs = re.search("\(\S+\s*,\s*(\w+)\);", var_line) # Substitution vars
                    if subs:
                        used.append(subs.group(1))

                if re.search("%\w+%", line):
                    used.append(re.search("%(\w+)%", line).group(1))

                if re.search("^\s*model\.\w+\(\w+\);", var_line):
                    used.append(re.search("^\s*model\.\w+\((\w+)\);", var_line).group(1))

                if re.search("^\s*list\.", var_line):
                    var = re.search("\(\s*(\w+)?,", var_line).group(1)
                    if "[" in var:
                        used.append(re.search("(\w+)?,\[", var_line).group(1))
                    else:
                        used.append(var)
                    
                    subs = re.search("\(\S+\s*,\s*(\w+)\);", var_line)
                    if subs:
                        used.append(subs.group(1))

                if re.search(":=\s*(\w+)\+?.*[;,]", var_line):
                    var = re.search(":=\s*(\w+)\+?.*[;,]", var_line).group(1)
                    if var == defins_var:
                        pass
                    elif var == "text":
                        if "%" in line:
                            var = re.search("%(\S+)%", var_line).group(1)
                            if "." in var:
                                used.append(re.search("(\w+)\.", var).group(1))
                            else:
                                used.append(var)
                        #else:
                            #used.append(re.search(":=\s*text\.\w+\(\s*(\w+)\+?.*[;,]", var_line).group(1))
                    else:
                        used.append(re.search(":=\s*(\w+)\+?.*[;,]", var_line).group(1))

                if re.search("\.(result|content)", var_line):
                    used.append(re.search("(\w+)\.(result|content)", var_line).group(1))

                if re.search("^\s*for\s*\S+\s+in\s+\w+", var_line):
                    cond = re.search("^\s*for\s*\S+\s*in\s*(\w+)", var_line).group(1)
                    if "(" in cond:
                        used.append(re.search("\((\S+),", cond).group(1))
                    elif "." in cond:
                        used.append(re.search("(\w+)\.", cond).group(1))
                    elif "[" in cond:
                        used.append(re.search("(\w+)\[", cond).group(1))
                        used.append(re.search("\[(\w+)", cond).group(1))
                    elif cond == "text":
                            #print "line " + str(var_ln) + ": var = " + str(cond)
                            cond = re.findall("^\s*if\s+text\.\w+\((\w+)", var_line)
                            for var in cond:
                                used.append(var)
                    else:
                        used.append(cond)

                if re.search("^\s*if\s+(not\s+)?", var_line):
                    if re.search("^\s*if\s+(size)?\(?(not\s+)?(\w+)(?<!\))", var_line):
                        cond = re.search("^\s*if\s+(size)?\(?(not\s+)?(\w+)(?<!\))", var_line).group(3)
                        if "." in cond:
                            used.append(re.search("(\w+)\.", cond).group(1))
                        elif "[" in cond:
                            used.append(re.search("(\w+)\[", cond).group(1))
                            used.append(re.search("\[(\w+)", cond).group(1))
                        elif cond == "not":
                            if re.search("^\s*if\s*\(\s*not\s*\(\s*(\w+)", var_line):
                                cond = re.search("^\s*if\s*\(\s*not\s*\(\s*(\w+)", var_line).group(1)
                                used.append(cond)
                        elif cond == "text":
                            #print "line " + str(var_ln) + ": var = " + str(cond)
                            cond = re.findall("^\s*if\s+text\.\w+\((\w+)", var_line)
                            for var in cond:
                                used.append(var)
                        else:
                            used.append(cond)

                    has_substring = re.search("has\s*substring\s*(\w+)", var_line)
                    if has_substring:
                        used.append(has_substring.group(1))

                    matches_regex = re.search("matches\s+regex\s*(\w+)", var_line)
                    if matches_regex:
                        used.append(matches_regex.group(1))

                    or_or = re.match("(?:(\".*)|\s+or\s+(\w+))", var_line)
                    if or_or:
                        used.append(or_or.group(2))
                        
                    if_quotes = re.sub("[\"']([^\"']*)[\"']", "", var_line)
                    if if_quotes:
                        pass
                    else:
                        and_and = re.search("\s+and\s+(not\s+)?(\w+)", var_line)
                        if and_and:
                            used.append(and_and.group(2))

                    equals = re.search("=\s*(\w+)", var_line)
                    if equals and equals.group(1) == "text":
                        equals = re.search("=\s+text\.\w+\((\w+)", var_line)

                    if equals:
                        used.append(equals.group(1))

                    not_in = re.search("not\s+in\s+(\w+)", var_line)
                    if not_in:
                        used.append(not_in.group(1))
                
                for var in used:
                    #print "var used: " + str(var) + " (" + str(var_line) + ")"
                    # Get actual line number
                    if assigner > 1:
                        in_brackets = re.search("\((.*)\)", var_line)
                        if in_brackets:
                            get_ln = re.compile("\$(\d+)\$\s+\S+\s*:=\s*%s,?"%var)
                            if re.search(get_ln, var_line):
                                var_ln = re.search(get_ln, var_line).group(1)
                            # vars = re.findall(":=\s*(\S+),?", var_line)
                            # for index, value in enumerate(reversed(vars)):
                                # if value == var:
                                    # var_ln = line_num - index

                    if re.match("^[0-9]", var):
                        pass # Variable is a number
                            
                    # This fudge garauntees removal of any variables declared outside of an if/for loop
                    elif var not in global_vars:
                        #print ("var - " + str(var) + ", line " + str(var_ln) + ": " + str(var_line))
                        #print global_vars
                        #print "======================================"

                        if var not in varlist:
                            #print ("line " + str(var_ln) + ": " + str(var_line))
                            #print varlist
                            #print "======================================"
                            initlist.append(str(var_ln) + ": " + str(var))

                        # print warn_list
                        same_block = False
                        new_if_block = False
                        for warn in warn_list:
                            if var in warn:
                                block_no = warn[0]
                                #print warn
                                #print ("if_eval (" + str(if_eval) + "), for_eval (" + str(for_eval) + ")")
                                #print ("line " + str(var_ln) + ": " + str(var_line))
                                
                                if if_eval == 0:
                                    # This is to catch variables declared in an if group, called outside of the evaluation
                                    #print var
                                    #print "=========================================="
                                    var_warn.append(str(var_ln) + ": " + str(var))
                                
                                if (if_block == block_no):
                                    #print ("line " + str(var_ln) + ": " + str(var_line))
                                    # Var is in the same block
                                    #print ("if_block (" + str(if_block) + ") or for_block (" + str(for_block) + ") = block_no (" + str(block_no) + ")")
                                    same_block = True
                                
                                if (if_block > block_no):
                                    new_if_block = True

                        # this takes place outside of for loop as a var may be assigned twice but still be valid in the same
                        # block, so we have to check that it is both not the same block and that it is a new block
                        if not same_block and new_if_block:
                            #print "Not same block"
                            #print ("var warning: " + str(warn) + ", if_block = " + str(if_block) + ", for_block = " + str(for_block) + ", block_no = " + str(block_no))
                            #print ("line " + str(var_ln) + ": " + str(var_line))
                            #print warn_list
                            #print ("==========================================")
                            var_warn.append(str(var_ln) + ": " + str(var))

                var_line = ""
                var_declared = False
                used = []

    ###################################################
    #== Read Lines in Reverse (to get for/if loops) ==#
    ###################################################

    rev_endpattern_num, rev_pattern_num, rev_endbody_num, rev_body_num = [0]*4
    rev_if_count, rev_endif_count, rev_for_count, rev_endfor_count, rev_table_count, rev_endtable_count = [0]*6
    rev_patt_eval, rev_if_eval, rev_for_eval, rev_body_eval, rev_table_eval = [0]*5
    rev_patt_err, rev_if_err, rev_for_err, rev_body_err, rev_table_err = ([] for i in range(5))

    rev_line_num = line_num + 1

    lines.reverse()
    for row in lines:
        rev_line_num -= 1
        fwd = False

        if not ignore_text:

            # Table declarations
            end_table = re.search("^\s*end\stable;", row)
            if end_table:
                rev_endtable_count, rev_table_eval = sections.open_match(rev_endtable_count, rev_table_eval)

            table = re.search("^\s*table\s+\w+\s+\d+\.\d", row)
            if table:
                rev_table_count, rev_table_eval = sections.close_match(rev_table_count, rev_table_eval)
                rev_table_eval = loops.loop_eval(rev_table_eval, rev_table_err, rev_line_num)

            # Pattern evaluation
            pattern_name, rev_pattern_num, rev_endpattern_num, rev_patt_eval, rev_patt_parse, rev_patt_err, pattern_list = pattern.pattern_parse(
                pattern_name, fwd, row, rev_pattern_num, rev_endpattern_num, rev_patt_eval, rev_patt_parse, rev_patt_err, rev_line_num)

        # If inside pattern
        if rev_patt_parse:

            # Dev notes evaluation
            if re.match("^\s*[\"\'][\"\'][\"\']", row):
                if re.match("[\"\'][\"\'][\"\'].*[\"\'][\"\'][\"\']", row):
                    ignore_text = False
                if open_notes == 0:
                    ignore_text = True
                    open_notes += 1
                    continue
                else:
                    open_notes -= 1
                    ignore_text = False

            if ignore_text:
                continue

            # Body evaluation
            rev_body_num, rev_endbody_num, rev_body_eval, rev_parsing, rev_body_err = body.body_parse(
                fwd, row, rev_body_num, rev_endbody_num, rev_body_eval, rev_parsing, rev_body_err, rev_line_num)

            # If inside body
            if rev_parsing:

                # Check IF evaluations
                if re.match("^\s*end\sif\s*;", row):
                    rev_endif_count, rev_if_eval = sections.open_match(rev_endif_count, rev_if_eval)
                if re.match("^\s*if\s+", row):
                    rev_if_count, rev_if_eval = sections.close_match(rev_if_count, rev_if_eval)
                    rev_if_eval = loops.loop_eval(rev_if_eval, rev_if_err, rev_line_num)
                # Check FOR evaluations
                if re.match("^\s*end\sfor\s*;", row):
                    rev_endfor_count, rev_for_eval = sections.open_match(rev_endfor_count, rev_for_eval)
                if re.match("^\s*for\s.*do", row):
                    rev_for_count, rev_for_eval = sections.close_match(rev_for_count, rev_for_eval)
                    rev_for_eval = loops.loop_eval(rev_for_eval, rev_for_err, rev_line_num)

tpl_file.close()

if (module_num > 1):
    print (" * More than 1 module declaration in this file!")
    for mod_err in mod_line:
        print ("    line " + str(mod_err))
elif (module_num == 0):
    print (" * Something wrong with module declaration!")

evaluate.eval(meta_eval, "metadata")
evaluate.eval(config_eval, "configuration")
evaluate.eval(defins_eval, "definitions")

missing.missing_warn("overview", missing_ov, missing_endov, ov_err, endov_err, ov_count, pattern_num, pattern_list, has_ov)
missing.missing_warn("trigger", missing_trig, missing_endtrig, trig_err, endtrig_err, trig_count, pattern_num, pattern_list, has_trigger)

if tags_err > 0:
    print(" * Missing tags declaration(s)...")
    for pattern in missing_tags:
        print ("    " + str(pattern))

if trig_on_err > 0:
    print(" * Missing trigger conditions...")
    for pattern in missing_trigon:
        print ("    " + str(pattern))

if (body_err or rev_body_err):
    printing.print_eval("body", body_num, endbody_num, "body declarations", body_err, rev_body_err)

if (pattern_num == 0 and not patt_err):
    print(" WARNING: No pattern declarations!");

if (pattern_num == 0 and body_num == 0 and not body_err):
    print(" WARNING: Not able to parse body - pattern missing!");
elif (body_num == 0 and not body_err):
    print(" WARNING: No body declarations!");

print ("\n ===TPL SUMMARY===\n")

print (" TPL Version: " + str(tpl_ver) + "\n")
print (" Number of lines in file:              " + str(line_num))
if (patt_err or rev_patt_err):
    printing.print_eval("pattern", pattern_num, endpattern_num, "pattern declarations", patt_err, rev_patt_err)
else:
    print (" Number of patterns in file:           " + str(pattern_num))

print (" Number of logging statements:         " + str(logs))
print (" Number of comment lines:              " + str(comments))
print (" Number of runCommands:                " + str(runcmds))
print (" Number of fileGets:                   " + str(filegets))
print (" Number of listDirectorys:             " + str(listdirs))
print (" Number of fileInfos:                  " + str(fileinfos))
print (" Number of registryKeys:               " + str(regkeys))
varlist += global_vars
varlist = ulist.uniq(varlist)
varlen = len(varlist) - keywords
print (" Number of variable assignments:       " + str(varlen))
print (" Number of definition blocks:          " + str(define_count))
print (" Number of SI types declared:          " + str(sis))
print (" Number of Detail types declared:      " + str(details))
print (" Number of Simple Identities:          " + str(sid_found))
print (" Number of imported modules:           " + str(imported))

if (if_err or rev_if_err):
    printing.print_eval("if", if_count, endif_count, "IF evaluations", if_err, rev_if_err)
else:
    print (" Number of IF evaluations:             " +str(if_count))

if (for_err or rev_for_err):
    printing.print_eval("for", for_count, endfor_count, "FOR loops", for_err, rev_for_err)
else:
    print (" Number of FOR loops:                  " + str(for_count))

if (table_err or rev_table_err):
    printing.print_eval("table", table_count, endtable_count, "tables declared", table_err, rev_table_err)
else:
    print (" Number of tables declared:            " +str(table_count))

if initlist:
    warning.warnings(initlist, "Uninitialised variable(s) found")

if var_warn:
    var_warn = ulist.uniq(var_warn)
    warning.warnings(var_warn, "Warning: Variable(s) in embedded if/for loops MAY be uninitialised")

if syntax_errs:
    warning.warnings(syntax_errs, "Syntax error in line(s) found")
    
print "\n"
