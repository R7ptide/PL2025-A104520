program AnalisaNumero;
var
    numero: Integer;
begin
    write('Introduza um número: ');
    readln(numero);

    if numero > 0 then
        write('O número é positivo.')
    else if numero < 0 then
        write('O número é negativo.')
    else
        write('O número é zero.');

end.