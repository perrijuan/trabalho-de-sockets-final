# servidor sockets 

usando uma biblioteca sockets o algoritmo faz resolução de questões de uma prova de uma matéria do curso da UFRJ chamada "Fundamentos de Computação", a prova envolve conceitos básicos de programação como conversão de bases, operações com números negativos em complemento a dois, usando de padrões de ponto flutuante sendo ieee 754 com 32 bits, e representação de texto em ASCII, e algbra de boole.

# instalação 

Usando um servidor local ou um simulador de host local como um hamachi ou uma maquina virtual para o controle de dados, que será o servidor é necessário definir o host sendo o ip e a porta que o servidor irá criar o objeto sockets, feito isso também é necessário para o uso da questão 6 e 7 que o servidor tenha já instalado a biblioteca "SchemDraw". 

# uso 

O servidor o mesmo deve ser executado antes do cliente caso trivial, e se atentando que deve definir um localhost para a conexão com os exemplos citados a cima. 

O cliente pode escolher quantas vezes e quais questões da prova ele quer resolver, logo quando o cliente erra ele será redirecionado para a seleção principal para fazer novamente, e para as questões 6 e 7 também é importante o programa não consegue representar no terminal, logo ele salva onde o arquivo foi executado, logo é necessário prestar atenção nisso, ele substitui o arquivo anterior pelo recente logo é necessário salvar os diagramas pois caso contrario pode haver perdas.

