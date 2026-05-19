# Relatório
## Nomes
Gabriel Eichelberger Fontaneli - 00601480 - Turma A

Rafaele Castagnara Alves - 00600867 - Turma A

Igor Daut - XXXXXXXX - Turma A

## Avaliação
https://docs.google.com/document/d/1s4GK3X-TBvSQau4x4FD3lZnHhxz5TqMd_Ma0pDckeUY/edit?tab=t.0

*1 INTRODUÇÃO*

O objetivo é analisar algoritmos e heurísticas para dois jogos selecionados, Tic-Tac-Toe Misere e Othello. 

*2 DESENVOLVIMENTO* 

2.2.a)
Para validar a eficiência do algoritmo minimax no problema Tic-Tac-Toe Misere, é necessário responder três perguntas sobre sua eficiência:
(i) O minimax sempre ganha ou empata jogando contra o randomplayer? 
(ii) O minimax sempre empata consigo mesmo? 
(iii) O minimax não perde para você quando você usa a sua melhor estratégia? 	

i. O minimax sempre ganha ou empata jogando contra o randomplayer?

Foram realizadas 200 simulações do minimax contra o randomPlayer, os resultados foram os seguintes:

| Modelo | Vitórias | Empates | Derrotas|
| --- | --- | --- | --- |
| Minimax | 155 | 45 | 0 |
| randomPlayer | 0 | 45 | 155 |


Com o agente randomPlayer iniciando o jogo, ele perdeu em todos os testes. Quando ele é o segundo a jogar, ele tem uma performance um pouco melhor, conseguindo empatar 45 jogos.

ii. O minimax sempre empata consigo mesmo?

Foram realizadas 100 simulações do minimax contra o minimax, os  resultados foram os seguintes:

| Modelo | Vitórias | Empates | Derrotas|
| --- | --- | --- | --- |
| Minimax | 0 | 100 | 0 |
| Minimax | 0 | 100 | 0 |


Isso indica que o minimax está implementado de forma correta.



iii. O minimax não perde para você quando você usa a sua melhor estratégia? 

Foram realizadas 10 simulações do minimax contra um jogador real, os resultados foram os seguintes:

| Modelo | Vitórias | Empates | Derrotas|
| --- | --- | --- | --- |
| Minimax | 6 | 4 | 0 |
| Humano | 0 | 4 | 6 |


Demonstra uma performance muito melhor quando o humano joga primeiro.

2.2.b)

Foram realizadas 10 simulações para cada par no torneio do Othello, os resultados estão apresentados nas tabelas abaixo:

| Heurística | Vitórias | Empates | Derrotas|
| --- | --- | --- | --- |
| Contagem de peças (joga primeiro) | 0 | 0 | 10 |
| Valor posicional  | 10 | 0 | 0 |


| Heurística | Vitórias | Empates | Derrotas|
| --- | --- | --- | --- |
| Contagem de peças (joga primeiro) | 0 | 0 | 10 |
| Customizada | 10 | 0 | 0 |


| Heurística | Vitórias | Empates | Derrotas|
| --- | --- | --- | --- |
| Contagem de peças (joga primeiro) | 0 | 0 | 10 |
| Mcts | 10 | 0 | 0 |


| Heurística | Vitórias | Empates | Derrotas|
| --- | --- | --- | --- |
| Valor posicional (joga primeiro) | 10 | 0 | 0 |
| Contagem de peças | 0 | 0 | 10 |


| Heurística | Vitórias | Empates | Derrotas|
| --- | --- | --- | --- |
| Valor posicional (joga primeiro) | 10 | 0 | 0 |
| Customizada | 0 | 0 | 10 |


| Heurística | Vitórias | Empates | Derrotas|
| --- | --- | --- | --- |
| Valor posicional (joga primeiro) | 4 | 0 | 6 |
| MCTS | 6 | 0 | 4 |


| Heurística | Vitórias | Empates | Derrotas|
| --- | --- | --- | --- |
| Customizada (joga primeiro) | 10 | 0 | 0 |
| Contagem de peças | 0 | 0 | 10 |


| Heurística | Vitórias | Empates | Derrotas|
| --- | --- | --- | --- |
| Customizada (joga primeiro) | 10 | 0 | 0 |
| Valor posicional | 0 | 0 | 10 |


| Heurística | Vitórias | Empates | Derrotas|
| --- | --- | --- | --- |
| Customizada (joga primeiro) | 5 | 1 | 4 |
| MCTS | 4 | 1 | 5 |


| Heurística | Vitórias | Empates | Derrotas|
| --- | --- | --- | --- |
| MCTS (joga primeiro) | 10 | 0 | 0 |
| Contagem de peças | 0 | 0 | 10 |


| Heurística | Vitórias | Empates | Derrotas|
| --- | --- | --- | --- |
| MCTS (joga primeiro) | 5 | 4 | 1 |
| Valor posicional | 4 | 1 | 5 |


| Heurística | Vitórias | Empates | Derrotas|
| --- | --- | --- | --- |
| MCTS (joga primeiro) | 6 | 0 | 4 |
| Customizada | 4 | 0 | 6 |


*Tabela final do mini torneio*

| Heurítica | vitórias do torneio |
| --- | --- |
| Contagem de peças | 1 |
| Valor posicional | 38 |
| Customizada | 39 |
| Modelo MCTS | 40 |

A partir desses resultados, é possível concluir que a MCTS foi a heurística que mais teve sucesso, porém também foi a mais inconsistente pois o algoritmo em si possui muita variância.
Outra conclusão é que o jogador que faz a primeira jogada possui vantagem, pois, quando a heurística customizada joga contra a heurística de valor posicional, ganha sempre quem começa.

Como funciona a heurística customizada?
	
Ela se baseia em uma estratégia para o jogo Othello que muda durante o decorrer do jogo. No início do jogo (quando tem menos de 20 peças no tabuleiro), a heurística prioriza o valor posicional das peças e a mobilidade (quantidade de movimentos legais que o jogador tem) e considera que ter muitas peças é ruim nessa fase inicial, diminuindo o valor da heurística com o aumento da quantidade de peças. 
No início do meio do jogo (entre 20 e 30 peças no tabuleiro), a estratégia continua priorizando o valor posicional das peças e a mobilidade, mas agora não diminui mais o valor com o aumento da quantidade de peças. Exatamente no meio do jogo (entre 30 e 40 peças no tabuleiro), a estratégia continua priorizando o valor posicional das peças e a mobilidade, mas agora consideramos a quantidade de peças do jogador, somando o dobro da diferença entre as peças do jogador e do oponente. Mais para o fim do jogo, mas ainda não no final, (entre 40 e 50 peças no tabuleiro), a estratégia continua priorizando o valor posicional das peças e a mobilidade, mas agora focamos mais na quantidade de peças, visto que no final do jogo é isso que conta para a vitória, somamos na pontuação cinco vezes a diferença entre a quantidade de peças do jogador e do oponente. No fim do jogo (o tabuleiro tem mais de 50 peças), a heurística prioriza apenas ter uma quantidade de peças maior do que o oponente.

*Extras:*

Como extra, foi implementado o algoritmo do MCTS (Monte Carlo Tree Search) e suas 4 fases da seguinte maneira: 
1.SELECT: Partindo da raiz, o algoritmo desce pela árvore escolhendo os nós filhos até encontrar um nó que não esteja totalmente expandido ou que seja o fim do jogo. A política de seleção foi implementada no método best_child() e usa da heurística UCT (Upper Confidence Bound for Trees), que foi vista em aula, o valor escolhido para a constante C foi 1.41, pois ele é considerado o valor padrão teórico.
2.EXPAND: Quando o algoritmo encontra um nó que ainda tem jogadas não testadas (untried_moves), ele sorteia uma dessas jogadas aleatoriamente usando random.choice(). Essa jogada é removida da lista de não tentadas, o novo estado do tabuleiro é gerado (next_state) e um novo nodo (MCTSNode) é criado e anexado como filho do estado atual.
3.SIMULATE: A partir do novo nó expandido, o algoritmo joga partidas aleatórias para ver qual seria o resultado com limite de profundidade 7.
4.BACK-PROPAGATE: O resultado da simulação sobe de volta até a raiz, atualizando as estatísticas de vitórias e visitas de cada nó no caminho. Se o estado for terminal, retorna 1 para vitória, 0.5 para empate e 0 para derrota. Caso o estado não seja terminal, retorna o valor da heurística de Valor Posicional convertida para uma escala de 0 a 1.
Quando o tempo de execução limite termina, o loop principal é interrompido e a função retorna a jogada do filho com o maior número de visitas.

4 CONCLUSÃO

Após testes, é possível concluir que o algoritmo minimax está funcionando de maneira ótima. 
