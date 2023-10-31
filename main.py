#       mudar
#       Testar cenários interativo (terá colisão do player com o cenário do Matheus)
import pygame
from fase1 import main as fase1_main  # Importar a fase 1
from fase2 import main as fase2_main  # Importar a fase 2
from fase1 import avancar_fase
from tiles0 import main as tiles_main  # Importar a fase teste

pygame.init()

largura_tela = 800
altura_tela = 800

fases = [fase1_main, tiles_main, fase2_main]

def main():
  fase_atual = 0
  # Configurações iniciais do programa principal
  tela = pygame.display.set_mode((largura_tela, altura_tela))
  pygame.display.set_caption("D.S.S.T.R")

  for _ in fases:
    # Inicialização da fase
    fases[fase_atual]()
    # pygame.display.update()

    if avancar_fase():
      fase_atual += 1

if __name__ == main():
  main()
