# https://python4astronomers.github.io/files/asciifiles.html

'''

function_01             ; some comment
    OPTCODE1 0x00       ; some other comment
    OPTCODE2 0x00
    NOP
    GOTO function_02    ; branch
    BRA function_02     ; comment

function_02             ; some new function
    SOME_OPTCODE 0x00   ; some new function
    SOME_OPTCODE 0x01


1. Read line
2. Strip comments after ';'
3. First line, load as function. How do we know function ends???
3. Scan function, if part of OPCODE list, add to edges lista
'''
from pprint import pprint

from graphviz import Digraph

f = open('sample.asm', 'r')

OPCODES = ('BRA', 'GOTO')
current_function = ''
previous_function = ''
edge_list = []
node_list = {}

for line in f:
    is_optcode = False
    line = line.rstrip() # strip '\n'

    current_line = line
    current_line = current_line.lstrip() # remove leading spaces

    # strip comment from line (';' delimiter)
    line, partition, comment = line.partition(';')

    # split line into sections
    line = line.split(" ")

    # ['function_001'] -> function
    # ['','','','','GOTO',...] -> within function

    # Detect function and add to node list
    if line[0] != '':
        #print(line[0])
        current_function = line[0]

    # Detect OPCODE in function
    if line[0] == '':
        #print(line[4])

        # Is OPCODE branch type?
        if line[4] in OPCODES:
            #print(line[5]) # function to branch/call
            #dot.edge(current_function, line[5])
            edge_list.append([current_function, line[5]])
            is_optcode = True


        # if line[4] text is same as opcode_branch_array
        # add edge from current function to current opcode
        # dot.edge('current_function', 'opcode')

    # create a new entry for the function
    if current_function not in node_list.keys():
        node_list.update({current_function:'<B>' + current_line + '</B>'})
    else:
        # if entry existed, append current line from function
        node_list[current_function] += '<BR ALIGN="LEFT"/>'
        if is_optcode:
            node_list[current_function] += '<FONT COLOR="MAROON"><I>' + current_line + '</I></FONT> '
        else:
            node_list[current_function] += current_line

    previous_function = current_function

pprint(edge_list)
pprint(node_list)

dot = Digraph(comment='Function List')
dot.node_attr['shape']='note'
dot.node_attr['fontname']='Monospace'

dot.edges(edge_list)
for node in node_list:
    dot.node(node, '<' + node_list[node] + '<BR ALIGN="LEFT"/>>')
dot.render('~/function_list.gv', view=True)