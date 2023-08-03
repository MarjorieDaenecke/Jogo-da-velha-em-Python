import os #biblioteca para as matrizes
import time 
from termcolor import colored
from random import random, choice


#GLOBAL
player_um = ""  # Variável global para armazenar o nome do primeiro jogador
player_dois = ""  # Variável global para armazenar o nome do segundo jogador

#Def para dar pausas no terminal e não ficar confuso
def tempo():
    tempo = time.sleep(1)
    
#Menu do jogo
def intro():
    print(colored('| ✰ JOGO DA VELHA ✰ | \n', 'red', 'on_white', attrs=['bold', 'underline']))
    tempo()
    regras = input('Você sabe jogar? \n 1.Sim \n 2.Não \n  ')
    tempo()
    if regras == "1":
        print("Então vamos começar")
        tempo()
    elif regras == "2":
        print(colored('| ✰ REGRAS ✰ | \n', 'red', 'on_white', attrs=['bold', 'underline']))
        print("Vou lhe ensinar passo a passo! ")
        tempo()
        print("1. Você escolherá um tamanho de tabuleiro, ele sempre terá o mesmo número de linhas e colunas.")
        print("2. Jogamos em duas pessoas, na qual uma representa o ¨x¨ e a outra o ¨O¨.")
        print("3.Cada rodada uma pessoa joga e o objetivo é criar uma sequencia de simbolos \n que você representa em uma linha, seja ela na horizontal, na vertical ou na diagonal, desde que seja de ponta á ponta.")
        print("4.Caso isso aconteça o jogador que completou vence, se por um acaso todos os \n espaços tenham sido preenchidos, mas ninguém conseguiu completar uma reta, acontece um empate, conhecido como VELHA. \n \n")
        tempo()
    else:
        tempo()
        print("Não temos essa opção")
        intro()

#criando o  tamanho do tabuleiro que o usuario desejar
def tamanho(size): 
    tabuleiro = [[" " for _ in range(size)] for _ in range(size)] #aqui para o tamanho ela vai criar um espaço branco de acordo com o número inserido
    return tabuleiro #retorna os espaços

#Desenho do tabuleiro
def screen(tabuleiro): #vai exibir o tabuleiro na tela
    os.system("cls") #limpa a tela a cada vez que o jogador jogar
    print("    " + "   ".join(str(i+1) for i in range(len(tabuleiro)))) #gera uma sequência de números que representa as colunas do tabuleiro. O "i+1" serve para começar com 1 
    print("   " + "----" * (len(tabuleiro)-1) + "----")  #Esepara o cabeçalho das linhas do tabuleiro. Remove a repetição da última barra vertical
    for i, linha in enumerate(tabuleiro):
        print(str(i+1) + ":   " + " | ".join(elemento for elemento in linha) + " ")  #Para cada linha, imprime o número da linha seguido dos valores das células separados. i+1 pra começar com 1 e não com 0 e remove a primeira e última barra vertical
        if i < len(tabuleiro) - 1:
            print("   " + "----" * (len(tabuleiro)-1) + "----")  #Após cada linha do tabuleiro para melhorar a legibilidade e remove a repetição da última barra horizontal

#validação de cada jogada 
def jogada(tabuleiro, jogador):
    linha = int(input("Digite o número da linha: ")) - 1 #cordenada de x, -1 pois começamos no 1
    coluna = int(input("Digite o número da coluna: ")) - 1 #cordenada de y, -1 pois começamos no 1

    if (linha < 0) or (linha >= len(tabuleiro)) or (coluna < 0) or (coluna >= len(tabuleiro)): #aqui ira ser contabilizado o tamanho do tabuleiro, caso o numero inserido utrapasse ou seja menor que o tabuleiro, a resposta será invalida
        print("Coordenadas inválidas! Tente novamente.")
        jogada(tabuleiro, jogador) #chamara a função novamente para uma nova resposta
    elif tabuleiro[linha][coluna] != " ": #caso as cordenados colocadas não estejam em branco, significa que ela já foi escolida
        print("Essa posição já está ocupada! Tente novamente.")
        jogada(tabuleiro, jogador) #chamara a função novamente para uma nova resposta

    else:
        tabuleiro[linha][coluna] = jogador #aqui será quando as cordenadas forem validas
        screen(tabuleiro)

#Programa dos players
def dois_players():
    print(colored('| ✰ Player vs Player ✰ | \n', 'red', 'on_white', attrs=['bold', 'underline']))
    tempo()
    player_um = input("Coloque o nome do primeiro jogador: ")
    player_dois = input("Coloque o nome do segundo jogador: ")
    size = int(input("Digite o tamanho do tabuleiro: "))
    if size < 3:
        tempo()
        print("Valor inválido!")
        main()
    else:
        tempo()
        tabuleiro = tamanho(size)
        screen(tabuleiro)
        chances = size ** 2  # Use o operador ** para calcular a potência

    jogador_atual = player_um  # Define o jogador atual como o player 1 (X)

    while True:
        print("Vez de", jogador_atual) #vez da pessoa que ira jogar 
        jogada(tabuleiro, "X" if jogador_atual == player_um else "O")

        chances -= 1

        if chances == 0 or verificar_vitoria(tabuleiro, "X"):
            if verificar_vitoria(tabuleiro, "X"): #caso tenha uma sequencia de "x"
                print("Parabéns,", player_um, "venceu!")
            else:
                print("Empate!") #caso não tem nenhuma sequencia
            break

        if verificar_vitoria(tabuleiro, "O"):  #caso tenha uma sequencia de "y"
            print("Parabéns,", player_dois, "venceu!")
            break

        jogador_atual = player_dois if jogador_atual == player_um else player_um  # Alterna o jogador atual

#Jogadas feitas pelo bot
def bot_play(tabuleiro):
    linhas_vazias = []
    colunas_vazias = []

    for i in range(len(tabuleiro)):
        if " " in tabuleiro[i]:
            linhas_vazias.append(i)

    for j in range(len(tabuleiro[0])):
        coluna = [tabuleiro[i][j] for i in range(len(tabuleiro))]
        if " " in coluna:
            colunas_vazias.append(j)

    if len(linhas_vazias) == 0 or len(colunas_vazias) == 0:
        return None

    while True:
        linha = choice(linhas_vazias) if linhas_vazias else None
        coluna = choice(colunas_vazias) if colunas_vazias else None

        if linha is not None and coluna is not None:
            if tabuleiro[linha][coluna] == " ":
                return linha, coluna
            else:
                # Remover a linha e coluna escolhidas
                linhas_vazias.remove(linha)
                colunas_vazias.remove(coluna)
        else:
            return None

#Verifica o resultado
def verificar_vitoria(tabuleiro, jogador):
    tamanho = len(tabuleiro) #analisa o tamanho do tabuleiro

    # Verificar linhas
    for i in range(tamanho):
        if all(elemento == jogador for elemento in tabuleiro[i]): #aqui ele vai passar pela linha i e ver se TODOS os elementos dela foram preenchidos e são iguais
            return True #para indicar que o jogador venceu, pois todos os elementos são iguais

    # Verificar colunas
    for j in range(tamanho): 
        coluna = [tabuleiro[i][j] for i in range(tamanho)] #mesma coisa, ve se os elementos da coluna j, são iguais
        if all(elemento == jogador for elemento in coluna): #verifica se é igual ao do jogador tbm
            return True #para indicar que o jogador venceu, pois todos os elementos são iguais

    # Verificar diagonal principal
    diagonal_principal = [tabuleiro[i][i] for i in range(tamanho)] #tabuleiro[i][i] pois o mesmo numero da linha é o da coluna
    if all(elemento == jogador for elemento in diagonal_principal):
        return True

    # Verificar diagonal secundária
    diagonal_secundaria = [tabuleiro[i][tamanho - 1 - i] for i in range(tamanho)]
    if all(elemento == jogador for elemento in diagonal_secundaria):
        return True

    return False #caso de velha

# Programa do bot vs jogador
def bot_vs_player():
    print(colored('| ✰ Jogador vs Bot ✰ | \n', 'red', 'on_white', attrs=['bold', 'underline']))
    tempo()
    player_um = input("Coloque seu nome: ")
    size = int(input("Digite o tamanho do tabuleiro: "))
    chances = size ** 2/2
    if size < 3:
        tempo()
        print("Valor inválido!")
        main()
    else:
        tempo()
        tabuleiro = tamanho(size)
        screen(tabuleiro)

    while True:
        print("Vez de", player_um)
        jogada(tabuleiro, "X")

        chances -= 1

        if chances == 0 or verificar_vitoria(tabuleiro, "X"):
            if verificar_vitoria(tabuleiro, "X"):
                print("Parabéns, você venceu!")
            else:
                print("Empate!")
            break

        print("Vez do Bot...")
        tempo()
        bot_move = bot_play(tabuleiro)

        if bot_move is not None:
            linha, coluna = bot_move
            tabuleiro[linha][coluna] = "O"
            screen(tabuleiro)

            if verificar_vitoria(tabuleiro, "O"):
                if modo_jogo == "1":
                    print("O Bot venceu!")
                break
        else:
            print("Empate!")
            break

#Bot ou Jogador vs Jogador (def auxiliar (praticamente a principal))
def modo_jogo():
    global player_um, player_dois #chamando o nome dos players
    print(colored("Modo de jogo: ", 'red', 'on_white', ['bold', 'underline'])) 
    modo = input("1. Bot \n2. Dois Players \n") #opções de jogo
    print("------------------")
    tempo()
    if modo == "1": #caso seja escolhido o bot (IA)
        bot_vs_player()
    elif modo == "2": #caso seja escolhido o modo Player x Player
        dois_players()
    else:
        print("Por favor, insira um valor válido!")
        modo_jogo()

def jogar_dnv():
    reiniciar = int(input("Você quer jogar novamente? \n 1. Sim \n 2. Não"))
    if reiniciar == 1:
        print(colored("Novo jogo: ", 'red', 'on_white', ['bold', 'underline']))
        main()
    elif reiniciar ==2:
        print("Obrigado por ter jogado!")
    else:
        print("Digite um valor valido")
        jogar_dnv()
        
#Caminho principal
def main():
    intro()
    modo_jogo()
    jogar_dnv()



main()
