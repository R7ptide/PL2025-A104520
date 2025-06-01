program ManipulacaoStrings;
var
    frase, palavra: string;
    i, contador, tamanho: integer;
    encontrou: boolean;
begin
    writeln('Digite uma frase:');
    readln(frase);
    writeln('Digite uma palavra para contar:');
    readln(palavra);
    
    contador := 0;
    tamanho := length(frase);
    encontrou := false;
    
    { Contar ocorrências da primeira letra da palavra }
    for i := 1 to tamanho do
    begin
        if frase[i] = palavra[1] then
        begin
            contador := contador + 1;
            encontrou := true;
        end;
    end;
    
    if encontrou then
        writeln('A primeira letra da palavra aparece ', contador, ' vezes na frase')
    else        writeln('A primeira letra da palavra não foi encontrada na frase');
    
    tamanho := length(frase);
    writeln('Tamanho da frase: ', tamanho);
    tamanho := length(palavra);
    writeln('Tamanho da palavra: ', tamanho);
end.
