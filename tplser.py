#!/usr/bin/env python
#
# Version 0.1.9 (Beta)
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

body_parsing, rev_parsing, pattern_parsing, rev_patt_parse, tpl_parsing, fwd = [False] * 6
pattern_name = ""

#pdb.set_trace()

with open(sys.argv[1]) as tpl_file:

    ##########################
    #== Read Lines Forward ==#
    ##########################

    module_num, endpattern_num, pattern_num, line_num, body_num, endbody_num, if_block, patt_eval, if_eval, for_eval, ov_eval, trig_eval, body_eval, meta_eval, table_eval, config_eval, defins_eval, warn_count, logs, runcmds, filegets, open_notes, comments, sis, details, imported, listdirs, fileinfos, regkeys, if_count, endif_count, for_count, endfor_count, ov_count, endov_count, trig_count, endtrig_count, table_count, unterminated_count, define_count, ov_err, endov_err, tags_err, trig_err, endtrig_err, trig_on_err, endtable_count, sids_err, sid_eval, sid_count, endsid_count, sid_found = [0]*52
    patt_err, if_err, for_err, body_err, table_err, sid_err, lines, mod_line, ov_pattern, trig_pattern, eca_errs, missing_trig, missing_endtrig, missing_trigon, has_trigger, has_ov, initlist, used, imports, unterminated, var_warn, warn_list, for_warn_list, syntax_errs, missing_ov, missing_endov, missing_tags, missing_sid, missing_sids, has_sid = ([] for i in range(30))
    ov_tags, trig_on, ignore_text, constants, defins, open_bracket, end_imports, trigger, assign_eval, var_warning, else_clause, sid_tags, for_block, open_assignment, stop_pattern = [False]*15
    defins_var, ob_line, trig_line, import_line, var_line, no_quotes, config_var = [""]*7

    # For storing custom variables declared in pattern, predefined keywords added here:
    global_vars, total_vars, varlist, if_close_pattern, constant_vars, vars_assigned, utilised, model_lines, config_funcs, defins_funcs = ([] for i in range(10))
    
    # Pre-defined TPL Keywords
    keyword_list = ['model', 'discovery', 'import', 'module', 'overrides', 'end', 'then', 'on', 'from', 'log', 'search', 'do', 'definitions', 'aged', 'as', 'at', 'break', 'by', 'continue', 'created', 'default', 'defined', 'deleted', 'desc', 'exists', 'expand', 'explode', 'false', 'flags', 'is', 'locale', 'modified', 'nodecount', 'nodes', 'none', 'order', 'out', 'processwith', 'relationship', 'removal', 'requires', 'show', 'step', 'stop', 'substring', 'subword', 'summary', 'tags', 'taxonomy', 'traverse', 'true', 'unconfirmed', 'with', 'where', 'matches', 'and', 'not', 'or', 'has', 'in', 'raw', 'regex', 'unix_cmd', 'windows_cmd', 'tpl', 'identify', 'constants', 'pattern', 'triggers', 'body', 'table', 'configuration', 'metadata', 'define', 'overview', 'if', 'for', 'else', 'elif', 'function', 'text', 'time']

    # This is a hack to get correct number in summary.
    keywords = len(keyword_list)
    
    # Regex for matching syntax
    and_rx = re.compile("\s+and\s+(not\s+)?(\w+)")
    comment_block_line_rx = re.compile("[\"\'][\"\'][\"\'].*[\"\'][\"\'][\"\']")
    comment_block_rx = re.compile("^\s*[\"\'][\"\'][\"\']")
    cond_rx = re.compile("\((\w+),")
    conditional_equals_rx = re.compile("((?:and\s+|or\s+|)\w+\s*=\s*%)")
    conditionals_rx = re.compile("((?:and\s+|or\s+|)\w+\s+matches(?:\s+\w+)?\s*%)")
    config_rx = re.compile("^\s*configuration\s+\w+\s+\d+\.\d")
    config_var_rx = re.compile("^\s*configuration\s+(\w+)\s+\d+\.\d")
    constants_rx = re.compile("^\s*constants\s*$")
    def_return_rx = re.compile("->\s*(.*)\s*$")
    def_var_rx = re.compile("^\s*define\s+(\w+)\(")
    def_vars_rx = re.compile("^\s*definitions\s+(\w+)\s+\d+\.\d")
    definitions_rx = re.compile("^\s*definitions\s+\w+\s+\d+\.\d")
    discovery_fileget_rx = re.compile("\s*discovery\.fileGet\(")
    discovery_fileinfo_rx = re.compile("\s*discovery\.fileInfo\(")
    discovery_listdir_rx = re.compile("\s*discovery\.listDirectory\(")
    discovery_regkey_rx = re.compile("\s*discovery\.registryKey\(")
    discovery_runcmd_rx = re.compile("\s*discovery\.runCommand\(")
    double_quotes_rx = re.compile("[\"].*?[\"]")
    else_rx = re.compile("^\s*else\s*$")
    embed_vars = re.compile("\(\s*(\w+),?")
    embedded_quotes_rx = re.compile("[\'].?[\"].*?[\']")
    end_config_rx = re.compile("^\s*end\sconfiguration;")
    end_constants_rx = re.compile("^\s*end\sconstants;")
    end_definitions_rx = re.compile("^\s*end\sdefinitions;")
    end_for_rx = re.compile("^\s*end\sfor\s*;")
    end_identify_rx = re.compile("^\s*end\s*identify;")
    end_if_rx = re.compile("^\s*end\sif\s*;")
    end_metadata_rx = re.compile("^\s*end\smetadata;")
    end_overview_rx = re.compile("^\s*end\soverview;")
    end_table_rx = re.compile("^\s*end\stable;")
    end_trigger_rx = re.compile("^\s*end\striggers;")
    equals_rx = re.compile("=\s+text\.\w+\((\w+)")
    for_in_rx = re.compile("^\s*for\s*\S+\s*in\s*(\w+)")
    for_rx = re.compile("^\s*for\s+(\S+)\s+in\s+")
    global_var_rx = re.compile("(\S+)\s*:=")
    has_substring_rx = re.compile("has\s*substring\s*(\w+)")
    identify_rx = re.compile("\s*identify\s+")
    if_line_rx = re.compile("^\s*if\s+(size)?\(?(not\s+)?(\w+)(?<!\))")
    if_not_rx = re.compile("^\s*if\s*\(\s*not\s*\(\s*(\w+)")
    if_rx = re.compile("^\s*if\s+")
    if_text_rx = re.compile("^\s*if\s+text\.\w+\((\w+)")
    if_then_rx = re.compile("^\s*if.*then\s*$")
    import_rx = re.compile("^\s*from\s+\S+\s+import\s+(\w+)")
    import_var_rx = re.compile("(\w+)\s+\d+\.\d")
    in_bracket_vars = re.compile(":=\s*(\w+),?")
    in_brackets_rx = re.compile("\((.*)\)")
    inference_rx = re.compile("^\s*inference\.")
    line_num_rx = re.compile("^\s*\$\d+\$(.*)")
    list_rx = re.compile("^\s*list\.")
    list_var_rx = re.compile("\(\s*(\S+)?,")
    log_rx = re.compile("\s*log\.\w+\(")
    matches_expand_rx = re.compile("\s*(\S+)\s*:=")
    matches_regex_rx = re.compile("matches\s+regex\s*(\w+)")
    metadata_rx = re.compile("^\s*metadata\s*$")
    model_det_rx = re.compile("\s*model\.Detail\(")
    model_re_rx = re.compile("^\s*model\.\w+\((\w+)\);")
    model_rx = re.compile("(^|:=)\s*model\.")
    model_si_rx = re.compile("\s*model\.SoftwareInstance\(")
    module_rx = re.compile("tpl\s\d\.\d\smodule\s\S+;")
    no_match_rx = re.compile("no_match\s*:=")
    not_in_rx = re.compile("not\s+in\s+(\w+)")
    numeric_rx = re.compile("^[0-9]")
    or_rx = re.compile("(?:(\".*)|\s+or\s+(\w+))")
    overview_rx = re.compile("^\s*overview\s*$")
    quotes_rx = re.compile("[\"\'](.*?)[\"\']")
    re_discovery_rx = re.compile(":=\s*(regex\.extract|discovery.*)\s*\((\w+),")
    result_rx = re.compile("(\w+)\.(result|content)")
    search_rx = re.compile(":=\s*search\s*\(")
    single_quotes_rx = re.compile("[\'].*?[\']")
    sp_chars_rx = re.compile("(\w+),?[\[\.]")
    square_bracket_rx = re.compile("\[(\w+)")
    sub_rx = re.compile("%(\w+)%")
    subs_rx = re.compile("\(\S+\s*,\s*(\w+)\);")
    syntax_rx = re.compile("^\s*\w+\s*=")
    table_rx = re.compile("^\s*table\s+\w+\s+\d+\.\d")
    table_vars_rx = re.compile("^\s*table\s+(\w+)\s+\d+\.\d")
    tags_rx = re.compile("\s*tags\s+\S+")
    text_rx = re.compile(":=\s*text\.")
    time_rx = re.compile(":=\s*time\.")
    tpl_ver_rx = re.compile("tpl\s+(\d+\.\d)")
    trig_cond_rx = re.compile(":=\s*\w+\s+(\w+)\s*")
    trig_node_rx = re.compile(":=\s*(\w+)\s+")
    trigger_on_rx = re.compile("^\s*(on\s+\w+\s*:=\s*)")
    trigger_term_rx = re.compile(":=\s*\w+\s*;")
    triggers_rx = re.compile("^\s*triggers\s*$")
    var_plus_rx = re.compile(":=\s*(\w+)\+?.*[;,]")
    var_rx = re.compile("^\s*(\w+)")
    vars_rx = re.compile("\s*(\w+)(?:\s*:=|,)")
    xpath_rx = re.compile("^\s*xpath\.")

    for full_line in tpl_file:
        lines.append(full_line.strip())
        line_num += 1
        fwd = True
        
        # Count of comments
        if re.match("^\s*//", full_line):
            comments += 1
        
        # Strip comments
        line = commentparse.removal(full_line, double_quotes_rx, single_quotes_rx)

		# Ignore developer notes block
        ignore_text = commentparse.noteblock(
                fwd, comment_block_rx, comment_block_line_rx, line, open_notes)

        if ignore_text:
            continue
        else:

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
                table_count, table_eval = sectionparse.open_match(
                    table_count, table_eval)

            end_table = re.search(end_table_rx, line)
            if end_table:
                endtable_count, table_eval = sectionparse.close_match(
                    endtable_count, table_eval)
                table_eval, table_err = evaluations.loop_eval(table_eval, table_err, line_num)

            # Configuration evaluation
            option = False # This option is not used by config eval - just a holder for the function
            tpl_parsing, global_vars, option, config_funcs = sectionparse.section(
                config_rx, end_config_rx, line, config_eval, config_var_rx, global_vars, option, tpl_parsing, config_funcs)

            # Definitions evaluation
            tpl_parsing, global_vars, defins, defins_funcs = sectionparse.section(
                definitions_rx, end_definitions_rx, line, defins_eval, def_vars_rx, global_vars, defins, tpl_parsing, defins_funcs)

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
                            varlist.append(var)
                            print "Appending " + str(var) + " to varlist..."
                    if def_returns:
                        split_return = str(def_returns.group(1)).split(',')
                        for split_var in split_return:
                            var = str.strip(split_var)
                            varlist.append(var)

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
                sid_count, sid_eval, has_sid, sid_tags = sectionparse.open_requireds(
                    pattern_name, line, sid_count, sid_eval, has_sid, sid_tags)
            
            # Count of simple ids
            if sid_eval > 0:
                if "simple_identity;" in line:
                    pass # guide line
                elif "->" in line:
                    sid_found += 1

            if re.search(end_identify_rx, line):
                endsid_count, sid_eval, missing_sid, sid_err, missing_sids, sids_err = sectionparse.close_requireds(
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
            pattern_name, pattern_num, endpattern_num, patt_eval, pattern_parsing, patt_err, pattern_list, varlist = sectionparse.pattern_parse(
                pattern_name, fwd, line, pattern_num, endpattern_num, patt_eval, pattern_parsing, patt_err, line_num ,varlist)
                
        # If inside pattern
        if pattern_parsing:
        
            '''
                Check number of if statements where odd number of evaluations equals 
                even numbers where even number of patterns exist.
                This resets the count, the next evaluation will fail but at least
                there is an indicator that something is wrong.
            '''
            if endpattern_num > 0:
                if not pattern_name == last_pattern:
                    if if_eval > 0:
                        if_eval = 0
                    last_pattern = pattern_name
                    if for_eval > 0:
                        for_eval = 0
                    last_pattern = pattern_name
            else:
                last_pattern = pattern_name

            # Overview evaluation
            if re.match(overview_rx, line):
                ov_count, ov_eval, has_ov, ov_tags = sectionparse.open_requireds(
                    pattern_name, line, ov_count, ov_eval, has_ov, ov_tags)

            # Count of tags
            if re.match(tags_rx, line):
                ov_tags = True

            if re.search(end_overview_rx, line):
                endov_count, ov_eval, missing_ov, ov_err, missing_tags, tags_err = sectionparse.close_requireds(
                    pattern_name, line, endov_count, ov_eval, missing_ov, ov_err, ov_tags, missing_tags, tags_err)

            # Constants
            if re.match(constants_rx, line):
                constants = True

            # This is just a quick var grab, we're not checking the integrity of constants right now
            if constants and re.search(global_var_rx, line):
                varlist.append(re.search(global_var_rx, line).group(1))

            if re.match(end_constants_rx, line):
                constants = False
                
            # Find redefined variables in constants
            if constants:
                if ":=" in line:
                    #Grab everything to the left of the seperator
                    left = re.findall("(\S+)\s*:=", line)
                    for var in left:
                        if var in constant_vars:
                            syntax_errs.append(str(line_num) + ", Constant " + str(var) + " has been redefined:\n      " + str.strip(line))
                        else:
                            constant_vars.append(var)
            else:
                # Reset after section is complete for the next pattern
                constant_vars = []

            # Trigger evaluation
            if re.match(triggers_rx, line):
                trig_count, trig_eval, has_trigger, trig_on = sectionparse.open_requireds(
                    pattern_name, line, trig_count, trig_eval, has_trigger, trig_on)

            # Check for trigger condition
            if re.match(trigger_on_rx, line):
                trig_on = True
                varlist.append(re.search(global_var_rx, line).group(1))

            if re.search(end_trigger_rx, line):
                endtrig_count, trig_eval, missing_trig, trig_err, missing_trigon, trig_on_err = sectionparse.close_requireds(
                    pattern_name, line, endtrig_count, trig_eval, missing_trig, trig_err, trig_on, missing_trigon, trig_on_err)

            # Body evaluation
            body_num, endbody_num, body_eval, body_parsing, body_err = sectionparse.body_parse(
                fwd, line, body_num, endbody_num, body_eval, body_parsing, body_err, line_num)

            # If inside body
            if body_parsing:

                # Check end ov
                ov_eval, missing_endov, endov_err = sectionparse.closing_decs(
                    ov_eval, missing_endov, pattern_name, endov_err)
                # Check end trigger
                trig_eval, missing_endtrig, endtrig_err = sectionparse.closing_decs(
                    trig_eval, missing_endtrig, pattern_name, endtrig_err)

                # Set general TPL parsing
                tpl_parsing = True
                #print ("Current valist is:\n" + str(varlist))

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
                if_count, if_eval = sectionparse.open_match(if_count, if_eval)
            if re.match(end_if_rx, line):
                endif_count, if_eval = sectionparse.close_match(endif_count, if_eval)
                if_eval, if_err = evaluations.loop_eval(if_eval, if_err, line_num)
            # Check FOR evaluations
            if re.match(for_rx, line):
                for_count, for_eval = sectionparse.open_match(for_count, for_eval)
            if re.match(end_for_rx, line):
                endfor_count, for_eval = sectionparse.close_match(endfor_count, for_eval)
                for_eval, for_err = evaluations.loop_eval(for_eval, for_err, line_num)

            # Check for syntax errors with the 'stop;' statement
            if if_eval > 0 and "stop;" in line:
                stop_pattern = True
            
            if stop_pattern and not "stop;" in line:
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
                stop_pattern = False
            
            ######################################################
            
            '''
                This is an alternative cleaner way of doing the variable asignment
                checking. Under development.
            '''

            # Find redefined variables in constants
            # if ":=" in line:
                #Grab everything to the left of the seperator
                # left = re.findall("(\S+)\s*:=", line)
                    # for var in left:
                        # constant_vars.append(var)
                        #if "model." in var:
                            # '''Variables assigned in model function are not pattern
                            # variables and therefore not used elsewhere.'''
                            # model_lines.append(line)
                            # pass
                        # else:
                            # print("line " + str(line_num) + ": " + str(var))
                            # vars_assigned.append(var)
                #Grab everything to the right of the seperator
                #right = re.findall(":=(.*)", line)
                #for var in right:
                    #if var not in vars_assigned:
                        #print("line " + str(line_num) + ": " + str(var))
            # else:
                #Reset after section is complete for the next pattern
                # constant_vars = []
                        
            #######################################################
                
            ############################
            # Variable initialisations #
            ############################
            
            var_ln = line_num
            
            # For warning variables inside of if evaluations
            if if_eval == 1 and re.match(if_rx, line):
                if_block += 1
            
            if if_eval == 1 and re.match(else_rx, line):
                else_clause = True
                
            ''' Join up variable assignments that spread over multiple lines'''
            
            if ";" in line:
                open_assignment = False
                
                # Check line syntax errors
                no_quotes = re.sub(quotes_rx, "", line)
                if re.search(syntax_rx, no_quotes): # missing colon (:)
                    syntax_errs.append(str(line_num) + ": " + str.strip(line))
                        
            if ":=" in line:
                open_assignment = True

            if open_assignment and not ";" in line:
                if re.search(if_then_rx, line):
                    var_line = line
                    var_declared = True
                else:
                    # Don't use join() here it does funky stuff to the insert!
                    var_line += " $" + str(line_num) + "$ " + str.strip(line)
                    var_declared = False
            else:
                open_assignment = False
                var_line += line
                var_declared = True
            
            #print var_line
            
            ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

            if var_declared:
            
                '''
                Get the line number from var_line $ = preserving the line number
                when concatenating an unterminated trigger/var statement
                '''
                if re.match(line_num_rx, var_line):
                    var_line = re.match(line_num_rx, var_line).group(1)

                assigner = var_line.count(':=')
                
                # Getting string between " & ' characters
                quotes = re.findall(quotes_rx, var_line)
                if quotes:
                    for quote in quotes:
                        if ":=" in quote:
                            assigner -= 1 # Don't count any ':=' chars between quotes
                
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
                vars = re.findall(vars_rx, var_line)
                for var in vars:
                    #print (str(line_num) + ", assigning var " + str(var) + " to varlist")
                    varlist.append(var)

                var = re.search(for_rx, var_line)
                if var:
                    for_block = True
                    #print (str(line_num) + ", assigning var " + str(var) + " to varlist")
                    varlist.append(var.group(1))
                
                # Get full count so that varlist can be reset with each pattern
                '''
                I can't recall why this is needed
                
                #if "matches expand" in line:
                    #var = re.search(matches_expand_rx, var_line)
                    #if var:
                        #print var_line
                        #print "3 " + str(var.group(1))
                        #varlist.append(var.group(1))
                '''

                if var:
                    '''
                    Check if variable has already been declared, if not then
                    it is a genuine warning
                    '''
                    if (if_eval > 0) and not else_clause and not for_block:
                        warn = ifblock.IfBlock(if_block, if_eval, var)
                        warn_list.append(warn)
                        for_block = False
                    else:
                        varlist.append(var)
                        
                for var in varlist:
                    total_vars.append(var)

                ######################
                # Variables utilised #
                ######################
                
                if config_var and config_var in line:
                    # This is getting a configuration variable config.(x)
                    conf = re.compile("%s\.(\w+)" %config_var)
                    var = re.search(conf, line)
                    if var:
                        used.append(var.group(1))
                
                in_brackets = re.search(in_brackets_rx, var_line)
                # Handle multiple assignments such as in model declarations
                if in_brackets:
                    vars = re.findall(in_bracket_vars, in_brackets.group(1))
                    for var in vars:
                        subs = re.findall(sub_rx, var) # multiple substitutions
                        if subs:
                            for sub in subs:
                                used.append(sub)
                        elif re.search(text_rx, var_line):
                            pass
                            
                    # Handle embedded functions and quotes
                    embed_line = re.sub(single_quotes_rx, "", var_line) # Single quotes
                    embed_line = re.sub(double_quotes_rx, "", embed_line) # Double quotes
                    embeds = embed_line.count('(')
                    bcount = var_line.count('(')
                    '''
                        This is kind of a workaround for functions being used, but
                        ultimately there needs to be some syntax checking for functions
                        themselves.
                    '''
                    if re.search(model_rx, var_line):
                        pass
                    elif re.search(log_rx, var_line):
                        subs = re.findall(sub_rx, var_line) # multiple substitutions
                        if subs:
                            for sub in subs:
                                used.append(sub)
                                #print sub
                                #print varlist
                    elif re.search(search_rx, var_line):
                        pass
                    elif re.search(time_rx, var_line):
                        pass
                    elif re.search(text_rx, var_line):
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

                #if re.search(re_discovery_rx, var_line):
                cond = re.search(cond_rx, var_line)
                if cond:
                    var = cond.group(1)
                    if "[" in var or "." in var:
                        used.append(re.search(sp_chars_rx, var).group(1))
                    else:
                        used.append(var)

                # variables acting as substitutes
                subs = re.search(subs_rx, var_line)
                if subs:
                    used.append(subs.group(1))

                '''
                Looking for %---% substitutions, can include log files so we use
                full line here.
                '''
                sub = re.search(sub_rx, line)
                if sub:
                    used.append(sub.group(1))

                model_re = re.search(model_re_rx, var_line)
                if model_re:
                    used.append(model_re.group(1))

                list_var = re.search(list_var_rx, var_line)
                if list_var:
                    var = list_var.group(1)
                    if "[" in var or "." in var:
                        if re.search(sp_chars_rx, var_line):
                            used.append(re.search(sp_chars_rx, var_line).group(1))
                    elif "%" in var:
                        pass # Just ignoring %...% subs, these will be checked in other function
                    else:
                        used.append(var)

                var_plus = re.search(var_plus_rx, var_line)
                if var_plus:
                    var = var_plus.group(1)
                    if var == "text":
                        if "%" in line:
                            vars = re.findall(sub_rx, var_line)
                            for var in vars:
                                if "[" in var or "." in var:
                                    used.append(re.search(sp_chars_rx, var).group(1))
                                else:
                                    used.append(var)
                    else:
                        used.append(var)

                result = re.search(result_rx, var_line)
                if result:
                    used.append(result.group(1))

                for_in = re.search(for_in_rx, var_line)
                if for_in:
                    cond = for_in.group(1)
                    if "(" in cond:
                        used.append(re.search(list_var, cond).group(1))
                    elif "." in cond:
                        used.append(re.search(sp_chars_rx, cond).group(1))
                    elif "[" in cond:
                        used.append(re.search(sp_chars_rx, cond).group(1))
                        used.append(re.search(square_bracket_rx, cond).group(1))
                    elif cond == "text":
                        cond = re.findall(if_text_rx, var_line)
                        for var in cond:
                            used.append(var)
                    else:
                        used.append(cond)

                if_line = re.search(if_line_rx, var_line)
                if if_line:
                    var = if_line.group(3)
                    if "." in var:
                        used.append(re.search(sp_chars_rx, var).group(1))
                    elif "[" in var:
                        used.append(re.search(sp_chars_rx, var).group(1))
                        used.append(re.search(square_bracket_rx, var).group(1))
                    elif var == "not":
                        if_not = (if_not_rx, var_line)
                        if if_not:
                            var = if_not.group(1)
                            used.append(var)
                    elif var == "text":
                        vars = re.findall(if_text_rx, var_line)
                        for var in vars:
                            used.append(var)
                    else:
                        used.append(var)

                    has_substring = re.search(has_substring_rx, var_line)
                    if has_substring:
                        used.append(has_substring.group(1))

                    matches_regex = re.search(matches_regex_rx, var_line)
                    if matches_regex:
                        used.append(matches_regex.group(1))

                    or_or = re.match(or_rx, var_line)
                    if or_or:
                        used.append(or_or.group(2))
                        
                    if_quotes = re.sub(quotes_rx, "", var_line)
                    if if_quotes:
                        pass
                    else:
                        and_and = re.search(and_rx, var_line)
                        if and_and:
                            used.append(and_and.group(2))

                    equals = re.search(equals_rx, var_line)
                    if equals:
                        used.append(equals.group(1))

                    not_in = re.search(not_in_rx, var_line)
                    if not_in:
                        used.append(not_in.group(1))
                        
                    # Check for uneven brackets
                    if "(" in var_line or ")" in var_line:
                        openb = var_line.count('(')
                        closeb = var_line.count(')')
                        if not openb == closeb:
                            syntax_errs.append(str(line_num) + ", Uneven opening and closing brackets:\n      " + str.strip(line))
                
                for var in used:
                    '''
                    Now we check all used variables against variable initialisations.
                    If they used and not initialised, or initialised within an if block.
                    '''
                    
                    #if var == "host":
                        # print ("====================================")
                        #print ("\nChecking...   " + str(var) + "\n")
                        #print str(line_num) + ": " + str(var_line)
                        # print global_vars
                        # print varlist
                    
                    # Get actual line number
                    if assigner > 1:
                        #print ("Var " + str(var) + "assigner > 1")
                        in_brackets = re.search(in_brackets_rx, var_line)
                        if in_brackets:
                            #print ("Var " + str(var) + "in brackets")
                            get_ln = re.compile("\$(\d+)\$\s+\S+\s*:=\s*%s,?"%var)
                            if re.search(get_ln, var_line):
                                var_ln = re.search(get_ln, var_line).group(1)

                    if re.match(numeric_rx, var):
                        #print ("Var " + str(var) + "integer")
                        pass # Variable is an integer value
                        
                    elif var in keyword_list:
                        '''
                            Variable is a keyword - some evaluation should be done
                            in future to check keyword used appropriately
                        '''
                        #print ("Var " + str(var) + "In keyword_list")
                        pass
                        
                    elif var in config_funcs:
                        # This is a configuration function variable
                        #print ("Var " + str(var) + "In config name")
                        pass
                    
                    elif var in defins_funcs:
                        # This is a definition function variable
                        #print ("Var " + str(var) + "In definition name")
                        pass
                    
                    elif var in global_vars:
                        #print ("Var " + str(var) + "In global vars")
                        # Check the line to see if it's declared as a function
                        get_conf = re.compile("(\w+)\.%s"%var)
                        line_conf = re.search(get_conf, var_line)
                        if line_conf:
                            if line_conf.group(1) in global_vars:
                                '''
                                    For configuration items, this needs to be a
                                    seperate list from global_vars ideally because
                                    we could still get mixed up with non-config name
                                '''
                                pass # variable belongs to configuration
                            elif line_conf.group(1) in keyword_list:
                                pass # is a keyword function
                            else:
                                # Configuration name is not valid
                                syntax_errs.append(str(line_num) + ", Config item not valid:\n      " + str.strip(var_line))
                        else:
                            pass

                        # elif defins:
                            # print ("Var " + str(var) + "In definition block")
                            # '''
                                # Variable currently evaluated inside definitions block
                                # Needs some extra rules or split from global vars
                            # '''
                            # pass
                    else:
                        #print ("Evaluating Var " + str(var))
                        '''
                            The variable may be previously initialised, but then gets
                            re-initialised inside the if-block, so we check against our
                            global list.
                        '''

                        # Variable just not initialised at all
                        if var not in varlist:
                            initlist.append(str(var_ln) + ": " + str(var))

                        same_block = False
                        new_if_block = False
                        
                        # Check variables inside the if-block
                        for warn in warn_list:
    
                            if warn.variable == var:
                                '''
                                    if a variable is on our warnlist, and the current variable
                                    matches it, we are interested
                                '''
                                
                                if warn.eval == 0:
                                    '''
                                        if the current variable is outside the if-block then
                                        this is definitely a valid warning.
                                    '''
                                    var_warn.append(str(var_ln) + ": " + str(var))
                                
                                if if_block == warn.block:
                                    #We're still inside the same if-block, we don't need a warning.
                                    same_block = True

                                if if_block > warn.block:
                                    '''
                                        The warning variable is inside an if-block earlier to
                                        the current if-block therefore it needs a warning.
                                    '''
                                    new_if_block = True

                        if not same_block and new_if_block:
                            '''
                                This takes place outside of for loop as a var may be assigned
                                twice but still be valid in the same block, so we have to check
                                that it is both not the same block and that it is a new block.
                            '''
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
            end_table = re.search(end_table_rx, row)
            if end_table:
                rev_endtable_count, rev_table_eval = sectionparse.open_match(
                    rev_endtable_count, rev_table_eval)

            table = re.search(table_rx, row)
            if table:
                rev_table_count, rev_table_eval = sectionparse.close_match(
                    rev_table_count, rev_table_eval)
                rev_table_eval, rev_table_err = evaluations.loop_eval(
                    rev_table_eval, rev_table_err, rev_line_num)

            # Pattern evaluation
            pattern_name, rev_pattern_num, rev_endpattern_num, rev_patt_eval, rev_patt_parse, rev_patt_err, pattern_list, varlist = sectionparse.pattern_parse(
                pattern_name, fwd, row, rev_pattern_num, rev_endpattern_num, rev_patt_eval, rev_patt_parse, rev_patt_err, rev_line_num, varlist)

        # If inside pattern
        if rev_patt_parse:

            # Dev notes evaluation
            ignore_text = commentparse.noteblock(
                fwd, comment_block_rx, comment_block_line_rx, row, open_notes)

            if ignore_text:
                continue

            # Body evaluation
            rev_body_num, rev_endbody_num, rev_body_eval, rev_parsing, rev_body_err = sectionparse.body_parse(
                fwd, row, rev_body_num, rev_endbody_num, rev_body_eval, rev_parsing, rev_body_err, rev_line_num)

            # If inside body
            if rev_parsing:

                # Check IF evaluations
                if re.match(end_if_rx, row):
                    rev_endif_count, rev_if_eval = sectionparse.open_match(
                        rev_endif_count, rev_if_eval)
                if re.match(if_rx, row):
                    rev_if_count, rev_if_eval = sectionparse.close_match(
                        rev_if_count, rev_if_eval)
                    rev_if_eval, rev_if_err = evaluations.loop_eval(
                        rev_if_eval, rev_if_err, rev_line_num)
                # Check FOR evaluations
                if re.match(end_for_rx, row):
                    rev_endfor_count, rev_for_eval = sectionparse.open_match(
                        rev_endfor_count, rev_for_eval)
                if re.match(for_rx, row):
                    rev_for_count, rev_for_eval = sectionparse.close_match(
                        rev_for_count, rev_for_eval)
                    rev_for_eval, rev_for_err = evaluations.loop_eval(
                        rev_for_eval, rev_for_err, rev_line_num)

tpl_file.close()

if (module_num > 1):
    print (" * More than 1 module declaration in this file!")
    for mod_err in mod_line:
        print ("    line %s" %mod_err)
elif (module_num == 0):
    print (" * Something wrong with module declaration!")

evaluations.eval(meta_eval, "metadata")
evaluations.eval(config_eval, "configuration")
evaluations.eval(defins_eval, "definitions")

evaluations.missing_warn(
    "overview", missing_ov, missing_endov, ov_err, endov_err, ov_count, pattern_num, pattern_list, has_ov)
evaluations.missing_warn(
    "trigger", missing_trig, missing_endtrig, trig_err, endtrig_err, trig_count, pattern_num, pattern_list, has_trigger)

if tags_err > 0:
    print(" * Missing tags declaration(s)...")
    for pattern in missing_tags:
        print ("    " + str(pattern))

if trig_on_err > 0:
    print(" * Missing trigger conditions...")
    for pattern in missing_trigon:
        print ("    " + str(pattern))

if (body_err or rev_body_err):
    printing.print_eval(
        "body", body_num, endbody_num, "body declarations", body_err, rev_body_err)

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
    printing.print_eval(
        "pattern", pattern_num, endpattern_num, "pattern declarations", patt_err, rev_patt_err)
else:
    print (" Number of patterns in file:           %s" %pattern_num)

print (" Number of logging statements:         %s" %logs)
print (" Number of comment lines:              %s" %comments)
print (" Number of runCommands:                %s" %runcmds)
print (" Number of fileGets:                   %s" %filegets)
print (" Number of listDirectorys:             %s" %listdirs)
print (" Number of fileInfos:                  %s" %fileinfos)
print (" Number of registryKeys:               %s" %regkeys)
total_vars += global_vars
total_vars = evaluations.uniq(total_vars)
varlen = len(total_vars)
print (" Number of variable assignments:       %s" %varlen)
print (" Number of definition blocks:          %s" %define_count)
print (" Number of SI types declared:          %s" %sis)
print (" Number of Detail types declared:      %s" %details)
print (" Number of Simple Identities:          %s" %sid_found)
print (" Number of imported modules:           %s" %imported)

if (if_err or rev_if_err):
    printing.print_eval(
        "if", if_count, endif_count, "IF evaluations", if_err, rev_if_err)
else:
    print (" Number of IF evaluations:             %s" %if_count)

if (for_err or rev_for_err):
    printing.print_eval(
        "for", for_count, endfor_count, "FOR loops", for_err, rev_for_err)
else:
    print (" Number of FOR loops:                  %s" %for_count)

if (table_err or rev_table_err):
    printing.print_eval(
        "table", table_count, endtable_count, "tables declared", table_err, rev_table_err)
else:
    print (" Number of tables declared:            %s" %table_count)

if initlist:
    evaluations.warnings(initlist, "Uninitialised variable(s) found")

if var_warn:
    var_warn = evaluations.uniq(var_warn)
    evaluations.warnings(
        var_warn, "Warning: Variable(s) in embedded if/for loops MAY be uninitialised")

if syntax_errs:
    evaluations.warnings(syntax_errs, "Syntax error in line(s) found")

if eca_errs:
    evaluations.warnings(
        eca_errs, "Warning: The syntax in these line(s) may cause an ECA Error")
    
print "\n"
