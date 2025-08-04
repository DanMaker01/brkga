🧩 O Bin Packing Problem (problema de empacotamento ou de "encher um container") é um desafio clássico de otimização combinatória. Nele, o objetivo é alocar itens de diferentes tamanhos em recipientes (bins) com capacidade limitada, minimizando o número total de bins utilizados ou o espaço desperdiçado. Neste projeto, o foco é o empacotamento de camisas de tamanhos variados — P, M, G e GG — em rolos de tecido com 5 metros de comprimento, respeitando uma demanda fixa para cada tipo.

🧬 O algoritmo BRKGA (Biased Random-Key Genetic Algorithm) é uma abordagem evolutiva baseada em genes representados por números reais no intervalo 
0
,
1
0,1. Cada indivíduo da população é um vetor que, ao ser ordenado, define uma sequência de empacotamento. O algoritmo combina elitismo, geração de mutantes aleatórios e cruzamento enviesado para balancear exploração e exploração, otimizando progressivamente a alocação de itens nos bins ao longo das gerações.

🎮 A aplicação conta com uma interface interativa desenvolvida em Pygame, que permite observar em tempo real o desempenho das soluções e o comportamento da população ao longo das gerações. Também há uma versão automatizada voltada para testes de performance e experimentos. Os dados gerados são exportados em arquivos .csv com timestamp, e gráficos são produzidos com Matplotlib para facilitar a análise do desperdício de material e da eficiência de empacotamento.

📦 Parâmetros do Problema Exemplo (resultados na pasta)

Demanda de Camisas:

P: 50 unidades

M: 150 unidades

G: 100 unidades

GG: 70 unidades

Tamanho das Camisas:

P: 1.50 metros

M: 1.55 metros

G: 1.90 metros

GG: 2.20 metros

Comprimento de cada rolo de tecido (bin): 5.00 metros
