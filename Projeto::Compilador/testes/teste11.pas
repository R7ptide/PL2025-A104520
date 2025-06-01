program testeArrayWrite;
var
    numeros: array[1..3] of integer;
    i: integer;
begin
    numeros[1] := 10;
    numeros[2] := 20;
    numeros[3] := 30;
    
    writeln('Teste write array:');
    write(numeros[1]);
    writeln(' - primeiro elemento');
    write(numeros[2]); 
    writeln(' - segundo elemento');
    write(numeros[3]);
    writeln(' - terceiro elemento')
end.
