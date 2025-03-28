import ply.lex as lex

tokens = (
    'PA',
    'PF',
    'PLUS',
    'MINUS',
    'MULT',
    'DIV',
    'NUM'
)

t_PA = r'\('
t_PF = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'\/'
t_NUM = r'\d+'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = '\t '

def t_error(t):
    print('Carácter desconhecido: ', t.value[0], 'Linha: ', t.lexer.lineno)
    t.lexer.skip(1)

lexer = lex.lex()
