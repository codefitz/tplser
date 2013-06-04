#!/usr/bin/env python
#
# Version 0.1.7 (alpha)
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

    module_num, endpattern_num, pattern_num, line_num, body_num, endbody_num, if_block, patt_eval, if_eval, for_eval, ov_eval, trig_eval, body_eval, meta_eval, table_eval, config_eval, defins_eval, warn_count, logs, runcmds, filegets, open_notes, comments, sis, details, imported, listdirs, fileinfos, regkeys, if_count, endif_count, for_count, endfor_count, ov_count, endov_count, trig_count, endtrig_count, table_count, unterminated_count, define_count, ov_err, endov_err, tags_err, trig_err, endtrig_err, trig_on_err, endtable_count, sids_err, sid_eval, sid_count, endsid_count, sid_found = [0]*52
    patt_err, if_err, for_err, body_err, table_err, sid_err, lines, mod_line, ov_pattern, trig_pattern, eca_errs, missing_trig, missing_endtrig, missing_trigon, has_trigger, has_ov, initlist, used, imports, unterminated, var_warn, warn_list, for_warn_list, syntax_errs, missing_ov, missing_endov, missing_tags, missing_sid, missing_sids, has_sid = ([] for i in range(30))
    ov_tags, trig_on, ignore_text, constants, defins, open_bracket, end_imports, trigger, assign_eval, var_warning, else_clause, sid_tags, for_block, open_assignment, stopp = [False]*15
    defins_var, ob_line, trig_line, import_line, var_line, no_quotes, config_var = [""]*7

    # For storing custom variables declared in pattern, predefined keywords added here:
    global_vars, varlist = ([ 'model', 'regex', 'discovery', 'search', 'table', 'time', 'false', 'true', 'process', 'function', 'sql_discovery', 'size', 'number', 'xpath', 'none', 'raw', 'expand', 'vsphere_discovery', 'from_id', 'vcenter_discovery', 'in' ] for i in range(2))
    
    # This is a hack to get correct number in summary.
    keywords = len(global_vars)
    
    # Regex for matching syntax
    module_rx = re.compile("tpl\s\d\.\d\smodule\s\S+;")
    tpl_ver_rx = re.compile("tpl\s+(\d+\.\d)")
    metadata_rx = re.compile("^\s*metadata\s*$")
    end_metadata_rx = re.compile("^\s*end\smetadata;")
    import_rx = re.compile("^\s*from\s+\S+\s+import\s+(\w+)")
    import_var_rx = re.compile("(\w+)\s+\d+\.\d")
    table_rx = re.compile("^\s*table\s+\w+\s+\d+\.\d")
    table_vars_rx = re.compile("^\s*table\s+(\w+)\s+\d+\.\d")
    end_table_rx = re.compile("^\s*end\stable;")
    config_rx = re.compile("^\s*configuration\s+\w+\s+\d+\.\d")
    config_var_rx = re.compile("^\s*configuration\s+(\w+)\s+\d+\.\d")
    end_config_rx = re.compile("^\s*end\sconfiguration;")
    definitions_rx = re.compile("^\s*definitions\s+\w+\s+\d+\.\d")
    def_vars_rx = re.compile("^\s*definitions\s+(\w+)\s+\d+\.\d")
    end_definitions_rx = re.compile("^\s*end\sdefinitions;")
    def_var_rx = re.compile("^\s*define\s+(\w+)\(")
    def_return_rx = re.compile("->\s*(.*)\s*$")
    log_rx = re.compile("\s*log\.\w+\(")
    discovery_runcmd_rx = re.compile("\s*discovery\.runCommand\(")
    discovery_fileget_rx = re.compile("\s*discovery\.fileGet\(")
    discovery_listdir_rx = re.compile("\s*discovery\.listDirectory\(")
    discovery_fileinfo_rx = re.compile("\s*discovery\.fileInfo\(")
    discovery_regkey_rx = re.compile("\s*discovery\.registryKey\(")
    model_si_rx = re.compile("\s*model\.SoftwareInstance\(")
    model_det_rx = re.compile("\s*model\.Detail\(")
    identify_rx = re.compile("\s*identify\s+")
    end_identify_rx = re.compile("^\s*end\s*identify;")
    trig_node_rx = re.compile(":=\s*(\w+)\s+")
    trig_cond_rx = re.compile(":=\s*\w+\s+(\w+)\s*")
    trigger_term_rx = re.compile(":=\s*\w+\s*;")
    triggers_rx = re.compile("^\s*triggers\s*$")
    trigger_on_rx = re.compile("^\s*(on\s+\w+\s*:=\s*)")
    embedded_quotes_rx = re.compile("[\'].?[\"].*?[\']")
    quotes_rx = re.compile("[\"\'](.*?)[\"\']")
    double_quotes_rx = re.compile("[\"].*?[\"]")
    single_quotes_rx = re.compile("[\'].*?[\']")
    var_rx = re.compile("^\s*(\w+)")
    vars_rx = re.compile("\s*(\w+)(?:\s*:=|,)")
    in_brackets_rx = re.compile("\((.*)\)")
    if_rx = re.compile("^\s*if\s+")
    if_then_rx = re.compile("^\s*if.*then\s*$")
    end_if_rx = re.compile("^\s*end\sif\s*;")
    comment_block_rx = re.compile("^\s*[\"\'][\"\'][\"\']")
    comment_block_line_rx = re.compile("[\"\'][\"\'][\"\'].*[\"\'][\"\'][\"\']")
    conditionals_rx = re.compile("((?:and\s+|or\s+|)\w+\s+matches(?:\s+\w+)?\s*%)")
    conditional_equals_rx = re.compile("((?:and\s+|or\s+|)\w+\s*=\s*%)")
    overview_rx = re.compile("^\s*overview\s*$")
    tags_rx = re.compile("\s*tags\s+\S+")
    end_overview_rx = re.compile("^\s*end\soverview;")
    constants_rx = re.compile("^\s*constants\s*$")
    global_var_rx = re.compile("(\S+)\s*:=")
    end_constants_rx = re.compile("^\s*end\sconstants;")
    end_trigger_rx = re.compile("^\s*end\striggers;")
    for_rx = re.compile("^\s*for\s+(\S+)\s+in\s+")
    end_for_rx = re.compile("^\s*end\sfor\s*;")
    else_rx = re.compile("^\s*else\s*$")
    syntax_rx = re.compile("^\s*\w+\s*=")
    line_num_rx = re.compile("^\s*\$\d+\$(.*)")
    list_rx = re.compile("^\s*list\.")
    xpath_rx = re.compile("^\s*xpath\.")
    model_rx = re.compile("(^|:=)\s*model\.")
    model_re_rx = re.compile("^\s*model\.\w+\((\w+)\);")
    inference_rx = re.compile("^\s*inference\.")
    no_match_rx = re.compile("no_match\s*:=")
    time_rx = re.compile(":=\s*time\.")
    matches_expand_rx = re.compile("\s*(\S+)\s*:=")
    in_bracket_vars = re.compile(":=\s*(\w+),?")
    embed_vars = re.compile("\(\s*(\w+),?")
    sub_rx = re.compile("%(\w+)%")
    subs_rx = re.compile("\(\S+\s*,\s*(\w+)\);")
    text_rx = re.compile(":=\s*text\.")
    search_rx = re.compile(":=\s*search\s*\(")
    re_discovery_rx = re.compile(":=\s*(regex\.extract|discovery.*)\s*\((\w+),")
    cond_rx = re.compile("\((\w+),")
    sp_chars_rx = re.compile("(\w+),?[\[\.]")
    list_var = re.compile("\(\s*(\S+)?,")

    for full_line in tpl_file:
        lines.append(full_line.strip())
        line_num += 1
        fwd = True
        
        # Count of comments
        if re.match("^\s*//", full_line):
            comments += 1
        
        # Strip comments
        if "//" in full_line:
            # This regex handles embedded " within ' quotes
            #values = re.findall("[\"\'].?.*?[\"\']", full_line)
            apos = full_line.find("'")
            dq = full_line.find('"')
            if apos > dq:
                values = re.findall(double_quotes_rx, full_line) # Double quotes
            else:
                values = re.findall(single_quotes_rx, full_line) # Single quotes
                
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
        if re.match(comment_block_rx, line):
            if open_notes > 0:
                ignore_text = False
                open_notes -= 1
            else:
                ignore_text = True
                open_notes += 1
            if re.search(comment_block_line_rx, line):
                ignore_text = False
                open_notes -= 1

        if ignore_text:
            continue
		
        if not ignore_text:

            # Module Evaluation
            if re.match(module_rx, line):
                module_num += 1
                mod_line.append(str(line_num) + ": " + line)
                tpl_ver = re.match(tpl_ver_rx, line).group(1)

            # Metadata Evaluation
            if re.match(metadata_rx, line):
                meta_eval += 1
                
            if re.match(end_metadata_rx, line):
                meta_eval -= 1

            # Imports - Join all import lines
            import_dec = re.search(import_rx, line)
            
            if import_dec:
                imported += 1
                import_ln = line_num
                import_line = line
                imports = True

            # Import line complete, get all variables
            if imports:
                if not ";" in import_line:
                    import_line += " " + str.strip(line)
                    end_imports = False
                else:
                    import_vars = re.findall(import_var_rx, import_line)
                    imports = False
                    for var in import_vars:
                        global_vars.append(var)

            # Table evaluations
            table = re.search(table_rx, line)
            if table:
                tab_var = re.search(table_vars_rx, line).group(1)
                global_vars.append(tab_var)
                table_count, table_eval = sections.open_match(table_count, table_eval)

            end_table = re.search(end_table_rx, line)
            if end_table:
                endtable_count, table_eval = sections.close_match(endtable_count, table_eval)
                table_eval = loops.loop_eval(table_eval, table_err, line_num)

            # Configuration evaluation
            config = re.search(config_rx, line)
            if config:
                config_eval += 1
                config_var = re.match(config_var_rx, line).group(1)
                # print ("config var = " + str(config_var))
                global_vars.append(config_var)
                tpl_parsing = True

            end_config = re.search(end_config_rx, line)
            if end_config:
                config_eval -= 1
                tpl_parsing = False

            # Definitions evaluation
            definitions = re.search(definitions_rx, line)
            if definitions:
                defins = True
                defins_eval += 1
                defins_var = re.match(def_vars_rx, line).group(1)
                if defins_var:
                    global_vars.append(defins_var)
                tpl_parsing = True

            end_defins = re.search(end_definitions_rx, line)
            if end_defins:
                defins = False
                defins_eval -= 1
                tpl_parsing = False

            # Definition statements
            if defins:
                define = line
                define_var = re.search(def_var_rx, define)
                if define_var:
                    define_count += 1
                    def_vars = re.search(in_brackets_rx, define)
                    def_returns = re.search(def_return_rx, define)
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
            if re.match(log_rx, line):
                logs += 1
                no_quotes = re.sub(quotes_rx, "", line)
                if "+" in no_quotes:
                    if "time." in no_quotes: # time function is not a string
                        eca_errs.append(str(line_num) + ", Concatenation of strings in log statement:\n      " + str.strip(line))
            
            # Count of run commands
            if re.search(discovery_runcmd_rx, line):
                runcmds += 1

            # Count of filegets
            if re.search(discovery_fileget_rx, line):
                filegets += 1
            
            # Count of listdirs
            if re.search(discovery_listdir_rx, line):
                listdirs += 1
            
            # Count of file infos
            if re.search(discovery_fileinfo_rx, line):
                fileinfos += 1

            # Count of registry key lookups
            if re.search(discovery_regkey_rx, line):
                regkeys += 1
                
            # Count of SIs
            if re.search(model_si_rx, line):
                sis += 1

            # Count of Details
            if re.search(model_det_rx, line):
                details += 1

            # Count of simple ids
            if re.match(identify_rx, line):
                sid_count, sid_eval, has_sid, sid_tags = attributes.open_requireds(pattern_name, line, sid_count, sid_eval, has_sid, sid_tags)
            
            # Count of simple ids
            if sid_eval > 0:
                if "simple_identity;" in line:
                    pass # guide line
                elif "->" in line:
                    sid_found += 1

            if re.search(end_identify_rx, line):
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

                # Break down trigger and check consistency in parts
                trig_on = re.search(trigger_on_rx, trig_trim).group(1)
                trig_node = re.search(trig_node_rx, trig_trim).group(1)
                trig_cond = re.search(trig_cond_rx,trig_trim).group(1)
                if trig_on and trig_node: # Basic trigger
                    #print trig_trim
                    trig_statement = False
                    if not trig_cond:
                        if re.search(trigger_term_rx, trig_trim): # If terminated here
                            trig_statement = True
                    else: # termination missing or conditional is missing
                        trig_statement = False
                        
                    # Even bracket check
                    #print trig_trim
                    delim = re.sub(embedded_quotes_rx, "%", trig_trim) # Deal with embedded quotes in single quotes
                    delim = re.sub(quotes_rx, "%", delim)
                    if "(" in delim:
                        open_brackets = delim.count('(')
                        close_brackets = delim.count(')')
                        if not open_brackets == close_brackets:
                            trig_statement = False
                        
                    # Substitute quotes for % delimiter
                    delim_count = delim.count("%") # Check how many conditional statements we should have
                    #print delim
                    #print "delim % = " + str(delim_count)
                    cond_count = 0
                    conds = re.findall(conditionals_rx, delim) # 'matches -----'
                    conds += re.findall(conditional_equals_rx, delim) # '='
                    
                    for cond in conds:
                        cond_count += 1
                        #print ("conds = " + str(cond_count) + ", delims = " + str(delim_count))

                    if delim_count == cond_count:
                        #print "cond_count = " + str(cond_count)
                        trig_statement = True
                    else:
                        trig_statement = False
                
                    if not trig_statement:
                        syntax_errs.append(str(trig_ln) + ": " + str.strip(trig_line))

            # Pattern evaluation
            pattern_name, pattern_num, endpattern_num, patt_eval, patt_parse, patt_err, pattern_list = pattern.pattern_parse(
                pattern_name, fwd, line, pattern_num, endpattern_num, patt_eval, patt_parse, patt_err, line_num)

        # If inside pattern
        if patt_parse:

            # Overview evaluation
            if re.match(overview_rx, line):
                ov_count, ov_eval, has_ov, ov_tags = attributes.open_requireds(pattern_name, line, ov_count, ov_eval, has_ov, ov_tags)

            # Count of tags
            if re.match(tags_rx, line):
                ov_tags = True

            if re.search(end_overview_rx, line):
                endov_count, ov_eval, missing_ov, ov_err, missing_tags, tags_err = attributes.close_requireds(
                    pattern_name, line, endov_count, ov_eval, missing_ov, ov_err, ov_tags, missing_tags, tags_err)

            # Constants
            if re.match(constants_rx, line):
                constants = True

            # This is just a quick var grab, we're not checking the integrity of constants right now
            if constants and re.search(global_var_rx, line):
                global_vars.append(re.search(global_var_rx, line).group(1))

            if re.match(end_constants_rx, line):
                constants = False

            # Trigger evaluation
            if re.match(triggers_rx, line):
                trig_count, trig_eval, has_trigger, trig_on = attributes.open_requireds(pattern_name, line, trig_count, trig_eval, has_trigger, trig_on)

            # Check for trigger condition
            if re.match(trigger_on_rx, line):
                trig_on = True
                global_vars.append(re.search(global_var_rx, line).group(1))

            if re.search(end_trigger_rx, line):
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
            if re.match(if_rx, line):
                if_count, if_eval = sections.open_match(if_count, if_eval)
            if re.match(end_if_rx, line):
                endif_count, if_eval = sections.close_match(endif_count, if_eval)
                if_eval = loops.loop_eval(if_eval, if_err, line_num)
            # Check FOR evaluations
            if re.match(for_rx, line):
                for_count, for_eval = sections.open_match(for_count, for_eval)
            if re.match(end_for_rx, line):
                endfor_count, for_eval = sections.close_match(endfor_count, for_eval)
                for_eval = loops.loop_eval(for_eval, for_err, line_num)

            ############################
            # Variable initialisations #
            ############################
            
            var_ln = line_num
            
            if if_eval > 0 and "stop;" in line:
                stopp = True
            
            if stopp and not "stop;" in line:
                if_containers = ['else', 'elif', 'end if;']
                stopright = False
                for i in if_containers:
                    if i in line:
                        stopright = True
                if not stopright:
                    if line.isspace(): # if line is just whitespace ignore
                        pass
                    else:
                        syntax_errs.append(str(line_num) + ", statement not reachable after stop:\n      " + str.strip(line))
                stopp = False
            
            # For warning variables inside of if evaluations
            if if_eval == 1 and re.match(if_rx, line):
                if_block += 1
                #print "if_block " + str(if_block) + ": " + str(line)
                #print ("pattern: " + str(pattern_name) + ", if_block: " + str(if_block))
            
            if if_eval == 1 and re.match(else_rx, line):
                else_clause = True
            
            if ";" in line:
                #print line
                open_assignment = False
                
                # Check line syntax errors
                no_quotes = re.sub(quotes_rx, "", line)
                #print no_quotes
                #print "================="
                if re.search(syntax_rx, no_quotes): # missing colon (:)
                    syntax_errs.append(str(line_num) + ": " + str.strip(line))
                        
            if ":=" in line:
                open_assignment = True
            
            if config_var and config_var in line:
                #print ("config_var is " + str(config_var))
                conf = re.compile("%s\.(\w+)" %config_var)
                #print ("conf is " + str(conf))
                var = re.search(conf, line)
                if var:
                    used.append(var.group(1))
                    #print ("appending... " + str(var.group(1)))

            if open_assignment and not ";" in line:
                #print "line " + str(var_ln) + " ';' not found"
                if re.search(if_then_rx, line):
                    var_line = line
                    var_declared = True
                else:
                    #print "line " + str(var_ln) + ": " + str(var_line)
                    var_line = " $".join(str(line_num)) + "$ ".join(str.strip(line))
                    var_declared = False
            else:
                open_assignment = False
                var_line += line
                var_declared = True

            if var_declared:
            
                '''
                Get the line number from var_line $ = preserving the line number
                when concatenating an unterminated trigger/var statement
                '''
                if re.match(line_num_rx, var_line):
                    var_line = re.match(line_num_rx, var_line).group(1)
                    #print "line " + str(var_ln) + ": " + str(var_line)
                
                assigner = var_line.count(':=')
                
                # Getting string between "/'  characters
                quotes = re.findall(quotes_rx, var_line)
                if quotes:
                    for quote in quotes:
                        if ":=" in quote:
                            assigner -= 1 # Remove an := chars between quotes
                
                # Check to see if it belongs to a function, multiple assigners are expected
                if assigner > 1:
                    defin = re.compile(":=\s*%s\."%defins_var)
                    if defin:
                        pass
                    elif re.search(log_rx, var_line):
                        pass
                    elif re.search(list_rx, var_line):
                        pass
                    elif re.search(xpath_rx, var_line):
                        pass
                    elif re.search(model_rx, var_line):
                        pass
                    elif re.search(inference_rx, var_line):
                        pass
                    elif re.search(no_match_rx, var_line):
                        pass
                    elif re.search(time_rx, var_line):
                        pass
                    else:
                        #print "line " + str(var_ln) + ": " + str(var_line)
                        #print "=========================================="
                        syntax_errs.append(str(var_ln) + ": " + str.strip(var_line))
                
                # Get variables assigned
                
                var = ""
                #print "line " + str(var_ln) + ": " + str(var_line)
                if re.search(var_rx, var_line):
                    var = re.search(var_rx, var_line).group(1)
                    #print ("var = " + str(var) + " (" + str(var_ln) + ")")
                    #if "." in var:
                    #    var = re.search("^\s*(\w+)\.", var_line).group(1)
                    varlist.append(var)
                    #print "appended " + str(var) + " to varlist (" + str(var_ln) + ")"
                    
                if re.search(var_rx, var_line):
                    vars = re.findall(vars_rx, var_line)
                    for var in vars:
                        varlist.append(var)
                        #print "appended " + str(var) + " to varlist (" + str(var_ln) + ")"

                if re.search(for_rx, var_line):
                    var = re.search(for_rx, var_line).group(1)
                    for_block = True
                    varlist.append(var)
                
                if "matches expand" in line:
                    var = re.search(matches_expand_rx, var_line)
                    if var:
                        #print("matches expand: " + str(var))
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
                
                in_brackets = re.search(in_brackets_rx, var_line)
                
                # Handle multiple assignments such as in model declarations
                if in_brackets:
                    vars = re.findall(in_bracket_vars, in_brackets.group(1))
                    for var in vars:
                        if re.search(sub_rx, var):
                            subs = re.findall(sub_rx, var) # multiple substitutions
                            if subs:
                                for sub in subs:
                                    used.append(sub)
                        elif re.search(text_rx, var_line):
                            pass
                        else:
                            used.append(var)
                            
                    # Handle embedded functions and quotes
                    embed_line = re.sub(single_quotes_rx, "", var_line) # Single quotes
                    embed_line = re.sub(double_quotes_rx, "", embed_line) # Double quotes
                    embeds = embed_line.count('(')
                    bcount = var_line.count('(')
                    if re.search(model_rx, var_line):
                        pass
                    elif re.search(log_rx, var_line):
                        pass
                    elif re.search(search_rx, var_line):
                        pass
                    elif re.search(time_rx, var_line):
                        pass
                    elif embeds > 0 and not embeds == bcount:
                        vars = re.findall(embed_vars, embed_line)
                        for var in vars:
                            if var == "text":
                                pass # text function
                            elif var == "not":
                                pass # not evaluation
                            else:
                                used.append(var)

                if re.search(re_discovery_rx, var_line):
                    cond = re.search(cond_rx, var_line).group(1)
                    if "[" in cond or "." in cond:
                        used.append(re.search(sp_chars_rx, cond).group(1))
                    else:
                        used.append(cond)

                    subs = re.search(subs_rx, var_line) # Substitution vars
                    if subs:
                        used.append(subs.group(1))

                if re.search(sub_rx, line):
                    used.append(re.search(sub_rx, line).group(1))

                if re.search(model_re_rx, var_line):
                    used.append(re.search(model_re_rx, var_line).group(1))

                if re.search(list_rx, var_line):
                    var = re.search(list_var, var_line).group(1)
                    if "[" in var or "." in var:
                        used.append(re.search(sp_chars_rx, var_line).group(1))
                    else:
                        used.append(var)
                    
                    subs = re.search(subs_rx, var_line)
                    if subs:
                        used.append(subs.group(1))

                if re.search(":=\s*(\w+)\+?.*[;,]", var_line):
                    var = re.search(":=\s*(\w+)\+?.*[;,]", var_line).group(1)
                    if var == "text":
                        if "%" in line:
                            vars = re.findall("%(\w+)%", var_line)
                            for var in vars:
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

                if re.search(if_rx, var_line):
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

                        '''
                        This takes place outside of for loop as a var may be assigned twice but still be valid in the same
                        block, so we have to check that it is both not the same block and that it is a new block
                        '''
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
                if re.match(end_if_rx, row):
                    rev_endif_count, rev_if_eval = sections.open_match(rev_endif_count, rev_if_eval)
                if re.match(if_rx, row):
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
        print ("    line %s" %mod_err)
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
print (" Number of lines in file:              %s" %line_num)
if (patt_err or rev_patt_err):
    printing.print_eval("pattern", pattern_num, endpattern_num, "pattern declarations", patt_err, rev_patt_err)
else:
    print (" Number of patterns in file:           %s" %pattern_num)

print (" Number of logging statements:         %s" %logs)
print (" Number of comment lines:              %s" %comments)
print (" Number of runCommands:                %s" %runcmds)
print (" Number of fileGets:                   %s" %filegets)
print (" Number of listDirectorys:             %s" %listdirs)
print (" Number of fileInfos:                  %s" %fileinfos)
print (" Number of registryKeys:               %s" %regkeys)
varlist += global_vars
varlist = ulist.uniq(varlist)
varlen = len(varlist) - keywords
print (" Number of variable assignments:       %s" %varlen)
print (" Number of definition blocks:          %s" %define_count)
print (" Number of SI types declared:          %s" %sis)
print (" Number of Detail types declared:      %s" %details)
print (" Number of Simple Identities:          %s" %sid_found)
print (" Number of imported modules:           %s" %imported)

if (if_err or rev_if_err):
    printing.print_eval("if", if_count, endif_count, "IF evaluations", if_err, rev_if_err)
else:
    print (" Number of IF evaluations:             %s" %if_count)

if (for_err or rev_for_err):
    printing.print_eval("for", for_count, endfor_count, "FOR loops", for_err, rev_for_err)
else:
    print (" Number of FOR loops:                  %s" %for_count)

if (table_err or rev_table_err):
    printing.print_eval("table", table_count, endtable_count, "tables declared", table_err, rev_table_err)
else:
    print (" Number of tables declared:            %s" %table_count)

if initlist:
    warning.warnings(initlist, "Uninitialised variable(s) found")

if var_warn:
    var_warn = ulist.uniq(var_warn)
    warning.warnings(var_warn, "Warning: Variable(s) in embedded if/for loops MAY be uninitialised")

if syntax_errs:
    warning.warnings(syntax_errs, "Syntax error in line(s) found")

if eca_errs:
    warning.warnings(eca_errs, "Warning: The syntax in these line(s) may cause an ECA Error")
    
print "\n"
