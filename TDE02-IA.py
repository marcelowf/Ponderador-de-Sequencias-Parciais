import random
import time

def imprimirMesa(mesa):
    print("┌───┬───┬───┬───┐")
    for i in range(4):
        print("│ " + " │ ".join(
            #Colorindo a mesa
            ["\033[91m" + 'X' + "\033[0m" if x == 'X' 
                else "\033[94m" + 'O' + "\033[0m" if x == 'O' 
                    else x for x in mesa[i]]
        ) + " │")
        if i != 3:
            print("├───┼───┼───┼───┤")
    print("└───┴───┴───┴───┘")

def verificarMesaCheia(mesa):
    for linha in mesa:
        if " " in linha:
            return False
    return True

#Verifica todas as linhas, colunas e diagonais
def verificarMesa(mesa, jogador):
    for linha in range(4):
        if all([mesa[linha][coluna] == jogador 
                for coluna in range(4)]):
            return True

    for coluna in range(4):
        if all([mesa[linha][coluna] == jogador 
                for linha in range(4)]):
            return True

    if all([mesa[diagonal][diagonal] == jogador 
            for diagonal in range(4)]
        ) or all([mesa[diagonal][3-diagonal] == jogador 
                for diagonal in range(4)]):
        return True

    return False

#Heurística avalia a posição de Max e Min em três dimensões: linhas, colunas e diagonais. 
#Retorna um valor numérico que representa a pontuação dessa posição para o jogador, que pode ser positivo para vantagem, negativo para desvantagem e zero para neutro.
def avaliarMinimax(mesa, jogador):
    oponente = 'O' if jogador == 'X' else 'X'
    pontuacao = 0

    #Conta quantas posições pertencem ao jogador e ao oponente (linhas, colunas ou diagonais)
    def avaliarSequencia(sequencia, jogador, oponente):
        jogadorCount = sum(1 for posicao in sequencia if posicao == jogador)
        oponenteCount = sum(1 for posicao in sequencia if posicao == oponente)

        #Avalia o oponente
        if oponenteCount == 0:
            if jogadorCount == 4:
                return 10  #Jogador vai vencer
            elif jogadorCount == 3:
                return 5  #Jogador prestes a vencer
            elif jogadorCount == 2:
                return 2  #Jogador tem chance razoável

        #Avalia o jogador
        if jogadorCount == 0:
            if oponenteCount == 4:
                return -10  #Derrota garantida para jogador.
            elif oponenteCount == 3:
                return -5  #Oponente prestes a vencer.
            elif oponenteCount == 2:
                return -2  #Oponente tem chance razoável.

        return 0

    for linha in range(4):
        pontuacao += avaliarSequencia(mesa[linha], jogador, oponente)

    for coluna in range(4):
        coluna_atual = [mesa[linha][coluna] for linha in range(4)]
        pontuacao += avaliarSequencia(coluna_atual, jogador, oponente)

    diagonalPrincipal = [mesa[indice][indice] for indice in range(4)]
    diagonalSecundaria = [mesa[indice][3 - indice] for indice in range(4)]
    pontuacao += avaliarSequencia(diagonalPrincipal, jogador, oponente)
    pontuacao += avaliarSequencia(diagonalSecundaria, jogador, oponente)

    return pontuacao

def minimax(mesa, profundidade, jogadaMax, jogador, alpha, beta, profundidadeMax):
    oponente = 'O' if jogador == 'X' else 'X'

    #Verifica se houve vitória ou empate
    if verificarMesa(mesa, jogador):
        return 10 - profundidade
    if verificarMesa(mesa, oponente):
        return profundidade - 10
    if verificarMesaCheia(mesa) or profundidade >= profundidadeMax:
        return avaliarMinimax(mesa, jogador)

    #Se jogador == max
    if jogadaMax:
        #Melhor valor possível == -infinito
        melhorValor = -float('inf')
        for linha in range(4):
            for coluna in range(4):
                #Se campo == vazio, faz jogada temporária
                if mesa[linha][coluna] == " ":
                    mesa[linha][coluna] = jogador
                    valorAtual = minimax(mesa, profundidade + 1, False, jogador, alpha, beta, profundidadeMax)
                    #Após minimax avaliar, desfaz a jogada
                    mesa[linha][coluna] = " "
                    #Atualiza melhor valor
                    melhorValor = max(melhorValor, valorAtual)
                    if alpha is not None:
                        #Atualiza limite inferior
                        alpha = max(alpha, valorAtual)
                        #Poda
                        if beta is not None and beta <= alpha:
                            break
        return melhorValor
    else:
        #Pior valor possível == +infinito
        melhorValor = float('inf')
        for linha in range(4):
            for coluna in range(4):
                #Se campo == vazio, faz jogada temporária do oponente
                if mesa[linha][coluna] == " ":
                    mesa[linha][coluna] = oponente
                    valorAtual = minimax(mesa, profundidade + 1, True, jogador, alpha, beta, profundidadeMax)
                    #Após minimax avaliar, desfaz a jogada
                    mesa[linha][coluna] = " "
                    #Atualiza pior valor
                    melhorValor = min(melhorValor, valorAtual)
                    if beta is not None:
                        #Atualiza limite superior
                        beta = min(beta, valorAtual)
                        #Poda
                        if alpha is not None and beta <= alpha:
                            break
        return melhorValor

def jogadaMinimax(mesa, jogador, poda, profundidade):
    #Considera a primeira jogada sempre X (Max)
    timerInit = time.time()
    melhorValor = -float('inf')
    melhorJogada = None
    alpha = -float('inf') if poda else None
    beta = float('inf') if poda else None

    for linha in range(4):
        for coluna in range(4):
            #Se campo == vazio, faz primeira jogada temporária e inicia a recurção
            if mesa[linha][coluna] == " ":
                mesa[linha][coluna] = jogador
                valorAtual = minimax(mesa, 0, False, jogador, alpha, beta, profundidade)
                #Após minimax avaliar, desfaz a jogada
                mesa[linha][coluna] = " "
                #Se o valor atual é melhor, Define a melhor jogada
                if valorAtual > melhorValor:
                    melhorValor = valorAtual
                    melhorJogada = (linha, coluna)
    
    timerEnd = time.time()
    print("O Computador demorou " + str(timerEnd - timerInit) + " segundos.")
    return melhorJogada

def escolherEstrategia(jogador):
    print(f"\nEstratégia do Computador {jogador}")
    estrategia = int(input("   1. Aleatória\n   2. Minimax\n   3. Minimax com Alfa-Beta\nEscolha: "))
    profundidade = None
    if estrategia == 2 or estrategia == 3:
        profundidade = int(input(f"Escolha a profundidade máxima para {jogador}: "))
    return estrategia, profundidade

def mostrarJogada(linha, coluna):
    print(f"Jogada: Linha {linha + 1}, Coluna {coluna + 1}")

def main():
    mesa = [[" " for _ in range(4)] for _ in range(4)]
    modo = int(input("Jogo da Velha 4x4\n   1. Humano vs Computador\n   2. Computador vs Computador\nEscolha: "))

    if modo == 1:
        estrategiaO, profundidadeO = escolherEstrategia('O')
        estrategiaX, profundidadeX = None, None
    else:
        estrategiaX, profundidadeX = escolherEstrategia('X')
        estrategiaO, profundidadeO = escolherEstrategia('O')

    jogador = 'X'
    while True:
        imprimirMesa(mesa)
        if verificarMesa(mesa, 'X'):
            print("\nJogador X venceu!")
            break
        elif verificarMesa(mesa, 'O'):
            print("\nJogador O venceu!")
            break
        elif verificarMesaCheia(mesa):
            print("\nEmpate!")
            break

        if modo == 2 or (modo == 1 and jogador == 'O'):
            if jogador == 'X':
                estrategia = estrategiaX
                profundidade = profundidadeX
            else:
                estrategia = estrategiaO
                profundidade = profundidadeO
            if estrategia == 1:
                jogadasPossiveis = [(linha, coluna) for linha in range(4) for coluna in range(4) if mesa[linha][coluna] == " "]
                linha, coluna = random.choice(jogadasPossiveis)
            elif estrategia == 2:
                linha, coluna = jogadaMinimax(mesa, jogador, False, profundidade)
            elif estrategia == 3:
                linha, coluna = jogadaMinimax(mesa, jogador, True, profundidade)
        else:
            while True:
                try:
                    linha, coluna = map(int, input("Digite linha e coluna (separado por espaço): ").split())
                    if mesa[linha][coluna] == " ":
                        break
                    else:
                        print("Posição já ocupada! Tente novamente.")
                except ValueError:
                    print("Entrada inválida! Digite números separados por espaço.")
                except IndexError:
                    print("Entrada fora do limite! Digite números de 0 a 3.")

        mesa[linha][coluna] = jogador
        mostrarJogada(linha, coluna)
        jogador = 'O' if jogador == 'X' else 'X'

main()
