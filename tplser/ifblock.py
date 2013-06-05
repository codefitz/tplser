'''
A block of code initialised by 'if' containing variables declared inside the block.
block_num = the if block we are at
var = the variable used
if_eval = the level of embeddedness
e.g. if x then (0) if y then (1) end if; end if;
'''

class IfBlock(object):
    def __init__(self, block_num, if_eval, var):
        self.block = block_num
        self.eval = if_eval
        self.variable = var