import random
import time
import matplotlib.pyplot as plt
import os

# Tamanhos e seus comprimentos em metros
ITEM_TYPES = {
    "P": 1.5,
    "M": 1.55,
    "G": 1.90,
    "GG": 2.20,
}

n = 10
# Quantidade fixa de camisas de cada tipo
CAMISA_COUNTS = {
    "P": n*5,
    "M": n*15,
    "G": n*10,
    "GG": n*7,
}

BIN_CAPACITY = 5.0
N = sum(CAMISA_COUNTS.values())  # Número total de camisas


def decode(individual, verbose=False):
    """
    Aplica o first-fit para empacotar a lista de camisas.
    Recebe um indivíduo e retorna ele separado em bins e também o desperdício total
    """
    bins = []
    current_bin = []
    current_sum = 0.0
    soma_de_sobras = 0.0

    for i, tipo in enumerate(individual):
        size = ITEM_TYPES[tipo]
        if current_sum + size <= BIN_CAPACITY:
            current_bin.append((i, tipo, size))
            current_sum += size
        else:
            bins.append(current_bin)
            sobra = BIN_CAPACITY - current_sum
            soma_de_sobras += sobra
            current_bin = [(i, tipo, size)]
            current_sum = size

    if current_bin:
        bins.append(current_bin)
        sobra = BIN_CAPACITY - current_sum
        soma_de_sobras += sobra

    if verbose:
        for bidx, bin_items in enumerate(bins):
            desc = [f"{tipo}({size})" for _, tipo, size in bin_items]
            print(f"Bin {bidx + 1}: {desc} - total: {sum(size for _, _, size in bin_items):.2f}m")

    return bins, soma_de_sobras


def fitness(individual):
    bins, disperdicio = decode(individual)
    return disperdicio


def random_individual():
    """
    Gera um indivíduo aleatório com as quantidades fixas de cada tipo.
    """
    base = []
    for tipo, qtd in CAMISA_COUNTS.items():
        base.extend([tipo] * qtd)
    random.shuffle(base)
    return base


def biased_crossover_respecting_counts(elite, non_elite, inherit_prob=0.7):
    """
    Realiza cruzamento enviesado mantendo a quantidade fixa de cada tipo.
    """
    counts = CAMISA_COUNTS.copy()
    child = []

    options = [
        elite[i] if random.random() < inherit_prob else non_elite[i]
        for i in range(len(elite))
    ]

    for tipo in options:
        if counts[tipo] > 0:
            child.append(tipo)
            counts[tipo] -= 1

    for tipo, restante in counts.items():
        child.extend([tipo] * restante)

    random.shuffle(child)
    return child


def brkga(pop_size=100, elite_frac=0.2, mutant_frac=0.15, inherit_prob=0.7, generations=1000):
    population = [random_individual() for _ in range(pop_size)]
    elite_size = int(elite_frac * pop_size)
    mutant_size = int(mutant_frac * pop_size)
    best_individual = None
    best_fit = float('inf')

    history_gen, history_fit = [], []

    for gen in range(generations):
        population.sort(key=fitness)
        current_fit = fitness(population[0])
        if current_fit < best_fit:
            best_fit = current_fit
            best_individual = population[0][:]
            bins_usados = len(decode(best_individual)[0])
            print(f"Melhorou na geração \t{gen}/{generations} \tdesperdício {best_fit:.2f}m \t bins: {bins_usados}")

            history_gen.append(gen)
            history_fit.append(best_fit)

        new_population = population[:elite_size]

        for _ in range(mutant_size):
            new_population.append(random_individual())

        while len(new_population) < pop_size:
            elite = random.choice(population[:elite_size])
            non_elite = random.choice(population[elite_size:])
            child = biased_crossover_respecting_counts(elite, non_elite, inherit_prob)
            new_population.append(child)

        population = new_population

    return best_individual, best_fit, history_gen, history_fit


def main(gen=10**3):
    generations = gen

    #medir tempo de execução
    start = time.time()
    print("tempo de inicio:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start)))
    best_ind, _, gen_hist, fit_hist = brkga(generations=generations)
    elapsed = time.time() - start

    solution_bins, desperdicio_total = decode(best_ind)
    num_bins_utilizados = len(solution_bins)

    print(f"\nTempo de execução: {elapsed:.2f} segundos")
    print(f"Número de bins utilizados: {num_bins_utilizados}")
    print(f"Desperdício total: {desperdicio_total:.2f}m")

    for idx, bin_items in enumerate(solution_bins):
        desc = [f"{tipo}({size})" for _, tipo, size in bin_items]
        total = sum(size for _, _, size in bin_items)
        print(f"Bin {idx + 1}: {desc} - total: {total:.2f}m")

    # Criar pasta de saída se necessário
    os.makedirs("resultados", exist_ok=True)

    plt.plot(gen_hist, fit_hist, marker='o')
    title = (
        "Evolução do desperdício\n"
        f"Número de bins: {num_bins_utilizados} | Desperdício: {desperdicio_total:.2f}m\n"
        f"Tempo: {elapsed:.2f}s"
    )
    plt.title(title, fontsize=8)
    plt.xlabel("Gerações")
    plt.ylabel("Desperdício total (m)")
    plt.grid(True)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout()
    plt.savefig(f"resultados/brkga_{generations}.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    main()
