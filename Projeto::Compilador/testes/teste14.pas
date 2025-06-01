program ContadorDownto;
var
    inicio, fim, passo, atual: integer;
    i: integer;
begin
    writeln('Programa de contagem regressiva');
    write('Número inicial: ');
    readln(inicio);
    write('Número final: ');
    readln(fim);
    
    if inicio > fim then
    begin
        writeln('Contagem regressiva de ', inicio, ' até ', fim, ':');
        for i := inicio downto fim do
            writeln('Valor atual: ', i);
    end
    else
    begin
        writeln('Contagem progressiva de ', inicio, ' até ', fim, ':');
        for i := inicio to fim do
            writeln('Valor atual: ', i);
    end;
    
    { Teste de loop while com contador regressivo }
    atual := inicio;
    writeln('Usando while para contagem:');
    
    if inicio > fim then
    begin
        while atual >= fim do
        begin
            writeln('While: ', atual);
            atual := atual - 1;
        end;
    end
    else
    begin
        while atual <= fim do
        begin
            writeln('While: ', atual);
            atual := atual + 1;
        end;
    end;
    
    writeln('Fim da contagem!');
end.
