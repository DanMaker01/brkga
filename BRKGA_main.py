##########################
# BRGKA
##########################
# Danillo Mendes Santiago
# 10414592
##########################

import numpy as np
import random

# DEFINIÇÕES
n = 10
DEMANDA = {
    'P' : n*5,
    'M' : n*15,
    'G' : n*10,
    'GG': n*7
}
TECIDO_NECESSARIO = {
    "P": 1.5,
    "M": 1.55,
    "G": 1.90,
    "GG": 2.20,
}
TAMANHO_BIN = 5
QUANTIDADE_GENES = sum(DEMANDA.values())
QUANTIDADE_INDIVIDUOS = 100
ELITE = 0.2
NUM_GERACOES = 1000

# FUNÇÕES
def _cria_individuo():
    individuo = []
    for letra in DEMANDA:
        individuo.extend([letra] * DEMANDA[letra])
    random.shuffle(individuo)
    return individuo

def _tamanho_bin(bin):
    return sum(TECIDO_NECESSARIO[letra] for letra in bin)

def _aptidao(individuo):
    bins = []
    bin_atual = []
    sobra_total = 0

    for g in individuo:
        bin_atual.append(g)
        if _tamanho_bin(bin_atual) > TAMANHO_BIN:
            bin_atual.pop()
            bins.append(bin_atual.copy())
            sobra_total += TAMANHO_BIN - _tamanho_bin(bin_atual)
            bin_atual = [g]

    if bin_atual:
        bins.append(bin_atual.copy())
        sobra_total += TAMANHO_BIN - _tamanho_bin(bin_atual)

    return sobra_total, bins

def _verifica_demanda(individuo):
    contagem = {k: 0 for k in DEMANDA}
    for gene in individuo:
        contagem[gene] += 1
    return all(contagem[k] == DEMANDA[k] for k in DEMANDA)

def cruzamento(pai1, pai2):
    filho = []
    contador = {k: 0 for k in DEMANDA}
    base = random.choice([pai1, pai2])

    for gene in base:
        if contador[gene] < DEMANDA[gene]:
            filho.append(gene)
            contador[gene] += 1

    outro = pai2 if base == pai1 else pai1
    for gene in outro:
        if contador[gene] < DEMANDA[gene]:
            filho.append(gene)
            contador[gene] += 1

    return filho

# INICIALIZA POPULAÇÃO
populacao = [_cria_individuo() for _ in range(QUANTIDADE_INDIVIDUOS)]

for geracao in range(NUM_GERACOES):
    # APTIDÃO E SELEÇÃO
    populacao = sorted(populacao, key=lambda ind: _aptidao(ind)[0])
    elite_qtd = int(ELITE * QUANTIDADE_INDIVIDUOS)
    elite = populacao[:elite_qtd]

    # NOVOS FILHOS
    filhos = []
    for _ in range(QUANTIDADE_INDIVIDUOS - elite_qtd):
        p1 = elite[0]  # melhor sempre
        p2 = random.choice(elite)
        filho = cruzamento(p1, p2)
        if not _verifica_demanda(filho):
            print("Erro: filho inválido")
        filhos.append(filho)

    populacao = elite + filhos

    melhor_aptidao = _aptidao(populacao[0])[0]
    print(f"Geração {geracao+1}/{NUM_GERACOES} | Melhor desperdício: {melhor_aptidao:.2f}")

# RESULTADO FINAL
mais_adaptado = populacao[0]
sobra_total, bins = _aptidao(mais_adaptado)
print("\nMelhor indivíduo:")
print(mais_adaptado)
print(f"Desperdício total: {sobra_total:.2f} metros")
print(f"Total de bins usados: {len(bins)}")
