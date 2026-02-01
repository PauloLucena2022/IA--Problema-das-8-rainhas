from random import randint
import numpy as np
import time 

# Função de Colisões
def colisoes(estado):
    colisoes_number = 0
    n = len(estado)

    for i in range(n):
        for p in range (i + 1, n):

            # Colisão por linha
            if estado[i] == estado[p]:
                colisoes_number += 1

            # Colisão por diagonal
            if abs(estado[i] - estado[p]) == abs(i - p):
                colisoes_number += 1
    return colisoes_number 
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Função para estado inicial
def estado_inicial():
    valor = []

    for _ in range(8):
        valor.append(randint(0, 7)) 

    return valor 
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Função para vizinhos
def vizinhos(estado):
    vizinho = estado.copy()

    coluna = randint(0,7)
    nova_linha = randint(0,7)

    while nova_linha == vizinho[coluna]:
        nova_linha = randint(0,7)

    vizinho[coluna] = nova_linha

    return vizinho 
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Função do Stochastic Hill Climbing
def stochastic_hill_climbing():
    estado_atual = estado_inicial()
    custo_atual = colisoes(estado_atual)
    max_nao_melhoria = 500

    final = []

    iter = 0
    nao_melhoria = 0

    inicio = time.time()

    while nao_melhoria <  max_nao_melhoria and custo_atual > 0:
        iter += 1

        vizinho = vizinhos(estado_atual)
        custo_vizinho = colisoes(vizinho)

        if custo_vizinho < custo_atual:
            estado_atual = vizinho 
            custo_atual = custo_vizinho

            nao_melhoria = 0
        else:
            nao_melhoria += 1

    fim = time.time()

    execucao = fim - inicio 

    final.append(estado_atual)
    final.append(custo_atual)
    final.append(iter)
    final.append(execucao)

    return final # [estado, custo, iterações, execução]
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Executando 50 vezes

#resultados = []
#iter = []
#tempo = []

#for _ in range(50):
#    resultado = stochastic_hill_climbing()

#    resultados.append(resultado)
#    iter.append(resultado[2])
#    tempo.append(resultado[3])

#print(f"\n50 Iterações: {iter}")
#print(f"\n50 Tempos de Execução: {tempo}")
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- 
# Média e Desvios Padrão

#media_iter = np.mean(iter)
#media_tempo = np.mean(tempo)
#std_iter = np.std(iter) 
#std_tempo =  np.std(tempo)

#print(f"\nMédia de Iterações: {media_iter:.2f} / Desvio Padrão de Iterações: {std_iter:.2f}")
#print(f"Média de Tempo de Execução: {media_tempo:.6f} / Desvio Padrão de Tempo de Execução: {std_tempo:.6f}")
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# 5 Melhores soluções distintas encontradas

#solucoes_diferentes = []

#for result in resultados:
#    estado = result[0]
#    repetido = False

#    for solution in solucoes_diferentes:
#        if estado == solution[0]:
#            repetido = True 
#            break 

#    if not repetido:
#        solucoes_diferentes.append(result)

#solucoes_crescente = sorted(solucoes_diferentes, key = lambda x: x[1]) # ordenado pelo custo
#cinco_solucoes = solucoes_crescente[:5]

#print("\n5 Melhores Soluções:\n")

#for solucao in range(5):
#    print(f"Solução {solucao + 1}:\n")
#    print(f"Estado: {cinco_solucoes[solucao][0]}")
#    print(f"Colisões: {cinco_solucoes[solucao][1]}")
#    print(f"Iterações: {cinco_solucoes[solucao][2]}")
#    print(f"Tempo de Execução: {cinco_solucoes[solucao][3]:.6f}")

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Menu da Aplicação

escolha = 0
resultados = []
iter = []
tempo = []

print('-=-' * 20)
print("Stochastic Hill Climbing - Problema das 8 Rainhas")
print('-=-' * 20)

while escolha != 5:

    print('Escolha uma opção abaixo:\n')
    print('1 - Rodar Stochastic Hill Climbing 50 vezes - Problema da 8 Rainhas;')
    print('2 - Mostrar Média/Desvio Padrão de Iterações do número mínimo de iterações necessário para parar o algoritmo;')
    print('3 - Mostrar Média/Desvio Padrão de padrão do tempo de execução do algoritmo;')
    print('4 - Mostrar as cinco melhores soluções distintas encontradas pelo algoritmo')
    print('5 - Finalizar.')

    escolha = int(input('Digite o número da opção desejada:'))
    print('-=-' * 20)

    # ------------------------------------------------------
    if escolha == 1:
        print('===' * 20)
        for _ in range(50):
            resultado = stochastic_hill_climbing()

            resultados.append(resultado)
            iter.append(resultado[2])
            tempo.append(resultado[3])

        print("Êxito na execução! Verifique informações sobre os resultados com as outras opções!")
        print('===' * 20)
    # ------------------------------------------------------
    elif escolha == 2:
        print('===' * 20)
        if len(resultados) == 0 :
            print("Desculpa, rode o Stochastic Hill Climbing para prosseguir!")
        
        else:
            media_iter = np.mean(iter)
            std_iter = np.std(iter) 

            print(f"Média de Iterações: {media_iter:.2f} / Desvio Padrão de Iterações: {std_iter:.2f}")
        print('===' * 20)
    # ------------------------------------------------------
    elif escolha == 3:
        print('===' * 20)
        if len(resultados) == 0 :
            print("Desculpa, rode o Stochastic Hill Climbing para prosseguir!")
        
        else:
            media_tempo = np.mean(tempo)
            std_tempo =  np.std(tempo)

            print(f"Média de Tempo de Execução: {media_tempo:.6f} / Desvio Padrão de Tempo de Execução: {std_tempo:.6f}")
        print('===' * 20)
    # ------------------------------------------------------
    elif escolha == 4:
        print('===' * 20)
        if len(resultados) == 0 :
            print("Desculpa, rode o Stochastic Hill Climbing para prosseguir!")
        
        else:
            solucoes_diferentes = []

            for result in resultados:
                estado = result[0]
                repetido = False

                for solution in solucoes_diferentes:
                    if estado == solution[0]:
                        repetido = True 
                        break 

                if not repetido:
                    solucoes_diferentes.append(result)

            solucoes_crescente = sorted(solucoes_diferentes, key = lambda x: x[1]) # ordenado pelo custo
            cinco_solucoes = solucoes_crescente[:5]

            print("\n5 Melhores Soluções:")

            for solucao in range(5):
                print(f"\nSolução {solucao + 1}:\n")
                print(f"Estado: {cinco_solucoes[solucao][0]}")
                print(f"Colisões: {cinco_solucoes[solucao][1]}")
                print(f"Iterações: {cinco_solucoes[solucao][2]}")
                print(f"Tempo de Execução: {cinco_solucoes[solucao][3]:.6f}")
        print('===' * 20)
    # ------------------------------------------------------
    elif escolha == 5:
        print("Obrigado por utilizar nosso código!")
        break
    # ------------------------------------------------------
    else:
        print('Opção desconhecida, tente novamente.')
