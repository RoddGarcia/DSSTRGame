import pygame
from menu import main_menu
from fase1 import main as fase1_main
from fase2 import main as fase2_main
from tiles0 import main as tiles_main

largura_tela = 800
altura_tela = 800

fases = [main_menu, 
         fase1_main, 
         fase2_main,
         2]

def main():
    fase_atual = 0
    pygame.display.set_caption("D.S.S.T.R")

    while fase_atual < len(fases):
        resultado = fases[fase_atual]()

        if resultado == "Jogar":
            fase_atual += 1
            pygame.mixer.music.stop() 

        pygame.display.update()

        if fase_atual == len(fases) - 1:
            pygame.quit()
            quit()

if __name__ == "__main__":
    main()
