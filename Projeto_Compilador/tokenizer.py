import os
import ply.lex as lex
import re

tokens = [
    'NUMBER',
    'RPARENT',
    'LPARENT',
    'RBRACKET',
    'LBRACKET',
    'COMMENT',
    'FRASE',
    'SEMICOLON',
    'DOT',
    'COLON',
    'EQUALS',
    'ATTRIB',
    "GREATER",
    "GE",
    "LESSER",
    "LE",
    "COMMA",
    "TIMES",
    "PLUS",
    "MINUS",
    'ID',
    'VAR',
    'PROGRAM',
    'BEGIN',
    'END',
    'WRITELN',
    'INTEGER',
    'REAL',
    'BOOLEAN',
    'STRING',
    'WRITE',
    'READLN',
    'LENGTH',
    'DOWNTO',
    'IF',
    'THEN',
    'ELSE',
    'FOR',
    'TO',
    'DO',    
    'WHILE',
    'AND',    
    'NOT',
    'DIV',
    'MOD',
    'DIVIDE',
    'NOTEQUAL',
    'ARRAY',
    'OF',
    'FUNCTION',
    'RANGE', 
    'TRUE',
    'FALSE',
    'OR'
]

t_LPARENT = r'\('
t_RPARENT = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_FRASE = r'\'([^\']*)\'|\"([^\"]*)\"'  # Aspas simples ou duplas para strings
t_NUMBER = r'\d+(\.\d+)?'
t_SEMICOLON = r'\;'
t_DOT = r'\.'
t_COLON = r':'
t_EQUALS = r'='
t_GREATER = r'>'
t_LESSER = r'<'
t_COMMA = r','
t_TIMES = r'\*'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_RANGE = r'\.\.'
t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

# Funções para reconhecer palavras com mais prioridade
def t_TRUE(t):
    r'true'
    return t

def t_FALSE(t):
    r'false'
    return t

def t_VAR(t):
    r'var'
    return t

def t_PROGRAM(t):
    r'program'
    return t

def t_BEGIN(t):
    r'begin'
    return t

def t_END(t):
    r'end'
    return t

def t_WRITELN(t):
    r'writeln'
    return t

def t_INTEGER(t):
    r'integer'
    return t

def t_REAL(t):
    r'real'
    return t

def t_BOOLEAN(t):
    r'boolean'
    return t

def t_STRING(t):
    r'string'
    return t

def t_WRITE(t):
    r'write'
    return t

def t_READLN(t):
    r'readln'
    return t

def t_LENGTH(t):
    r'length'
    return t

def t_DOWNTO(t):
    r'downto'
    return t

def t_IF(t):
    r'if'
    return t

def t_THEN(t):
    r'then'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_FOR(t):
    r'for'
    return t

def t_OR(t):
    r'or'
    return t

def t_TO(t):
    r'to'
    return t

def t_DO(t):
    r'do'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_AND(t):
    r'and'
    return t

def t_NOT(t):
    r'not'
    return t

def t_DIV(t):
    r'div'
    return t

def t_MOD(t):
    r'mod'
    return t

def t_ARRAY(t):
    r'array'
    return t

def t_OF(t):
    r'of'
    return t

def t_FUNCTION(t):
    r'function'
    return t

def t_GE(t):
    r'>='
    return t

def t_LE(t):
    r'<='
    return t

def t_NOTEQUAL(t):
    r'<>'
    return t

def t_DIVIDE(t):
    r'\/'
    return t

def t_ATTRIB(t):
    r':='
    return t

def t_COMMENT(t):
    r'{.*}'
    pass  # Ignora comentários, não retorna o token

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'  # Espaços e tabs são ignorados

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

# a flag re.IGNORECASE é usada para tornar o lexer case-insensitive
# (ou seja, as palavras podem ser escritas em qualquer combinação de maiúsculas e minúsculas)
lexer = lex.lex(reflags=re.IGNORECASE)

def tokenize_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            codigo = f.read()
        
        # Reset do lexer
        lexer.lineno = 1
        lexer.input(codigo)
        
        print(f"=== Tokens encontrados no arquivo: {file_path} ===\n")
        
        # Iterar pelos tokens e imprimir
        for tok in lexer:
            value = tok.value.replace("\n", "\\n")
            print(f"LexToken({tok.type}, '{value}', {tok.lineno}, {tok.lexpos})")
            
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não encontrado!")
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Uso: python tokenizer.py <arquivo.pas>")
        print("Exemplo: python tokenizer.py teste.pas")
        sys.exit(1)
    
    file_path = sys.argv[1]
    tokenize_file(file_path)