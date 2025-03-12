import re

def tokenize(code):
    token_specification = [
        ('COMMENT', r'#.*'),
        ('SELECT', r'select'),
        ('WHERE', r'where'),
        ('LIMIT', r'LIMIT'),
        ('VAR', r'\?[a-zA-z]+'),  
        ('IDS', r'[a-z]+:[a-zA-Z]+(\s"[^.]+)?'),
        ('SEP', r'\.'),
        ('LPARENT', r'\{'),
        ('RPARENT', r'\}'),
        ('NUM', r'\d+'),
        ('NEWLINE', r'\n'),
        ('SKIP', r'[ \t]+'),
        ('ERRO', r'.') 
    ]

    reg = '|'.join([f'(?P<{id}>{expreg})' for id, expreg in token_specification]) 
    reconhecidos = []
    linha = 1 
    mo = re.finditer(reg, code) 
    for m in mo:
        dic = m.groupdict()        
        if dic['SELECT']:
            t = ("SELECT", dic['SELECT'], linha, m.span())
        elif dic['WHERE']:
            t = ("WHERE", dic['WHERE'], linha, m.span())
        elif dic['LIMIT']:
            t = ("LIMIT", dic['LIMIT'], linha, m.span())
        elif dic['VAR']:
            t = ("VAR", dic['VAR'], linha, m.span())
        elif dic['IDS']:
            t = ("IDS", dic['IDS'], linha, m.span())
        elif dic['SEP']:
            t = ("SEP", dic['SEP'], linha, m.span())
        elif dic['LPARENT']:
            t = ("LPARENT", dic['LPARENT'], linha, m.span())
        elif dic['RPARENT']:
            t = ("RPARENT", dic['RPARENT'], linha, m.span())
        elif dic['NUM']:
            t = ("NUM", int(dic['NUM']), linha, m.span())
        elif dic['NEWLINE']:
            linha += 1
        elif dic['SKIP'] or dic['COMMENT']:
            pass 
        else: 
            t = ("ERRO", m.group(), linha, m.span())

        if not dic['SKIP'] and not dic['NEWLINE'] and not dic['COMMENT']:
            reconhecidos.append(t)
        
    
    return reconhecidos


code = """ # DBPedia: obras de Chuck Berry 

select ?nome ?desc where {
    ?s a dbo:MusicalArtist.
    ?s foaf:name "Chuck Berry"@en .
    ?w dbo:artist ?s.
    ?w foaf:name ?nome.
    ?w dbo:abstract ?desc
} LIMIT 100 """


for tok in tokenize(code):
    print(tok)
