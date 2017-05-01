#!/usr/bin/env python
#
# Author: Wes Fitzpatrick (github@wafitz.net)
#

# Standard modules
import re
import sys

# Local modules
import tplser

pyver = sys.version_info

if pyver >= (2, 7, 0):
    import argparse

    parser = argparse.ArgumentParser()
    tpl_file = tplser.tplfile.tplfile
    parser.add_argument('*.tpl', type=tpl_file)
    args = parser.parse_args()
else:
    if len(sys.argv) < 2:
        sys.exit("You must specify a *tpl file!\n")

print("\nNow parsing " + str(sys.argv[1]) + "...\n")

body_parsing, rev_parsing, pattern_parsing, rev_patt_parse, tpl_parsing, fwd = [False] * 6
pattern_name = ""

# pdb.set_trace()

with open(sys.argv[1]) as tpl_file:
    ###########################
    # == Read Lines Forward ==#
    ###########################

    (module_num, endpattern_num, pattern_num, line_num, body_num, endbody_num, if_block, patt_eval, if_eval, for_eval,
     ov_eval, trig_eval, body_eval, meta_eval, table_eval, config_eval, defins_eval, warn_count, logs, runcmds,
     filegets, open_notes, comments, sis, details, imported, listdirs, fileinfos, regkeys, if_count, endif_count,
     for_count, endfor_count, ov_count, endov_count, trig_count, endtrig_count, table_count, unterminated_count,
     define_count, ov_err, endov_err, tags_err, trig_err, endtrig_err, trig_on_err, endtable_count, sids_err, sid_eval,
     sid_count, endsid_count, sid_found) = [0] * 52

    (patt_err, if_err, for_err, body_err, table_err, sid_err, lines, mod_line, ov_pattern, trig_pattern, eca_errs,
     missing_trig, missing_endtrig, missing_trigon, has_trigger, has_ov, initlist, used, imports, unterminated,
     var_warn, warn_list, for_warn_list, syntax_errs, missing_ov, missing_endov, missing_tags, missing_sid,
     missing_sids, has_sid, pattern_list) = ([] for i in range(31))

    (ov_tags, trig_on, ignore_text, constants, defins, open_bracket, end_imports, trigger, assign_eval, var_warning,
     else_clause, sid_tags, for_block, open_assignment, stop_pattern, last_pattern, tpl_ver) = [False] * 17

    defins_var, ob_line, trig_line, import_line, var_line, no_quotes, config_var = [""] * 7

    # For storing custom variables declared in pattern, predefined keywords added here:
    (global_vars, total_vars, varlist, if_close_pattern, constant_vars, vars_assigned, utilised, model_lines,
     config_funcs, defins_funcs) = ([] for j in range(10))

    # Pre-defined TPL Keywords
    keyword_list = ['model', 'discovery', 'import', 'module', 'overrides', 'end', 'then', 'on', 'from', 'log', 'search',
                    'do', 'definitions', 'aged', 'as', 'at', 'break', 'by', 'continue', 'created', 'default', 'defined',
                    'deleted', 'desc', 'exists', 'expand', 'explode', 'false', 'flags', 'is', 'locale', 'modified',
                    'nodecount', 'nodes', 'none', 'order', 'out', 'processwith', 'relationship', 'removal', 'requires',
                    'show', 'step', 'stop', 'substring', 'subword', 'summary', 'tags', 'taxonomy', 'traverse', 'true',
                    'unconfirmed', 'with', 'where', 'matches', 'and', 'not', 'or', 'has', 'in', 'raw', 'regex',
                    'unix_cmd', 'windows_cmd', 'tpl', 'identify', 'constants', 'pattern', 'triggers', 'body', 'table',
                    'configuration', 'metadata', 'define', 'overview', 'if', 'for', 'else', 'elif', 'function', 'text',
                    'time', 'size']

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
    sp_chars_rx = re.compile("(\w+),?[\[.]")
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

        line_num += 1

        # Count of comments
        if re.match("^\s*//", full_line):
            comments += 1

        # Strip comments
        line = tplser.commentparse.removal(full_line, double_quotes_rx, single_quotes_rx)

        # Ignore developer notes block
        ignore_text = tplser.commentparse.noteblock(
            fwd, comment_block_rx, comment_block_line_rx, line, open_notes)

        if ignore_text:
            continue
        else:

            # Imports - Join all import lines
            import_dec = re.search(import_rx, line)

            if import_dec:
                imported += 1
                import_line = line
                imports = True

            # Import line complete, get all variables
            if imports:
                if ";" not in import_line:
                    import_line += " " + str.strip(line)
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
                table_count, table_eval = tplser.sectionparse.open_match(
                    table_count, table_eval)

            # Configuration evaluation
            option = False  # This option is not used by config eval - just a holder for the function
            tpl_parsing, global_vars, option, config_funcs = tplser.sectionparse.section(
                config_rx, end_config_rx, line, config_eval, config_var_rx, global_vars, option, tpl_parsing,
                config_funcs)

            # Definitions evaluation
            tpl_parsing, global_vars, defins, defins_funcs = tplser.sectionparse.section(
                definitions_rx, end_definitions_rx, line, defins_eval, def_vars_rx, global_vars, defins, tpl_parsing,
                defins_funcs)

            # Definition statements
            if defins:
                define = line
                define_var = re.search(def_var_rx, define)
                if define_var:
                    define_count += 1

            # Count of logs
            if re.match(log_rx, line):
                logs += 1

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
                sid_count, sid_eval, has_sid, sid_tags = tplser.sectionparse.open_requireds(
                    pattern_name, line, sid_count, sid_eval, has_sid, sid_tags)

            # Count of simple ids
            if sid_eval > 0:
                if "simple_identity;" in line:
                    pass  # guide line
                elif "->" in line:
                    sid_found += 1

            # Pattern evaluation
            pattern_name, pattern_num, endpattern_num, patt_eval, pattern_parsing, patt_err, pattern_list, varlist = \
                tplser.sectionparse.pattern_parse(pattern_name, True, line, pattern_num, endpattern_num, patt_eval,
                                                  pattern_parsing, patt_err, line_num, varlist)

        # Configuration evaluation
        option = False  # This option is not used by config eval - just a holder for the function
        tpl_parsing, global_vars, option, config_funcs = tplser.sectionparse.section(
            config_rx, end_config_rx, line, config_eval, config_var_rx, global_vars, option, tpl_parsing,
            config_funcs)

        # Definitions evaluation
        tpl_parsing, global_vars, defins, defins_funcs = tplser.sectionparse.section(
            definitions_rx, end_definitions_rx, line, defins_eval, def_vars_rx, global_vars, defins, tpl_parsing,
            defins_funcs)

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
                ov_count, ov_eval, has_ov, ov_tags = tplser.sectionparse.open_requireds(
                    pattern_name, line, ov_count, ov_eval, has_ov, ov_tags)

            # Count of tags
            if re.match(tags_rx, line):
                ov_tags = True

            if re.search(end_overview_rx, line):
                endov_count, ov_eval, missing_ov, ov_err, missing_tags, tags_err = tplser.sectionparse.close_requireds(
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
                    # Grab everything to the left of the seperator
                    left = re.findall("(\S+)\s*:=", line)
                    for var in left:
                        if var in constant_vars:
                            syntax_errs.append(
                                str(line_num) + ", Constant " + str(var) + " has been redefined:\n      " + str.strip(
                                    line))
                        else:
                            constant_vars.append(var)
            else:
                # Reset after section is complete for the next pattern
                constant_vars = []

            # Trigger evaluation
            if re.match(triggers_rx, line):
                trig_count, trig_eval, has_trigger, trig_on = tplser.sectionparse.open_requireds(
                    pattern_name, line, trig_count, trig_eval, has_trigger, trig_on)

            # Check for trigger condition
            if re.match(trigger_on_rx, line):
                trig_on = True
                varlist.append(re.search(global_var_rx, line).group(1))

            if re.search(end_trigger_rx, line):
                endtrig_count, trig_eval, missing_trig, trig_err, missing_trigon, trig_on_err = \
                    tplser.sectionparse.close_requireds(pattern_name, line, endtrig_count, trig_eval, missing_trig,
                                                        trig_err, trig_on, missing_trigon, trig_on_err)

            # Body evaluation
            body_num, endbody_num, body_eval, body_parsing, body_err = tplser.sectionparse.body_parse(
                True, line, body_num, endbody_num, body_eval, body_parsing, body_err, line_num)

            # If inside body
            if body_parsing:

                # Check end ov
                ov_eval, missing_endov, endov_err = tplser.sectionparse.closing_decs(
                    ov_eval, missing_endov, pattern_name, endov_err)
                # Check end trigger
                trig_eval, missing_endtrig, endtrig_err = tplser.sectionparse.closing_decs(
                    trig_eval, missing_endtrig, pattern_name, endtrig_err)

                # Set general TPL parsing
                tpl_parsing = True
                # print ("Current valist is:\n" + str(varlist))

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
                if_count, if_eval = tplser.sectionparse.open_match(if_count, if_eval)

            # Check FOR evaluations
            if re.match(for_rx, line):
                for_count, for_eval = tplser.sectionparse.open_match(for_count, for_eval)

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
                if re.search(syntax_rx, no_quotes):  # missing colon (:)
                    syntax_errs.append(str(line_num) + ": " + str.strip(line))

            if ":=" in line:
                open_assignment = True

            if open_assignment and ";" not in line:
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

            # print var_line

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
                            assigner -= 1  # Don't count any ':=' chars between quotes

                # Check to see if it belongs to a function, multiple assigners are expected
                if assigner > 1:
                    defin = re.compile(":=\s*%s\." % defins_var)
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
                        # print "line " + str(var_ln) + ": " + str(var_line)
                        # print "=========================================="
                        syntax_errs.append(str(var_ln) + ": " + str.strip(var_line))

                # Get variables assigned

                var = ""
                vas = re.findall(vars_rx, var_line)
                for var in vas:
                    # print (str(line_num) + ", assigning var " + str(var) + " to varlist")
                    varlist.append(var)

                var = re.search(for_rx, var_line)
                if var:
                    for_block = True
                    # print (str(line_num) + ", assigning var " + str(var) + " to varlist")
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
                        warn = tplser.ifblock.IfBlock(if_block, if_eval, var)
                        warn_list.append(warn)
                        for_block = False
                    else:
                        varlist.append(var)

                for var in varlist:
                    total_vars.append(var)

tpl_file.close()

print("\n ===PATTERN MODULE STATISTICS===\n")

if not tpl_ver:
    pass
else:
    print(" TPL Version: " + str(tpl_ver) + "\n")

print(" Lines:                      %s" % line_num)
print(" Patterns:                   %s" % pattern_num)
print(" IF evaluations:             %s" % if_count)
print(" FOR loops:                  %s" % for_count)
print(" Tables:                     %s" % table_count)
print(" Log Statements:             %s" % logs)
print(" Comment Lines:              %s" % comments)
print(" runCommands:                %s" % runcmds)
print(" fileGets:                   %s" % filegets)
print(" listDirectorys:             %s" % listdirs)
print(" fileInfos:                  %s" % fileinfos)
print(" registryKeys:               %s" % regkeys)
total_vars += global_vars
total_vars = tplser.evaluations.uniq(total_vars)
varlen = len(total_vars)
print(" Variables:                  %s" % varlen)
print(" Definition Blocks:          %s" % define_count)
print(" Software Instances:         %s" % sis)
print(" Details:                    %s" % details)
print(" Simple Identities:          %s" % sid_found)
print(" Imported Modules:           %s" % imported)

print("\n")
