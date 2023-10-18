#       mudar
#       Testar cenários interativo (terá colisão do player com o cenário do Matheus)
#       O tempo_restante deve aparecer em todos os níves (o tempo restante não resetará)
#       Adicionar música
#       Adicionar efeitos sonoros
#       Adicionar sprites

import pygame
from fase1 import main as fase1_main
from fase2 import main as fase2_main
from fase3 import main as fase3_main
import fase1
import time

pygame.init()

largura_tela = 800
altura_tela = 600

tempo_inicial = time.time()
tempo_limite = 200

fases = [
    fase1_main, 
    fase2_main, 
    fase3_main
    ]

def main():
    fase_atual = 0
    # Configurações iniciais do programa principal
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("D.S.S.T.R")

    while fase_atual < len(fases):
        # Inicialização da fase
        fases[fase_atual]()

        if fase1.nivel_concluido:
            fase_atual += 1

if __name__ == "__main__":
    main()
