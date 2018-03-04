from graphviz import Digraph

dot = Digraph(comment='The Round Table')
dot.node_attr['shape']='note'
dot.node_attr['fontname']='Monospace'
dot.graph_attr['labeljust']='l'

dot.node('A', '<'
              'King Arthur<BR ALIGN="LEFT"/>And the Round Table'
              '>')
dot.node('B', 'Sir Bedevere the Wise')
dot.node('L', 'Sir Lancelot the Brave')

dot.edges(['AB', 'AL'])
dot.edge('B', 'L', constraint='false')

print(dot.source)

dot.render('~/round-table.gv', view=True)

