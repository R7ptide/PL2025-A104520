program TesteCompleto;
var
    numeros: array[1..3] of integer;
    idade, contador: integer;
    ativo, encontrado: boolean;
    i: integer;
begin
    writeln('=== Teste Completo do Compilador Pascal ===');
    
    { Arrays }
    numeros[1] := 10;
    numeros[2] := 20;
    numeros[3] := 30;
    
    { Booleanos }
    ativo := true;
    encontrado := false;
    
    { Teste de operadores lógicos com NOT }
    if not encontrado then
        writeln('Status: NOT encontrado = true');
    
    if ativo and (not encontrado) then
        writeln('Status: ativo AND (NOT encontrado) = false')
    else
        writeln('Status: ativo AND (NOT encontrado) = true');
    
    { Teste de arrays com write }
    writeln('Elementos do array:');
    write('Elemento 1: ');
    write(numeros[1]);
    writeln('');
    write('Elemento 2: ');
    write(numeros[2]);
    writeln('');
    write('Elemento 3: ');
    write(numeros[3]);
    writeln('');
    
    writeln('=== Teste Finalizado ===')
end.
