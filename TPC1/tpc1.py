

def somador_on_off(texto):
    soma = 0
    ativo = True
    num = "" 
    
    i = 0
    while i < len(texto):
        char = texto[i]

        if char in "0123456789":
            num += char
        else: 
            if num:  
                if ativo:
                    soma += int(num)
                num = ""  
            
            if texto[i:i+2].lower() == "on":
                ativo = True
                i += 1
            elif texto[i:i+3].lower() == "off":
                ativo = False
                i += 2
            elif char == "=":
                print(soma)

        i += 1

    if num and ativo: 
        soma += int(num)



teste = "ola 10 on 2025-02-06 Off 30 on asadsasd40sdfsdf = Off 50 60 = On 70 ="
somador_on_off(teste)
