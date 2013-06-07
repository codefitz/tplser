import re

def notes(direction, comment_rx, comment_line_rx, line, open):
    if re.match(comment_rx, line):
        if direction:
            if open > 0:
                ignore_text = False
                open -= 1
            else:
                ignore_text = True
                open += 1
            if re.search(comment_line_rx, line):
                ignore_text = False
                open -= 1
        else:
            if re.match(comment_line_rx, line):
                ignore_text = False
            if open == 0:
                ignore_text = True
                open += 1
            else:
                open -= 1
                ignore_text = False
                
        return ignore_text