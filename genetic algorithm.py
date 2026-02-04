# Importando bibliotecas
import random 
import numpy 
import time

from deap import algorithms
from deap import base
from deap import creator
from deap import tools


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# =-=-=-=-=-==- FUNÇÕES =-=-=-=-=-=-=-
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


def evaluate(individual):
    """
        Função de avaliação (fitness) para o problema das 8 rainhas com codificação binária.
        
        1. Decodifica o indivíduo de 24 bits em uma lista de 8 posições de rainhas.
        2. Calcula o número total de colisões (ataques) entre as rainhas.
    """

    # 1. Decodificar o indivíduo binário 
    positions = []

    for i in range(NUM_QUEENS):

        # Pega o bloco de 3 bits para a rainha atual
        start_index = i * BITS_PER_QUEEN
        end_index = start_index + BITS_PER_QUEEN
        bits = individual[start_index:end_index]

        binary_string = "".join(map(str, bits))
        position = int(binary_string, 2)
        positions.append(position)

    # 2: Calcular o número de colisões
    num_clashes = 0

    for i in range(NUM_QUEENS):
        for j in range(i + 1, NUM_QUEENS):
                       
            # 1. Verifica ataque na mesma linha
            if positions[i] == positions[j]:
                num_clashes += 1
                   
            # 2. Verifica ataque na diagonal
            if abs(i - j) == abs(positions[i] - positions[j]):
                num_clashes += 1
    
    # retorna o número de colisões
    return (num_clashes,)


def decode_individual(individual):
    """Função auxiliar para decodificar e imprimir uma solução."""
    positions = []
    for i in range(NUM_QUEENS):
        start_index = i * BITS_PER_QUEEN
        end_index = start_index + BITS_PER_QUEEN
        bits = individual[start_index:end_index]
        binary_string = "".join(map(str, bits))
        position = int(binary_string, 2)
        positions.append(position)
    return positions


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# =-=-=-=-=-==- CORPO DO CÓDIGO =-=-=-=-=-=-=-
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# ------ 1. configuração do algoritmo genético ------

NUM_QUEENS = 8  # Número de rainhas (e também de linhas/colunas)
BITS_PER_QUEEN = 3  # 3 bits para representar 8 linhas (0 a 7)
INDIVIDUAL_LENGTH = NUM_QUEENS * BITS_PER_QUEEN  # Comprimento total do cromossomo: 8 * 3 = 24 bits

# - Fitness: O objetivo é minimizar o número de ataques. Usamos peso -1.0.
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

# - Indivíduo: Agora, um indivíduo é uma lista de bits (0s e 1s), com o fitness definido acima.
creator.create("Individual", list, fitness=creator.FitnessMin)

# - Inicialização da Toolbox 
toolbox = base.Toolbox()

# - Gerador de Atributos: O atributo agora é um bit (0 ou 1).
toolbox.register("attr_bool", random.randint, 0, 1)

# - Gerador de Indivíduo: Um indivíduo é criado repetindo o gerador de bits 24 vezes.
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, INDIVIDUAL_LENGTH)

# - Gerador de População: Uma população é simplesmente uma lista de indivíduos.
toolbox.register("population", tools.initRepeat, list, toolbox.individual)



# ------  2. Registro dos Operadores Genéticos  ------ 
CXPB = 0.8  # Taxa de Cruzamento (mate): 80%
MUTPB = 0.03 # Taxa de Mutação (mutate): 3%

toolbox.register("evaluate", evaluate) # - função de avaliação
toolbox.register("Select", tools.selRoulette) # - seleção por roleta
toolbox.register("mate", tools.cxOnePoint) #- Ponto de corte
toolbox.register("mutate", tools.mutFlipBit, indpb=MUTPB) # - Mutação bit flip

def main():
    print('Execução do Algoritmo Genético...')

    NUM_EXECUTIONS = 50
    NGEN = 1000
    POP_SIZE = 20
    ELITISM_SIZE = 1 

    # Listas para armazenar os resultados das 50 execuções
    iteration_counts = []
    execution_times = []

    optimal_results = []
    optimal_solutions_seen = set()


    
    for i in range(NUM_EXECUTIONS):
        start_time = time.time()
        
        # Inicializa a população
        pop = toolbox.population(n=POP_SIZE)
        
        # Avalia a população inicial
        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit
        
        found_solution = False # - Indica se a solução ótima foi encontrada
        gen = 0 # - Contabilizador de geração

        for gen in range(1, NGEN + 1):

            # --- Elitismo: Salva os melhores indivíduos ---
            elites = tools.selBest(pop, k=ELITISM_SIZE)
            elites = [toolbox.clone(ind) for ind in elites]

            # --- Seleção dos Pais (Roleta) ---
            offspring = toolbox.Select(pop, k=POP_SIZE - ELITISM_SIZE)
            offspring = [toolbox.clone(ind) for ind in offspring]

            # --- Cruzamento e Mutação ---
            offspring = algorithms.varAnd(offspring, toolbox, CXPB, 1.0)

            # --- Avaliação dos novos indivíduos ---
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
            
            # --- Nova População (Sobreviventes) ---
            pop[:] = elites + offspring
            
            # --- Critério de Parada: Solução Ótima Encontrada ---
            best_ind = tools.selBest(pop, 1)[0]
            if best_ind.fitness.values[0] == 0:
                found_solution = True
                break
        
        end_time = time.time()
        exec_time = end_time - start_time


        # Armazena os resultados desta execução
        iteration_counts.append(gen)
        execution_times.append(exec_time)

        best_ind_final = tools.selBest(pop, 1)[0]
        if best_ind_final.fitness.values[0] == 0:
            sol_decoded = decode_individual(best_ind_final)
            sol_tuple = tuple(sol_decoded)
            
            if sol_tuple not in optimal_solutions_seen and len(optimal_results) < 5:
                optimal_results.append({
                    'solution': sol_decoded,
                    'generations': gen,
                    'collisions': 0.0,
                    'time': exec_time 
                })
                optimal_solutions_seen.add(sol_tuple)



        print(f"Execução {i+1}/{NUM_EXECUTIONS} | Gerações: {gen} | Tempo: {end_time - start_time:.4f}s | Melhor Fitness: {best_ind_final.fitness.values[0]}")

    # --- b) Cálculo das Estatísticas ---
    print("\n--- Análise Estatística das 50 Execuções ---")
    
    mean_iterations = numpy.mean(iteration_counts)
    std_iterations = numpy.std(iteration_counts)
    print(f"Iterações para parada: Média = {mean_iterations:.2f}, Desvio Padrão = {std_iterations:.2f}")

    mean_time = numpy.mean(execution_times)
    std_time = numpy.std(execution_times)
    print(f"Tempo de execução: Média = {mean_time:.4f}s, Desvio Padrão = {std_time:.4f}s")

    # --- c) Melhores Soluções Encontradas ---
    print("\n--- 5 Melhores Soluções Distintas Encontradas ---")
    if not optimal_results:
        print("Nenhuma solução ótima (fitness 0) foi encontrada nas 50 execuções.")
    else:
        for i, res in enumerate(optimal_results):
            print(f"Solução {i+1}:")
            print(f"  Estado (Decodificado): {res['solution']}")
            print(f"  Colisões: {res['collisions']}")
            print(f"  Interações (Gerações): {res['generations']}")
            print(f"  Tempo: {res['time']:.4f}s")
            print("-" * 45)


if __name__ == "__main__":
    main()

