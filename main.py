import random
import numpy as np


# Definição dos itens: cada camisa tem tamanho e demanda.
# Camisa P: 1.5m, 500 unidades
# Camisa M: 1.55m, 300 unidades
# Camisa G: 1.90m, 600 unidades
# Camisa GG: 2.20m, 200 unidades
items = []
items.extend([("P", 1.5)] * 5)
items.extend([("M", 1.55)] * 3)
items.extend([("G", 1.90)] * 6)
items.extend([("GG", 2.20)] * 2)
N = len(items)  # Número total de itens

bin_capacity = 5.0  # Capacidade de cada bin em metros

def decode(individual):
    """
    Decodifica o vetor de chaves aleatórias em uma solução:
    - Ordena os itens com base nas chaves associadas.
    - Aloca os itens em bins, usando o método first-fit.
    Retorna uma lista de bins, onde cada bin é uma lista de índices dos itens.
    """
    # Cria uma lista de tuplas (chave, índice) e ordena com base na chave
    indexed_keys = list(zip(individual, range(N)))
    indexed_keys.sort()  # Ordena implicitamente pelo primeiro elemento (chave)
    
    bins = []
    current_bin = []
    current_sum = 0.0

    for _, i in indexed_keys:
        size = items[i][1]
        # Se couber no bin atual, adiciona; senão, inicia um novo bin
        if current_sum + size <= bin_capacity:
            current_bin.append(i)
            current_sum += size
        else:
            bins.append(current_bin)
            current_bin = [i]
            current_sum = size

    if current_bin:
        bins.append(current_bin)

    return bins


def fitness(individual):
    """
    Função de avaliação: número de bins utilizados (menor é melhor).
    """
    bins = decode(individual)
    return len(bins)


x_geracoes = []
y_bins = []
def brkga(pop_size=50, elite_fraction=0.2, mutant_fraction=0.15, inheritance_prob=0.7, generations=1000):
    """
    Implementa o BRKGA (Biased Random-Key Genetic Algorithm)
    
    Parâmetros:
      pop_size         : Tamanho da população
      elite_fraction   : Fração da população considerada elite
      mutant_fraction  : Fração de indivíduos gerados aleatoriamente (mutantes)
      inheritance_prob : Probabilidade de herdar o gene do pai elite
      generations      : Número de gerações
    Retorna o melhor indivíduo encontrado e seu fitness.
    """
    # Inicializa a população com indivíduos aleatórios
    population = []
    for _ in range(pop_size):
        individual = [random.random() for _ in range(N)]
        population.append(individual)
    
    best_individual = None
    best_fit = float('inf')
    
    for gen in range(generations):
        # Ordena a população pelo fitness (menor número de bins)
        population.sort(key=lambda ind: fitness(ind))
        current_best = fitness(population[0])
        if current_best < best_fit:
            best_fit = current_best
            best_individual = population[0][:]
            print(f"Geração {gen}: Melhor solução usa {best_fit} bins")
            x_geracoes.append(gen)
            y_bins.append(best_fit)

        
        # Definição dos tamanhos dos grupos elite e de mutantes
        elite_size = int(elite_fraction * pop_size)
        mutant_size = int(mutant_fraction * pop_size)
        
        new_population = population[:elite_size]  # preserva os elites
        
        # Adiciona indivíduos mutantes (aleatórios)
        for _ in range(mutant_size):
            mutant = [random.random() for _ in range(N)]
            new_population.append(mutant)
        
        # Preenche o restante da nova população com descendentes gerados por crossover enviesado
        while len(new_population) < pop_size:
            elite_parent = random.choice(population[:elite_size])
            non_elite_parent = random.choice(population[elite_size:])
            child = []
            for i in range(N):
                if random.random() < inheritance_prob:
                    child.append(elite_parent[i])
                else:
                    child.append(non_elite_parent[i])
            new_population.append(child)
        
        population = new_population

    x_geracoes.append(generations)
    y_bins.append(best_fit)
    return best_individual, best_fit

import time
import matplotlib.pyplot as plt
# Execução do algoritmo
if __name__ == "__main__":
    start_time = time.time()
    qtd_geracoes = 100
    best_ind, best_bins = brkga(generations=qtd_geracoes)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Tempo de execução: {elapsed_time:.2f} segundos\n")

    print("Melhor solução (encontrada):")
    print("Número de bins utilizados:", best_bins)
    desperdicio_total = -(sum(items[i][1] for i in range(N)) - best_bins * bin_capacity)
    print("Disperdício total:", desperdicio_total,"m")
    # print("Melhor indivíduo:")
    # for i in best_ind:
    #     print(f"{i:.2f}", end=" \n")

    bins_solution = decode(best_ind)
    for idx, bin_items in enumerate(bins_solution):
        # Exibe os itens de cada bin com seus respectivos tipos e tamanhos
        bin_desc = [f"{items[i][0]}({items[i][1]})" for i in bin_items]
        # print(f"Bin {idx+1}: {bin_desc} : tamanho total: {sum(items[i][1] for i in bin_items):.2f}m")

    
    # Gráfico de evolução do número de bins utilizados ao longo das gerações
    plt.plot(x_geracoes, y_bins, marker='o')
    

    titulo = str("Evolução do número de bins utilizados ao longo das gerações"+"\n"+
        "Número de bins: "+str(best_bins)+"\n"+
        "Disperdício total: "+str(desperdicio_total)+"m"+"\n"+
        "Tempo de execução: "+str(round(elapsed_time,2))+" segundos")
    plt.title(titulo,fontsize=8)
    plt.xlabel("Gerações")
    plt.ylabel("Número de bins")
    plt.grid()
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    nome_arquivo = "resultados/"+str(qtd_geracoes)+"gen.png"
    plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
    plt.tight_layout()
    plt.show()