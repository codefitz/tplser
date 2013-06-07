import re

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