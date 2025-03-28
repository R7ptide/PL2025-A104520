from expr_analex import lexer

prox_simb = ('Erro', '', 0, 0)

def parserError(simb):
    print("Erro sintático, token inesperado: ", simb)

def rec(simb):
    global prox_simb
    if prox_simb.type == simb:
        prox_simb = lexer.token()
    else:
        parserError(prox_simb)


def rec_Fator():
    global prox_simb
    if prox_simb and prox_simb.type == 'NUM':
        val = int(prox_simb.value)
        rec('NUM')
        return val
    elif prox_simb and prox_simb.type == 'PA':
        rec('PA')
        val = rec_Exp()
        rec('PF')
        return val
    else:
        parserError(prox_simb)


def rec_Termo2(val):
    global prox_simb
    if prox_simb and prox_simb.type == 'MULT':
        rec('MULT')
        val2 = rec_Fator()
        return rec_Termo2(val * val2)
    elif prox_simb and prox_simb.type == 'DIV':
        rec('DIV')
        val2 = rec_Fator()
        return rec_Termo2(val / val2)
    else:
        return val


def rec_Termo():
    val = rec_Fator()
    return rec_Termo2(val)


def rec_Exp2(val):
    global prox_simb
    if prox_simb and prox_simb.type == 'PLUS':
        rec('PLUS')
        val2 = rec_Termo()
        return rec_Exp2(val + val2)
    elif prox_simb and prox_simb.type == 'MINUS':
        rec('MINUS')
        val2 = rec_Termo()
        return(val - val2)
    else:
        return val    


def rec_Exp():
    val = rec_Termo()
    return rec_Exp2(val)


def rec_Parser(data):
    global prox_simb
    lexer.input(data)
    prox_simb = lexer.token()
    result = rec_Exp()
    return result
    