# https://python4astronomers.github.io/files/asciifiles.html

'''

    CODE                ; some text

; text
function_01:            ; some comment
    OPTCODE1 0x00       ; some other comment
    OPTCODE2 0x00
    NOP
    GOTO function_02    ; branch
    BRA function_02     ; comment

function_02:            ; some new function
    SOME_OPTCODE 0x00   ; some new function
    SOME_OPTCODE 0x01


TODO:
1. remove any text after ';' on current line
2. skip if blank line
3. remove ':' from functions
4. start processing functions when first encountered
5. start from line 50
6. format to upper case
'''
from pprint import pprint

from graphviz import Digraph

f = open('program.asm', 'r')

OPCODES = ('BRA', 'GOTO', 'CALL')
current_function = ''
previous_function = ''
edge_list = []
node_list = {}

# skip header
for index in range(50):
    f.__next__()

for line in f:
    is_optcode = False
    line = line.rstrip() # strip '\n'

    current_line = line
    current_line = current_line.strip() # remove leading and trailing spaces

    if current_line == '':
        continue

    if current_line[0] == ';':
        continue

    # is there leading blank?
    if line[0] != ' ':
        # its a function call, save
        current_function, partition, comment = line.partition(':')
    else:
        # its a opcode, check
        optcode = current_line.split()
        optcode_formatted = optcode[0].upper()
        if optcode.__len__() <= 1:
            continue # TODO dont skip entry
        optcode_function = optcode[1].upper()
        if optcode_formatted in OPCODES:
            is_optcode = True
            edge_list.append([current_function.lower(), optcode_function.lower()])

    '''
    # strip comment from line (';' delimiter)
    line, partition, comment = line.partition(';')

    # split line into sections
    line = line.split(" ")

    # Detect function and add to node list
    if line[0] != '':
        #print(line[0])
        current_function = line[0]

    # Detect OPCODE in function
    if line[0] == '' and line.__len__() > 8:
         # Is OPCODE branch type?
        if line[8] in OPCODES:
            edge_list.append([current_function, line[5]])
            is_optcode = True
    '''

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
#dot.format = 'png'

dot.edges(edge_list)
for node in node_list:
    dot.node(node, '<' + node_list[node] + '<BR ALIGN="LEFT"/>>')
dot.render('test-output/function_list.gv', view=True)