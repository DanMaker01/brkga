# Problema de Corte de Estoque (CSP) aplicado ao corte de tecido

🧩 O **Cutting Stock Problem (CSP)**, ou **problema de corte de estoque**, é um desafio clássico de otimização combinatória.  
Nele, o objetivo é determinar como cortar itens de diferentes tamanhos a partir de rolos de comprimento fixo, minimizando o desperdício de material ou o número de rolos utilizados.  

Neste projeto, o foco é o corte de **camisas de tamanhos variados** — P, M, G e GG — em **rolos de tecido de 5 metros**, respeitando uma demanda fixa para cada tipo.

---

## 🔬 Algoritmo Utilizado

🧬 O **BRKGA (Biased Random-Key Genetic Algorithm)** é uma abordagem evolutiva baseada em genes representados por números reais no intervalo `[0,1]`.  
Cada indivíduo da população é um vetor que, ao ser ordenado, define uma **sequência de corte**.  

O algoritmo combina:
- **elitismo** (manutenção dos melhores indivíduos),  
- **mutantes aleatórios**, e  
- **crossover enviesado**,  

para equilibrar **exploração** e **exploração**, otimizando progressivamente a alocação dos cortes ao longo das gerações.

---

## 🎮 Visualização Interativa

A aplicação conta com uma **interface interativa em Pygame**, que permite observar em tempo real:  
- o desempenho das soluções, e  
- o comportamento da população ao longo das gerações.  

Além disso, existe uma versão **automatizada** voltada para **testes de performance e experimentos**.  
Os dados gerados são exportados em arquivos `.csv` com timestamp, e gráficos são produzidos em **Matplotlib** para analisar o **desperdício de tecido** e a **eficiência dos cortes**.

---

## ▶️ Execução

Para rodar o código, utilize:

```bash
python main.py
```
---

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
