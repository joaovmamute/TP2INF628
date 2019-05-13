"""
Codigo Trabalho Pratico 1 de INF 628

Joao Vitor Rodrigues de Vasconcelos
75772
"""

import gym
import random
import math
import time
import matplotlib.pyplot as plt

def Torneio(P):
    """
    Funcao torneio para o genetico
    """
    rMaior = -math.inf
    rTemp = 0
    for _ in range(10):
        r = random.randint(0,len(P)//1.5 - 1)
        if P[r][0] > rMaior:
            rMaior = P[r][0]
            rTemp = r
    return P[rTemp][1]

def Crossover(Ind1, Ind2):
    """
    Funcao que faz o crossover entre 2 individuos
    """
    tInd1 = Ind1
    tInd2 = Ind2
    Kid1 = []
    Kid2 = []
    r1 = random.randint(0,len(tInd1)//2 - 1)
    r2 = random.randint(len(tInd1)//2,len(tInd1) - 1)
    for x in range(len(tInd1)//2):
        if x < r1:
            Kid1.append(tInd2[x])
            Kid2.append(tInd1[x])
        if x >= r1:
            Kid1.append(tInd1[x])
            Kid2.append(tInd2[x])
    for x in range(len(tInd1)//2,len(tInd1)):
        if x < r2:
            Kid1.append(tInd2[x])
            Kid2.append(tInd1[x])
        if x >= r2:
            Kid1.append(tInd1[x])
            Kid2.append(tInd2[x])
    return Kid1, Kid2

def Mutacao(Kid, e, taxaS):
    """
    Funcao que faz a mutacao
    """
    tAct = []
    cont = 0
    Rep = 1
    if taxaS == 1:
        Rep = random.randint(1,4)
    while Rep > 0:
        r = random.randint(0,len(Kid) - 1)
        E = random.random()*e
        if Rep < 4:
            for y in range(len(Kid[r])):
                tAct.append(Kid[r][y])
                tAct[y] += E
                if tAct[y] > 1:
                    tAct[y] = random.randint(-1000,1000)*0.001
        else:
            for y in range(4):
                tAct.append(random.randint(-1000,1000)*0.001)
        Kid.pop(r)
        Kid.insert(r, tAct)
        Rep -= 1
    return Kid
    
def main():
    """
    Inicio da funcao main
    """
    env = gym.make('BipedalWalker-v2')
    """
    Inicializando as constantes
    """
    Ge = 100
    G = 0
    numInd = 100
    tamInd = 28 
    passos = 504
    Immortals = 5
    MelhorR = -math.inf
    delta = 0
    epsilon = 0.1
    taxaM = 20
    taxaS = 0
    """
    Inicializando as listas
    """
    Ind = []
    Pop = []
    newPop = []
    Dados = []
    BEST = []
    """
    Criando a primeira geração
    """
    for i in range(numInd):
        Ind = []
        for x in range(tamInd):
            acaoT = env.action_space.sample()
            Ind.append(acaoT)
        newPop.append(Ind)
    inicio = time.time()
    for i in range(numInd):             #For para iterar entre os individuos
        rTot = 0
        env.reset()
        for p in range(passos//tamInd): #For para iterar entre os passos do individuo
            for x in range(tamInd):     #For para iterar entre as açoes do individuo
                if p == 0:              #Primeiro passo é tratado como "Inicialização" portanto tem comportamento diferente
                    observation, reward, done, info = env.step(newPop[i][x])
                if p != 0 and x < tamInd//2:
                    observation, reward, done, info = env.step(newPop[i][x + tamInd//2])
                if p != 0 and x >= tamInd//2:
                    break
                rTot += reward
        Pop.append((rTot,newPop[i]))
    Pop.sort(reverse=True)
    fim = time.time()
    MelhorR = Pop[0][0]
    print('_'*79)
    print('Geracao', G)
    print('Melhor recompensa: %.3f' % MelhorR)
    print('Delta: %.3f' % delta)
    print('Tempo gasto: %.3f' % (fim - inicio))
    print('_'*79)
    Dados.append((G,Pop[0][0]))
    """
    Funcao fitness, mantendo o melhor
    """
    newPop = []
    for x in range(numInd//2):
        if x <= Immortals:
            for i in range(Immortals):
                newPop.append(Pop[i][1])
        else:
            R1 = random.randint(0,100)
            R2 = random.randint(0,100)
            sInd1 = Torneio(Pop)
            sInd2 = Torneio(Pop)
            sKid1, sKid2 = Crossover(sInd1, sInd2)
            if R1 < taxaM:
                sKid1 = Mutacao(sKid1, epsilon, taxaS)
            newPop.append(sKid1)
            if R2 < taxaM:
                sKid2 = Mutacao(sKid2, epsilon, taxaS)
            newPop.append(sKid2)
    """
    Iterando entre as geracoes
    """
    for G in range(1,Ge):
        Pop = []
        inicio = time.time()
        for i in range(numInd):             #For para iterar entre os individuos
            rTot = 0
            env.reset()
            for p in range(passos//tamInd): #For para iterar entre os passos do individuo
                for x in range(tamInd):     #For para iterar entre as açoes do individuo
                    if p == 0:              #Primeiro passo é tratado como "Inicialização" portanto tem comportamento diferente
                        observation, reward, done, info = env.step(newPop[i][x])
                    if p != 0 and x < tamInd//2:
                        observation, reward, done, info = env.step(newPop[i][x + tamInd//2])
                    if p != 0 and x >= tamInd//2:
                        break
                    rTot += reward
                if done:
                    break
            Pop.append((rTot,newPop[i]))
        Pop.sort(reverse=True)
        fim = time.time()
        if MelhorR < Pop[0][0]:
            MelhorR = Pop[0][0]
        print('Geracao', G)
        print('Melhor recompensa global: %.3f' % MelhorR)
        print('Melhor recompensa: %.3f' % Pop[0][0])
        Dados.append((G,Pop[0][0]))
        """
        Ajustando constantes para a mutacao
        """
        delta = Dados[G][1] - MelhorR
        if delta >= 0:
            epsilon = 0.1
            taxaM = 20
            taxaS = 0
        else:
            epsilon = 0.4
            taxaM = 80
            taxaS = 1
        print('Delta: %.3f' % delta)
        print('Tempo gasto: %.3f' % (fim - inicio))
        print('_'*79)
        """
        Selecao dos individuos da proxima geracao, mantendo o melhor
        """
        newPop = []
        for x in range(numInd//2):
            R1 = random.randint(0,100)
            R2 = random.randint(0,100)
            sInd1 = Torneio(Pop)
            sInd2 = Torneio(Pop)
            sKid1, sKid2 = Crossover(sInd1, sInd2)
            if x <= Immortals:
                for i in range(Immortals):
                    newPop.append(Pop[i][1])
            else:
                if R1 < taxaM:
                    sKid1 = Mutacao(sKid1, epsilon, taxaS)
                newPop.append(sKid1)
            if R2 < taxaM:
                sKid2 = Mutacao(sKid2, epsilon, taxaS)
            newPop.append(sKid2)
    xDados = []
    yDados = []
    for i in range(len(Dados)):
        xDados.append(Dados[i][0])
        yDados.append(Dados[i][1])
    plt.plot(xDados,yDados)
    plt.xlabel('Gerações')
    plt.ylabel('Valor de Adaptação')
    plt.show()

if __name__ == "__main__":
    main()
    
