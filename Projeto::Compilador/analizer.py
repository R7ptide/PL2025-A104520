from tokenizer import tokens
import ply.yacc as yacc
import os

TRUE = 1
FALSE = 0

tabela_de_simbolos = {}
next_index = 0
if_counter = 0
for_counter = 0
while_counter = 0
string_counter = 0

def p_program(p):
    'program : header block DOT'
    p[0] = f"{p[1]}START:\n{p[2]}STOP"

def p_header(p):
    'header : PROGRAM ID SEMICOLON variables'
    p[0] = p[4]  

def p_variables(p):
    'variables : VAR varDecls'
    p[0] = p[2]

def p_variables_2(p):
    'variables : empty'
    p[0] = ""

def p_varDecls(p):
    'varDecls : varDeclaration varDecls'
    p[0] = p[1] + p[2]

def p_varDecls_empty(p):
    'varDecls : empty'
    p[0] = ""

def p_varDeclaration(p):
    'varDeclaration : idList COLON type SEMICOLON'
    var_names = p[1]
    var_type = p[3] 

    vars = ""
    global next_index
    for var in var_names:
        tabela_de_simbolos[var] = (var_type, next_index)
        next_index += 1 

        if var_type == "INTEGER":
            vars += f"    PUSHI 0\n"
        elif var_type == "REAL":
            vars += f"    PUSHF 0.0\n"
        elif var_type == "BOOLEAN":
            vars += f"    PUSHI {FALSE}\n"
        elif var_type == "STRING":
            ## Espaço para o array, valor da string original, iterador da string , tamanho da string
            global string_counter
            vars += f"    PUSHI 0\n    PUSHI 0\n    PUSHI 0\n    PUSHI 0\n" 
            tabela_de_simbolos[var] = ((var_type,string_counter),next_index-1)
            tabela_de_simbolos["string" + str(string_counter)] = ("STRING",next_index)
            next_index += 1
            tabela_de_simbolos["indice" + str(string_counter)] = ("INTEGER",next_index)
            next_index += 1
            tabela_de_simbolos["size" + str(string_counter)] = ("INTEGER",next_index)
            next_index += 1
            string_counter += 1 
        elif isinstance(var_type, tuple) and var_type[0] == "ARRAY":
            _, base_type, size = var_type
            vars += f"    ALLOC {size}\n"
    
    p[0] = vars

def p_idList(p):
    'idList : ID idListTail'
    p[0] = [p[1]] + p[2] 

def p_idListTail(p):
    'idListTail : COMMA ID idListTail'
    p[0] = [p[2]] + p[3] 

def p_idListTail_empty(p):
    'idListTail : empty'
    p[0] = []

def p_type(p):
    'type : baseType'
    p[0] = p[1]

def p_type_array(p):
    'type : arrayType'
    p[0] = p[1]

def p_arrayType(p):
    'arrayType : ARRAY LBRACKET NUMBER RANGE NUMBER RBRACKET OF baseType'
    lower = int(p[3])
    upper = int(p[5])
    base_type = p[8]
    size = upper - lower + 1

    p[0] = ("ARRAY", base_type, size)

def p_baseType(p):
    'baseType : INTEGER'
    p[0] = "INTEGER"

def p_type_2(p):
    'baseType : REAL'
    p[0] = "REAL"

def p_type_3(p):
    'baseType : BOOLEAN'
    p[0] = "BOOLEAN"

def p_type_4(p):
    'baseType : STRING'
    p[0] = "STRING"

def p_block(p):
    'block : BEGIN contentList END'
    p[0] = p[2] 

def p_contentList(p):
    'contentList : content contentTail'
    p[0] = p[1] + p[2]

def p_contentList_empty(p):
    'contentList : empty'
    p[0] = ""

def p_contentTail(p):
    'contentTail : SEMICOLON contentList'
    p[0] = p[2]

def p_contentTail_empty(p):
    'contentTail : empty'
    p[0] = ""


def p_content(p):
    'content : openStatement'
    p[0] = p[1]

def p_content_2(p):
    'content : closedStatement'
    p[0] = p[1]

def p_openStatement(p):
    'openStatement : IF booleanexpression THEN content'
    global if_counter

    end_label = f'ENDIF{if_counter}'
    if_counter += 1
   
    code = p[2] # Verfica a expressão booleana
    code += f"    JZ {end_label}\n" # Caso seja falsa salta para o bloco else 
    code += p[4] # Caso seja verdadeiro executamos o código

    code += f"{end_label}:\n"  # End label
    p[0] = code

def p_openStatement_else(p):
    'openStatement : IF booleanexpression THEN closedStatement ELSE openStatement'
    global if_counter

    else_label = f'ELSEBLOCK{if_counter}'
    end_label = f'ENDIF{if_counter}'
    if_counter += 1
   
    code = p[2] # Verfica a expressão booleana
    code += f"    JZ {else_label}\n" # Caso seja falsa salta para o bloco else 
    code += p[4] # Caso seja verdadeiro executamos o código

    code += f"    JUMP {end_label}\n"

    code += f"{else_label}:\n"  # Rótulo do bloco else
    code += p[6]  # Código do bloco ELSE (se existir)
    code += f"{end_label}:\n"  # End label
    p[0] = code

def p_openStatement_while(p):
    'openStatement : WHILE booleanexpression DO openStatement'
    global while_counter

    while_label = f'WHILEBLOCK{while_counter}'
    end_label = f'ENDWHILE{while_counter}'
    while_counter += 1

    code = f"{while_label}:\n"
    code += p[2] 
    code += f"    JZ {end_label}\n"  
    code += p[4]
    code += f"    JUMP {while_label}\n"
    code += f"{end_label}:\n"

    p[0] = code

def p_openStatement_for(p):
    'openStatement : FOR ID ATTRIB expression forDirection expression DO openStatement'
    global for_counter

    for_label = f'FORBLOCK{for_counter}'
    for_counter += 1

    # declarar variavel de controlo
    var_type, var_indice = tabela_de_simbolos[p[2]]
    code = p[4]
    code += f"    STOREG {var_indice}\n"
    # executar o bloco
    code += f"{for_label}:\n"
    code += p[8]
    # atualizar a variavel de controlo
    code += f"    PUSHG {var_indice}\n"
    code += f"    PUSHI 1\n"
    if p[5] == "TO":
        code += f"    ADD\n"
    elif p[5] == "DOWNTO":
        code += f"    SUB\n"
    code += f"    STOREG {var_indice}\n"
    # verificar se a variavel de controlo chegou ao limite
    code += f"    PUSHG {var_indice}\n"
    code += p[6]
    if p[5] == "TO":
        code += f"    SUP\n"
    elif p[5] == "DOWNTO":
        code += f"    INF\n"
    code += f"    JZ {for_label}\n"

    p[0] = code

def p_closedStatement(p):
    'closedStatement : simpleStatement'
    p[0] = p[1]

def p_closedStatement_block(p):
    'closedStatement : block'
    p[0] = p[1]

def p_closedStatement_else(p):
    'closedStatement : IF booleanexpression THEN closedStatement ELSE closedStatement'
    global if_counter

    else_label = f'ELSEBLOCK{if_counter}'
    end_label = f'ENDIF{if_counter}'
    if_counter += 1
   
    code = p[2] # Verfica a expressão booleana
    code += f"    JZ {else_label}\n" # Caso seja falsa salta para o bloco else 
    code += p[4] # Caso seja verdadeiro executamos o código

    code += f"    JUMP {end_label}\n"

    code += f"{else_label}:\n"  # Rótulo do bloco else
    code += p[6]  # Código do bloco ELSE (se existir)
    code += f"{end_label}:\n"  # End label
    p[0] = code

def p_closedStatement_while(p):
    'closedStatement : WHILE booleanexpression DO closedStatement'
    global while_counter

    while_label = f'WHILEBLOCK{while_counter}'
    end_label = f'ENDWHILE{while_counter}'
    while_counter += 1

    code = f"{while_label}:\n"
    code += p[2]
    code += f"    JZ {end_label}\n"
    code += p[4]
    code += f"    JUMP {while_label}\n"
    code += f"{end_label}:\n"

    p[0] = code

def p_closedStatement_for(p):
    'closedStatement : FOR ID ATTRIB expression forDirection expression DO closedStatement'
    global for_counter

    for_label = f'FORBLOCK{for_counter}'
    for_counter += 1

    # declarar variavel de controlo
    var_type, var_indice = tabela_de_simbolos[p[2]]
    code = p[4]
    code += f"    STOREG {var_indice}\n"
    # executar o bloco
    code += f"{for_label}:\n"
    code += p[8]
    # atualizar a variavel de controlo
    code += f"    PUSHG {var_indice}\n"
    code += f"    PUSHI 1\n"
    if p[5] == "TO":
        code += f"    ADD\n"
    elif p[5] == "DOWNTO":
        code += f"    SUB\n"
    code += f"    STOREG {var_indice}\n"
    # verificar se a variavel de controlo chegou ao limite
    code += f"    PUSHG {var_indice}\n"
    code += p[6]
    if p[5] == "TO":
        code += f"    SUP\n"
    elif p[5] == "DOWNTO":
        code += f"    INF\n"
    code += f"    JZ {for_label}\n"

    p[0] = code


def p_simpleStatement(p):
    'simpleStatement : WRITELN LPARENT writeArgs RPARENT'
    p[0] = p[3] + "    WRITELN\n"

def p_simpleStatement_2(p):
    'simpleStatement : WRITE LPARENT writeArgs RPARENT'
    p[0] = p[3]

def p_writeArgs(p):
    'writeArgs : singleArg moreArgs'
    p[0] = p[1] + p[2]

def p_moreArgs(p):
    'moreArgs : COMMA singleArg moreArgs'
    p[0] = p[2] + p[3]


def p_moreArgs_2(p):
    'moreArgs : empty'
    p[0] = ""

def p_singleArg(p):
    'singleArg : FRASE'
    string = p[1][1:-1]
    p[0] = f"    PUSHS \"{string}\"\n    WRITES\n"

def p_singleArg_2(p):
    'singleArg : ID idTail'
    var_name = p[1]
    if var_name in tabela_de_simbolos:
        var_type, var_indice = tabela_de_simbolos[var_name]
        
        if p[2] == "":  # Variável simples sem índice
            code = f"    PUSHG {var_indice}\n"
            if var_type == "INTEGER":
                code += "    WRITEI\n"
            elif var_type == "REAL":
                code += "    WRITEF\n"
            elif var_type == "BOOLEAN":
                code += "    WRITEI\n"  # Trata booleanos como inteiros
            else:
                code += "    WRITES\n"  # Default para outros tipos
            p[0] = code
        else:  # Array com índice
            if isinstance(var_type, tuple) and var_type[0] == "ARRAY":
                _, base_type, _ = var_type
                code = f"    PUSHG {var_indice}\n"
                # Código para calcular o índice do array e carregar o valor
                code += p[2]  # expression para o índice
                code += f"    LOADN\n"  # Carregar o valor do array
                if base_type == "INTEGER":
                    code += "    WRITEI\n"
                elif base_type == "REAL":
                    code += "    WRITEF\n"
                elif base_type == "BOOLEAN":
                    code += "    WRITEI\n"
                else:
                    code += "    WRITES\n"
                p[0] = code
            else:
                print(f"Erro: '{var_name}' não é um array")
                p[0] = ""
    else:
        print(f"Erro: Variável '{var_name}' não declarada")
        p[0] = ""

def p_simpleStatement_3(p):
    'simpleStatement : READLN LPARENT readIdOrArray RPARENT'
    p[0] = p[3]
    
def p_readIdOrArray(p):
    'readIdOrArray : ID idTail'
    var_name = p[1]

    if var_name in tabela_de_simbolos:
        var_type, indice = tabela_de_simbolos[var_name]
        if p[2] == "":
            if isinstance(var_type,tuple) and var_type[0] == "STRING":
                type,counter = var_type
                var_type_2, indice_2 = tabela_de_simbolos["string" + str(counter)]
                var_type_3, indice_3 = tabela_de_simbolos["indice" + str(counter)]
                var_type_size, indice_size = tabela_de_simbolos["size" + str(counter)]
                code = f"    READ\n"
                code += f"    STOREG {indice_2}\n"
                code += f"    PUSHG{indice_2}\n"
                code += f"    STRLEN\n"
                code += f"    STOREG {indice_size}\n"
                code += f"    PUSHG{indice_size}\n"
                code += f"    ALLOCN\n"
                code += f"    STOREG {indice}\n"
            
                code += f"    LOOPSTRING{counter}:\n"
                code += f"    PUSHG {indice_3}\n"
                code += f"    PUSHG {indice_size}\n"
                code += f"    INF\n"
                code += f"    JZ ENDSTRING{counter}\n"

                code += f"    PUSHG {indice}\n"
                code += f"    PUSHG {indice_3}\n"
                code += f"    PUSHG {indice_2}\n"
                code += f"    PUSHG {indice_3}\n"
                code += f"    CHARAT\n"
                code += f"    STOREN\n"

                code += f"    PUSHG {indice_3}\n"
                code += f"    PUSHI 1\n"
                code += f"    ADD\n"
                code += f"    STOREG {indice_3}\n"
                code += f"    JUMP LOOPSTRING{counter}\n"
                code += f"    ENDSTRING{counter}:\n"

                p[0] = code
            elif var_type == "INTEGER":
                p[0] = f"    READ\n    ATOI\n    STOREG {indice}\n"
            elif var_type == "REAL":
                p[0] = f"    READ\n    ATOF\n    STOREG {indice}\n"
          
        elif isinstance(var_type, tuple) and var_type[0] == "ARRAY":
            code = f"    PUSHG {indice}\n"
            code += p[2]
            code += f"    READ\n    ATOI\n    STOREN\n"
            p[0] = code

def p_idTail(p):
    'idTail : LBRACKET expression RBRACKET'
    code = p[2]    # calculo do indice
    code += f"    PUSHI 1\n"  # Atualizar índice, na VM começa em 0
    code += f"    SUB\n"
    p[0] = code

def p_idTail_empty(p):
    'idTail : empty'
    p[0] = ""
        
def p_simpleStatement_5(p):
    'simpleStatement : attribIdOrArray ATTRIB expression'
    var = p[1]
    if isinstance(var, tuple) and var[0] == "array":
        code = var[1]
        code += p[3]
        code += f"    STOREN\n"
        p[0] = code
    else:
        code = p[3]
        code += p[1]  # Código para atribuição
        p[0] = code

def p_attribIdOrArray(p):
    'attribIdOrArray : ID idTail'
    var_name = p[1]
    if var_name in tabela_de_simbolos:
        var_type, var_indice = tabela_de_simbolos[var_name]
        if p[2] == "":
            p[0] = f"    STOREG {var_indice}\n"
        elif isinstance(var_type, tuple) and var_type[0] == "ARRAY":
            code = f"    PUSHG {var_indice}\n"
            code += p[2]
            p[0] = ("array", code)

            


def p_forDirection(p):
    'forDirection : TO'
    p[0] = "TO"
    
def p_forDirection_downto(p):
    'forDirection : DOWNTO'
    p[0] = "DOWNTO"


def p_booleanExpression(p):
    'booleanexpression : expression booleanTail'
    p[0] = p[1] + p[2] # No código VM primeiro temos de dar load às variáveis e só depois comparamos

def p_booleanTail(p):
    'booleanTail : oplogico expression'
    p[0] = p[2] + p[1]  

def p_booleanTail_empty(p):
    'booleanTail : empty'
    p[0] = ""

def p_expression(p):
    'expression : termo '
    p[0] = p[1]
 

def p_expression_2(p):
    'expression : expression oplp termo'
    p[0] = p[1] + p[3] + p[2]

def p_termo(p):
    'termo : fator '
    p[0] = p[1]


def p_termo_2(p):
    'termo : termo ophp fator'
    p[0] = p[1] + p[3] + p[2]

def p_ophp(p):
    'ophp : TIMES'
    p[0] = "    MUL\n"
    
def p_ophp_2(p):
    'ophp : DIV'
    p[0] = "    DIV\n"

def p_ophp_mod(p):
    'ophp : MOD'
    p[0] = "    MOD\n"

def p_ophp_and(p):
    'ophp : AND'
    p[0] = "    AND\n"

def p_ophp_divide(p):
    'ophp : DIVIDE'
    p[0] = "    FDIV\n"

def p_oplp(p):
    'oplp : PLUS'
    p[0] = "    ADD\n"

def p_oplp_2(p):
    'oplp : MINUS'
    p[0] = "    SUB\n"

def p_oplp_or(p):
    'oplp : OR'
    p[0] = "    OR\n"

def p_fator(p):
    'fator : const'
    p[0] = p[1]

def p_fator_2(p):
    'fator : var'
    p[0] = p[1]

def p_fator_3(p):
    'fator : LPARENT booleanexpression RPARENT'
    p[0] = p[2]

def p_fator_4(p):
    'fator : functioncall'
    p[0] = p[1]

def p_fator_5(p):
    'fator : NOT fator'
    p[0] = p[2] + "    NOT\n"

def p_functioncall(p):
    'functioncall : LENGTH LPARENT arguments RPARENT'
    p[0] = p[3] + "    STRLEN\n"
        

def p_arguments(p):
    'arguments : ID'
    var_type,index = tabela_de_simbolos[p[1]]
    var_type_2,counter = var_type
    _,index_2 = tabela_de_simbolos["string" + str(counter)]
    p[0] = f'    PUSHG {index_2}\n'

def p_arguments_frase(p):
    'arguments : FRASE'
    string = p[1][1:-1] # Retira as aspas da string
    p[0] = f"    PUSHS \"{string}\"\n"

def p_const(p):
    'const : NUMBER'
    # verificamos se tem um ponto para descobrir se é um REAL
    if '.' in p[1]:
        p[0] = f"    PUSHF {p[1]}\n" 
    else:
        p[0] = f"    PUSHI {p[1]}\n"  

def p_const_2(p):
    'const : FRASE'
    string = p[1][1:-1] # Retira as aspas da string
    p[0] = f"    PUSHS \"{string}\"\n    CHRCODE\n"

def p_const_true(p):
    'const : TRUE'
    p[0] = f"    PUSHI {TRUE}\n"

def p_const_false(p):
    'const : FALSE'
    p[0] = f"    PUSHI {FALSE}\n"

def p_var(p):
    'var : ID varTail'
    var_name = p[1]
    if var_name in tabela_de_simbolos:
        var_type, var_indice = tabela_de_simbolos[var_name]
        if p[2] == "":
            p[0] = f"    PUSHG {var_indice}\n"
        else:
            p[0] = f"    PUSHG {var_indice}\n" + p[2]
    else:
        print(f"Erro: Variável '{var_name}' não declarada")
        p[0] = ""

def p_varTail_array(p):
    'varTail : LBRACKET expression RBRACKET' 
    code = p[2]
    code += f"    PUSHI 1\n"  #atualizar index na vm começa em 0
    code += f"    SUB\n"
    code += f"    LOADN\n"
    p[0] = code

def p_varTail_empty(p):
    'varTail : empty'
    p[0] = ""

def p_oplogico(p):
    'oplogico : EQUALS'
    p[0] = "    EQUAL\n"

def p_oplogico_2(p):
    'oplogico : GREATER'
    p[0] = "    SUP\n"
    
def p_oplogico_3(p):
    'oplogico : GE'
    p[0] = "    SUPEQ\n"
    
def p_oplogico_4(p):
    'oplogico : LESSER'
    p[0] = "    INF\n"
    
def p_oplogico_5(p):
    'oplogico : LE'
    p[0] = "    INFEQ\n"

def p_oplogico_6(p):
    'oplogico : NOTEQUAL'
    p[0] = "    EQUAL\n    NOT\n"


def p_empty(p):
    'empty :'
    p[0] = ""

def p_error(p):
    if p:
        print(f"Erro de sintaxe no token '{p.value}' (tipo: {p.type}) na linha {p.lineno}")
    else:
        print("Erro de sintaxe no final do arquivo")

parser = yacc.yacc(debug=True)


def reset_globals():
    """Reset das variáveis globais para permitir múltiplas execuções"""
    global tabela_de_simbolos, next_index, if_counter, for_counter, while_counter, string_counter
    tabela_de_simbolos = {}
    next_index = 0
    if_counter = 0
    for_counter = 0
    while_counter = 0
    string_counter = 0

def parse_file_with_reset(input_filename, output_filename=None):
    """Versão da parse_file que reseta as variáveis globais antes de processar"""
    reset_globals()
    return parse_file(input_filename, output_filename)

def parse_file(input_filename, output_filename=None):
    try:
    
        with open(input_filename, 'r', encoding='utf-8') as file:
            data = file.read()
        
        result = parser.parse(data)
        
        if result and result.strip():  # Verifica se há código VM válido
            if output_filename:
                with open(output_filename, 'w', encoding='utf-8') as outfile:
                    outfile.write(result)
                print(f"Código gerado com sucesso!")
                return True
            return result
        else:
            print("Código Pascal de input errado - Erro na análise sintática")
            if output_filename and os.path.exists(output_filename):
                os.remove(output_filename)
            return False
            
    except FileNotFoundError:
        print(f"Arquivo não encontrado: '{input_filename}'")
        return False
    except UnicodeDecodeError:
        print(f"Código Pascal de input errado - Erro de codificação no arquivo: '{input_filename}'")
        return False
    except Exception as e:
        print(f"Código Pascal de input errado")
        if output_filename and os.path.exists(output_filename):
            os.remove(output_filename)
        return False

if __name__ == "__main__":
    import sys
    
    # Verificar se foi passado um arquivo como argumento
    if len(sys.argv) != 2:
        print("Uso: python analizer.py <arquivo.pas>")
        print("Exemplo: python analizer.py teste.pas")
        print("        python analizer.py testes/teste6.pas")
        print("\nO arquivo de saída será gerado automaticamente na pasta 'codigo_vm'")
        print("com o nome '<arquivo_original>_result.txt'")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Verificar se o arquivo existe
    if not os.path.exists(input_file):
        print(f"Erro: Arquivo '{input_file}' não encontrado!")
        sys.exit(1)
    
    # Extrair o nome do arquivo sem extensão e diretório
    filename = os.path.basename(input_file)
    if filename.endswith('.pas'):
        base_name = filename[:-4]  # Remove .pas
    else:
        base_name = filename

    output_file = os.path.join("codigo_vm", f"{base_name}_result.txt")

    success = parse_file_with_reset(input_file, output_file)
    if not success:
        sys.exit(1)


