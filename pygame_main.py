
import random
import pygame

# ========= CONFIGURAÇÕES =========
ITEM_TYPES = {"P": 1.5, "M": 1.55, "G": 1.90, "GG": 2.20}
n=10
CAMISA_COUNTS = {"P": n*5, "M": n*15, "G": n*10, "GG": n*7}
BIN_CAPACITY = 5.0
POP_SIZE = 100
GENERATIONS = 1000
ELITE_FRAC = 0.2
MUTANT_FRAC = 0.3
INHERIT_PROB = 0.5

CORES = {"P": (255, 100, 100), "M": (100, 255, 100), "G": (100, 100, 255), "GG": (240, 240, 50)}
LARGURA_TELA, ALTURA_TELA = 1000, 700
BG = (30, 30, 30)
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)

# ========= FUNÇÕES DE GENÉTICA CLÁSSICA (float genes) =========

def random_individual():
    # Gera lista de floats [0,1]
    tamanho = sum(CAMISA_COUNTS.values())
    return [random.random() for _ in range(tamanho)]

def decode(individual):
    # Monta lista fixa dos tipos na ordem natural (fixa)
    tipos_ordenados = []
    for tipo, qtd in CAMISA_COUNTS.items():
        tipos_ordenados.extend([tipo] * qtd)

    # Ordena índices pelo gene float (menor para maior)
    indices_ordenados = sorted(range(len(individual)), key=lambda i: individual[i])

    # Sequência de camisas na ordem dos genes ordenados
    individuo_ordenado = [tipos_ordenados[i] for i in indices_ordenados]

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
    _, sobra = decode(individual)
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

# ========= FUNÇÕES DE VISUALIZAÇÃO =========

def desenhar_grafico(historico, x, y, largura, altura, max_valor):
    if len(historico) < 2:
        return
    max_valor = max_valor if max_valor > 0 else 1
    pontos = len(historico)
    escala_y = altura / max_valor
    escala_x = largura / (pontos - 1)

    for i in range(pontos - 1):
        x1 = x + i * escala_x
        y1 = y + altura - historico[i] * escala_y
        x2 = x + (i + 1) * escala_x
        y2 = y + altura - historico[i + 1] * escala_y
        pygame.draw.line(screen, AMARELO, (x1, y1), (x2, y2), 2)

    pygame.draw.line(screen, BRANCO, (x, y), (x, y + altura), 2)
    pygame.draw.line(screen, BRANCO, (x, y + altura), (x + largura, y + altura), 2)

    texto_max = font.render(f"{max_valor:.2f}", True, BRANCO)
    screen.blit(texto_max, (x - texto_max.get_width() - 5, y))

def desenhar_bins_e_grafico(bins, geracao, desperdicio, historico, max_desperdicio,
                            destaque=False, melhoria_valor=None, melhoria_bins=None):
    screen.fill(BG)
    y = 10
    escala = 80
    for bin in bins[:60]:
        x = 10
        for _, tipo, tamanho in bin:
            largura = tamanho * escala
            pygame.draw.rect(screen, CORES[tipo], (x, y, largura, 12))
            if destaque:
                pygame.draw.rect(screen, BRANCO, (x, y, largura, 12), 1)
            x += largura
        y += 16
        if y > ALTURA_TELA - 100:
            break

    screen.blit(font.render(f"Geração: {geracao + 1}", True, BRANCO), (800, 20))
    screen.blit(font.render(f"Desperdício: {desperdicio:.2f}m", True, BRANCO), (800, 50))
    screen.blit(font.render(f"Bins usados: {len(bins)}", True, BRANCO), (800, 80))

    if melhoria_valor is not None:
        screen.blit(font.render(f"-{melhoria_valor:.2f}", True, AMARELO), (720, 50))
    if melhoria_bins is not None:
        screen.blit(font.render(f"-{melhoria_bins}", True, AMARELO), (720, 80))

    desenhar_grafico(historico, 800, 110, 180, 580, max_desperdicio)
    pygame.display.flip()

# ========= ALGORITMO PRINCIPAL =========

def brkga_visual(pop_size, elite_frac, mutant_frac, inherit_prob, generations):
    population = [random_individual() for _ in range(pop_size)]
    elite_size = int(elite_frac * pop_size)
    mutant_size = int(mutant_frac * pop_size)
    melhor_desperdicio = float("inf")
    melhor_num_bins = float("inf")
    efeito_frames = 0
    melhoria_valor = None
    melhoria_bins = None
    historico_desperdicio = []

    for gen in range(generations):
        # Avaliar e ordenar população
        pop_fitness = [(fitness(ind), ind) for ind in population]
        pop_fitness.sort(key=lambda x: x[0])

        melhor = pop_fitness[0][1]
        desperdicio = pop_fitness[0][0]
        bins, _ = decode(melhor)
        num_bins = len(bins)

        historico_desperdicio.append(desperdicio)
        max_desperdicio = max(historico_desperdicio)

        if desperdicio < melhor_desperdicio:
            melhoria_valor = melhor_desperdicio - desperdicio
            melhoria_bins = melhor_num_bins - num_bins if num_bins < melhor_num_bins else None
            melhor_desperdicio = desperdicio
            melhor_num_bins = num_bins
            efeito_frames = 20

        if gen % 10 == 0:
            desenhar_bins_e_grafico(
                bins, gen, desperdicio, historico_desperdicio, max_desperdicio,
                destaque=efeito_frames > 0,
                melhoria_valor=melhoria_valor if efeito_frames > 0 else None,
                melhoria_bins=melhoria_bins if efeito_frames > 0 else None,
            )
            if efeito_frames > 0:
                efeito_frames -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
                # pygame.quit()
                # exit()

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
        clock.tick(10)  # FPS para rodar rápido

# ========= INICIALIZAÇÃO PYGAME =========

pygame.init()
screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("BRKGA Clássico - Visualização")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

if __name__ == "__main__":
    brkga_visual(POP_SIZE, ELITE_FRAC, MUTANT_FRAC, INHERIT_PROB, GENERATIONS)

    # Mantém a janela aberta após o algoritmo terminar
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
