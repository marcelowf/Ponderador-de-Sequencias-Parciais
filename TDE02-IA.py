import random

def imprimirMesa(mesa):
    print("┌─┬─┬─┬─┐")
    for i in range(4):
        print("│" + "│".join(mesa[i]) + "│")
        if i != 3:
            print("├─┼─┼─┼─┤")
    print("└─┴─┴─┴─┘")

def verificarMesaCheia(mesa):
    for linha in mesa:
        if " " in linha:
            return False
    return True

def verificarVitoria(mesa, jogador):
    for i in range(4):
        if all([mesa[i][j] == jogador 
                for j in range(4)]):
            return True

    for j in range(4):
        if all([mesa[i][j] == jogador 
                for i in range(4)]):
            return True
    
    if all([mesa[i][i] == jogador 
            for i in range(4)]
        ) or all([mesa[i][3-i] == jogador 
                for i in range(4)]):
        return True
    
    return False

def avaliarMinimax(mesa, jogador):
    oponente = 'O' if jogador == 'X' else 'X'
    pontuacao = 0
    
    # Verificar linhas
    for i in range(4):
        linha_jogador = sum([1 for j in range(4) if mesa[i][j] == jogador])
        linha_oponente = sum([1 for j in range(4) if mesa[i][j] == oponente])
        if linha_oponente == 0:
            if linha_jogador == 4:
                return 10  # Vitória garantida
            elif linha_jogador == 3:
                pontuacao += 5
            elif linha_jogador == 2:
                pontuacao += 2
        if linha_jogador == 0:
            if linha_oponente == 4:
                return -10  # Derrota garantida
            elif linha_oponente == 3:
                pontuacao -= 5
            elif linha_oponente == 2:
                pontuacao -= 2

    # Verificar colunas
    for j in range(4):
        coluna_jogador = sum([1 for i in range(4) if mesa[i][j] == jogador])
        coluna_oponente = sum([1 for i in range(4) if mesa[i][j] == oponente])
        if coluna_oponente == 0:
            if coluna_jogador == 4:
                return 10  # Vitória garantida
            elif coluna_jogador == 3:
                pontuacao += 5
            elif coluna_jogador == 2:
                pontuacao += 2
        if coluna_jogador == 0:
            if coluna_oponente == 4:
                return -10  # Derrota garantida
            elif coluna_oponente == 3:
                pontuacao -= 5
            elif coluna_oponente == 2:
                pontuacao -= 2

    # Verificar diagonais
    diagonal_jogador1 = sum([1 for i in range(4) if mesa[i][i] == jogador])
    diagonal_oponente1 = sum([1 for i in range(4) if mesa[i][i] == oponente])
    if diagonal_oponente1 == 0:
        if diagonal_jogador1 == 4:
            return 10
        elif diagonal_jogador1 == 3:
            pontuacao += 5
        elif diagonal_jogador1 == 2:
            pontuacao += 2
    if diagonal_jogador1 == 0:
        if diagonal_oponente1 == 4:
            return -10
        elif diagonal_oponente1 == 3:
            pontuacao -= 5
        elif diagonal_oponente1 == 2:
            pontuacao -= 2

    diagonal_jogador2 = sum([1 for i in range(4) if mesa[i][3-i] == jogador])
    diagonal_oponente2 = sum([1 for i in range(4) if mesa[i][3-i] == oponente])
    if diagonal_oponente2 == 0:
        if diagonal_jogador2 == 4:
            return 10
        elif diagonal_jogador2 == 3:
            pontuacao += 5
        elif diagonal_jogador2 == 2:
            pontuacao += 2
    if diagonal_jogador2 == 0:
        if diagonal_oponente2 == 4:
            return -10
        elif diagonal_oponente2 == 3:
            pontuacao -= 5
        elif diagonal_oponente2 == 2:
            pontuacao -= 2

    return pontuacao

def minimax(mesa, profundidade, is_maximizando, jogador, alpha, beta, max_depth):
    oponente = 'O' if jogador == 'X' else 'X'
    
    if verificarVitoria(mesa, jogador):
        return 10 - profundidade
    if verificarVitoria(mesa, oponente):
        return profundidade - 10
    if verificarMesaCheia(mesa) or profundidade >= max_depth:
        return avaliarMinimax(mesa, jogador)
    
    if is_maximizando:
        melhor_valor = -float('inf')
        for i in range(4):
            for j in range(4):
                if mesa[i][j] == " ":
                    mesa[i][j] = jogador
                    valor_atual = minimax(mesa, profundidade + 1, False, jogador, alpha, beta, max_depth)
                    mesa[i][j] = " "
                    melhor_valor = max(melhor_valor, valor_atual)
                    alpha = max(alpha, valor_atual)
                    if beta <= alpha:
                        break
        return melhor_valor
    else:
        melhor_valor = float('inf')
        for i in range(4):
            for j in range(4):
                if mesa[i][j] == " ":
                    mesa[i][j] = oponente
                    valor_atual = minimax(mesa, profundidade + 1, True, jogador, alpha, beta, max_depth)
                    mesa[i][j] = " "
                    melhor_valor = min(melhor_valor, valor_atual)
                    beta = min(beta, valor_atual)
                    if beta <= alpha:
                        break
        return melhor_valor

def jogadaMinimax(mesa, jogador, usar_poda, max_depth):
    melhor_valor = -float('inf')
    melhor_jogada = None
    alpha = -float('inf')
    beta = float('inf')
    
    for i in range(4):
        for j in range(4):
            if mesa[i][j] == " ":
                mesa[i][j] = jogador
                if usar_poda:
                    valor_atual = minimax(mesa, 0, False, jogador, alpha, beta, max_depth)
                else:
                    valor_atual = minimax(mesa, 0, False, jogador, -float('inf'), float('inf'), max_depth)
                mesa[i][j] = " "
                if valor_atual > melhor_valor:
                    melhor_valor = valor_atual
                    melhor_jogada = (i, j)
    return melhor_jogada

def main():
    mesa = [[" " for _ in range(4)] for _ in range(4)]
    print("Jogo da Velha 4x4")
    print("1- Humano vs Computador")
    print("2- Computador vs Computador")
    modo = int(input("Escolha: "))

    print("Estratégia do Computador")
    print("1- Aleatória")
    print("2- Minimax")
    print("3- Minimax com Alfa-Beta")
    estrategia = int(input("Escolha: "))
    
    if estrategia == 2 or estrategia == 3:
        max_depth = int(input("Escolha a profundidade máxima para Minimax (ex: 1, 2, 3...): "))
    
    jogador = 'X'
    while True:
        imprimirMesa(mesa)
        
        if verificarVitoria(mesa, 'X'):
            print("Jogador X venceu!")
            break
        if verificarVitoria(mesa, 'O'):
            print("Jogador O venceu!")
            break
        if verificarMesaCheia(mesa):
            print("Empate!")
            break
        
        if modo == 2 or (modo == 1 and jogador == 'O'):
            if estrategia == 1:
                jogadas_possiveis = [(i, j) for i in range(4) for j in range(4) if mesa[i][j] == " "]
                i, j = random.choice(jogadas_possiveis)
            elif estrategia == 2:
                i, j = jogadaMinimax(mesa, jogador, False, max_depth)
            elif estrategia == 3:
                i, j = jogadaMinimax(mesa, jogador, True, max_depth)
        else:
            while True:
                try:
                    i, j = map(int, input("Digite linha e coluna (0-3) para jogar (separado por espaço): ").split())
                    if mesa[i][j] == " ":
                        break
                    else:
                        print("Posição já ocupada! Tente novamente.")
                except ValueError:
                    print("Entrada inválida! Por favor, digite dois números separados por espaço (ex: 1 2).")
                except IndexError:
                    print("Entrada fora do limite! Certifique-se de digitar números entre 0 e 3.")
        
        mesa[i][j] = jogador
        jogador = 'O' if jogador == 'X' else 'X'

main()