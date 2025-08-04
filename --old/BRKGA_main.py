##########################
# BRGKA
##########################
# Danillo Mendes Santiago
# 10414592
##########################

import random

# ========= PARAMETROS DO PROBLEMA =========
ITEM_TYPES = {"P": 1.5, "M": 1.55, "G": 1.90, "GG": 2.20}
n=10
CAMISA_COUNTS = {"P": n*5, "M": n*15, "G": n*10, "GG": n*7}
BIN_CAPACITY = 5.0

# PARAMETROS DO ALG. GENÉTICO
POP_SIZE = 100
ELITE_FRAC = 0.2
MUTANT_FRAC = 0.4
INHERIT_PROB = 0.5

# ========= FUNÇÕES DO ALG. GENÉTICO  =========

def random_individual():
    # Gera um vetor de R^n onde cada componente pertece à [0,1]
    tamanho = sum(CAMISA_COUNTS.values())
    return [random.random() for _ in range(tamanho)]

def decode(individual):
    # Monta uma lista fixa com a demanda. Ex.: [P,P,M,M,M,G,G,G,G,GG]
    tipos_ordenados = []
    for tipo, qtd in CAMISA_COUNTS.items():
        tipos_ordenados.extend([tipo] * qtd)

    # Ordena índices pelo gene float (menor para maior)
    indices = range(len(individual))
    indices_ordenados = sorted( indices, key=lambda i: individual[i])

    # Sequência de camisas na ordem dos genes ordenados
    individuo_ordenado = [tipos_ordenados[i] for i in indices_ordenados]

    # Divide a sequencia, tentando ocupar todo o bin, na medida do possível
    bins = []
    current_bin = []
    current_sum = 0.0
    sobra_total = 0.0

    for i, tipo in enumerate(individuo_ordenado):
        size = ITEM_TYPES[tipo]
        if current_sum + size <= BIN_CAPACITY:
            current_bin.append((i, tipo, size))
            current_sum += size
        else:
            bins.append(current_bin)
            sobra_total += BIN_CAPACITY - current_sum
            current_bin = [(i, tipo, size)]
            current_sum = size

    if current_bin:
        bins.append(current_bin)
        sobra_total += BIN_CAPACITY - current_sum

    return bins, sobra_total

def fitness(individual):
    bins_usados, sobra = decode(individual)
    return sobra

def biased_crossover(elite, non_elite, inherit_prob=INHERIT_PROB):
    # Crossover clássico gene a gene
    child = []
    for e_gene, n_gene in zip(elite, non_elite):
        if random.random() < inherit_prob:
            child.append(e_gene)
        else:
            child.append(n_gene)
    return child

# ========= ALGORITMO PRINCIPAL =========
import time

def brgka_simples(num_geracoes, pop_size, elite_frac, mutant_frac, inherit_prob):
    
    population = [random_individual() for _ in range(pop_size)]
    elite_size = int(elite_frac * pop_size)
    mutant_size = int(mutant_frac * pop_size)

    melhor_individuo = None
    melhor_desperdicio = float("inf")

    for geracao in range(num_geracoes):
        # Avaliar população
        pop_fitness = [ (fitness(ind) , ind) for ind in population]
        pop_fitness.sort(key=lambda x: x[0])

        desperdicio_atual = pop_fitness[0][0]
        melhor_atual = pop_fitness[0][1]

        if desperdicio_atual < melhor_desperdicio:
            melhor_desperdicio = desperdicio_atual
            melhor_individuo = melhor_atual

        # Nova população
        new_pop = [ind for _, ind in pop_fitness[:elite_size]]
        for _ in range(mutant_size):
            new_pop.append(random_individual())
        while len(new_pop) < pop_size:
            elite = random.choice(new_pop[:elite_size])
            non_elite = random.choice(population[elite_size:])
            filho = biased_crossover(elite, non_elite, inherit_prob)
            new_pop.append(filho)

        population = new_pop

    # Decode final
    bins, desperdicio_final = decode(melhor_individuo)
    num_bins = len(bins)
    sequencia_de_corte = [ [tipo for _, tipo, _ in bin] for bin in bins]

    return num_bins, desperdicio_final, sequencia_de_corte

# ==================================================================
# ===================== EXECUÇÃO PRINCIPAL =========================
# ==================================================================

# ============ TESTES DE PERFORMANCE =======================

num_geracoes = [1000]#, 5000, 10000, 50000, 100000]
num_repeticoes = 2

resultados_individuais = []  # cada item: (geracoes, tempo_execucao, desperdicio, repetição_id)
resultados_medios = []       # cada item: (geracoes, media_tempo, media_desp)

for n_geracoes in num_geracoes:
    tempos = []
    desperdicios = []

    print(f"\n== Rodando {n_geracoes} gerações, {num_repeticoes} vezes ==")
    for rep in range(num_repeticoes):
        print(f"  Execução {rep+1}/{num_repeticoes}...")
        inicio = time.time()
        num_bins, desperdicio, sequencia_camisas = brgka_simples(
            n_geracoes, POP_SIZE, ELITE_FRAC, MUTANT_FRAC, INHERIT_PROB
        )
        duracao = time.time() - inicio
        resultados_individuais.append((n_geracoes, duracao, desperdicio, rep + 1))
        tempos.append(duracao)
        desperdicios.append(desperdicio)

    media_tempo = sum(tempos) / num_repeticoes
    media_desp = sum(desperdicios) / num_repeticoes
    resultados_medios.append((n_geracoes, media_tempo, media_desp))
