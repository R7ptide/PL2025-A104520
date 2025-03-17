import ply.lex as lex

tokens = (
    'VALOR',
    'LISTAR',
    'MOEDA',
    'SELECIONAR',
    'SAIR',
    'CODIGO',
    'VIRGULA',
    'PONTO',
)

def t_VALOR(t):
    r'2e|1e|50c|20c|10c|5c'
    return t

t_LISTAR = r'LISTAR'
t_MOEDA = r'MOEDA'
t_SELECIONAR = r'SELECIONAR'
t_SAIR = r'SAIR'
t_CODIGO = r'[A-Z]\d{2}'
t_VIRGULA = r','
t_PONTO = r'\.'
t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    t.lexer.skip(1)

lexer = lex.lex()