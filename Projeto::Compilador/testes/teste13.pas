program LoopsAninhados;
var
    numeros: array[1..9] of integer;
    i, j, soma, produto, posicao: integer;
begin
    writeln('Preencha 9 números (3x3):');
    
    { Preencher o array }
    posicao := 1;
    for i := 1 to 3 do
    begin
        for j := 1 to 3 do
        begin
            write('Elemento [', i, ',', j, ']: ');
            readln(numeros[posicao]);
            posicao := posicao + 1;
        end;
    end;
    
    { Calcular soma da diagonal principal }
    soma := 0;
    soma := soma + numeros[1]; { posição [1,1] }
    soma := soma + numeros[5]; { posição [2,2] }
    soma := soma + numeros[9]; { posição [3,3] }
    
    { Calcular produto da primeira linha }
    produto := 1;
    produto := produto * numeros[1];
    produto := produto * numeros[2];
    produto := produto * numeros[3];
    
    { Exibir os números }
    writeln('Números inseridos:');
    posicao := 1;
    for i := 1 to 3 do
    begin
        for j := 1 to 3 do
        begin
            write(numeros[posicao], ' ');
            posicao := posicao + 1;
        end;
        
    end;
    
    writeln('Soma da diagonal principal: ', soma);
    writeln('Produto da primeira linha: ', produto);
end.
