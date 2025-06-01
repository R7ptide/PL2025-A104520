program TesteCompletoOperadores;
var
    a, b: integer;
    x, y, z: real;
    resultado: real;
begin
    { Teste dos operadores de comparacao }
    a := 10;
    b := 5;
    
    if a > b then
        writeln('a > b: verdadeiro');
    
    if a >= b then
        writeln('a >= b: verdadeiro');
    
    if b < a then
        writeln('b < a: verdadeiro');
    
    if b <= a then
        writeln('b <= a: verdadeiro');
    
    if a <> b then
        writeln('a <> b: verdadeiro');
    
    { Teste do operador de divisao real }
    x := 15.0;
    y := 4.0;
    z := x / y;
    
    writeln('15.0 / 4.0 = ');
    writeln(z);
    
    { Teste combinado }
    resultado := a / b;
    if resultado <> 2.0 then
        writeln('Divisao de inteiros: resultado diferente de 2.0');
end.
