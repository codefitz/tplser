import re
import evaluations
pattern_list = []

'''
    Function to handle configuration, definition and other special sections of
    TPL pattern.
'''
def section(start_rx, end_rx, line, eval, var_rx, global_vars, option, tpl_parsing):
    start = re.search(start_rx, line)
    if start:
        option = True
        eval += 1
        var = re.match(var_rx, line)
        if var:
            global_vars.append(var.group(1))
        tpl_parsing = True

    end = re.search(end_rx, line)
    if end:
        option = False
        eval -= 1
        tpl_parsing = False
    
    return tpl_parsing, global_vars, option

'''
    Function for parsing the pattern block.
'''
def pattern_parse(name, direction, line, num, end_num, eval, parse, err, line_num):
    if re.match("^\s*pattern\s\S+\s\d+\.\d", line):
        if direction:
            pname = re.findall("pattern\s(.*\s\d+\.\d)", line)
            name = pname[0]
            pattern_list.append(name)
            print (" Checking pattern... " + name)
            num += 1
            eval += 1
            parse = True
        else:
            num += 1
            eval -= 1
            eval = evaluations.loop_eval(eval, err, line_num)
            parse = False
    if re.match("^\s*end\spattern;", line):
        if direction:
            end_num += 1
            eval -= 1
            eval = evaluations.loop_eval(eval, err, line_num)
            parse = False 
        else:
            num += 1
            eval += 1
            parse = True
    return name, num, end_num, eval, parse, err, pattern_list

'''
    Function to parse the body section.
'''
def body_parse(direction, line, num, end_num, eval, parse, err, line_num):
    if re.match("^\s*body\s*$", line):
        if direction:
            num += 1
            eval += 1
            parse = True
        else:
            num += 1
            eval -= 1
            eval = evaluations.loop_eval(eval, err, line_num)
            parse = False
    elif re.match("^\s*end\sbody;", line):
        if direction:
            end_num += 1
            eval -= 1
            eval = evaluations.loop_eval(eval, err, line_num)
            parse = False
        else:
            num += 1
            eval += 1
            parse = True
    return num, end_num, eval, parse, err
    
'''
    Function to check for section opener
'''
def open_match(count, eval):
    count += 1
    eval += 1
    return count, eval

'''
    Function to check for section closer
'''
def close_match(count, eval):
    count += 1
    eval -= 1
    return count, eval

'''
    Function for checking opener to a section with attributes
'''
def open_requireds(pattern_name, line, count, eval, found, attr):
    count += 1
    eval += 1
    found.append(pattern_name)
    attr = False
    return count, eval, found, attr

'''
    Get a list of attibutes e.g. overview tags
'''
def close_requireds(pattern_name, line, count, eval, missing, err, attr, missing_attr, attr_err):
    count += 1
    eval -= 1
    if (eval < 0):
        missing.append(pattern_name)
        eval = 0
        err += 1
    if not attr:
        missing_attr.append(pattern_name)
        attr_err += 1
    return count, eval, missing, err, missing_attr, attr_err

'''
    Close section with attributes
'''
def closing_decs(eval, missing_end, pattern_name, err):
    if (eval > 0):
        missing_end.append(pattern_name)
        eval = 0
        err += 1
    return eval, missing_end, err