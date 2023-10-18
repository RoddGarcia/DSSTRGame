import pygame
import random
import time

pygame.init()

largura_tela = 800
altura_tela = 600
branco = (255, 255, 255)
verde = (0, 255, 0)
vermelho = (255, 0, 0)
azul = (0, 0, 255)
amarelo = (255, 255, 0)
cinza = (128, 128, 128)

jogador_x = largura_tela // 2
jogador_y = altura_tela - 50

pontos_azuis = []

energeticos = []
energetico_chanceDeSpawn = 1
energetico_duracao = 5  # Duração boost em segundos
energetico_boost = 7  # Acréscimo de boost

energetico_timer = None

refens = []

obstaculos = []
num_refens = 1
num_obstaculos = 3

clock = pygame.time.Clock()

fonte = pygame.font.Font(None, 36)
tempo_inicial = time.time()
tempo_limite = 200

refens_salvos = 0

#Classe Player
class Player:

  def __init__(self, x, y, vel):
    self.x = x
    self.y = y
    self.vel = vel
    self.refens_salvos = 0
    self.velocidade = vel

    # Dicionário que representa o inventário
    self.curativo_coletados = {'Azul': 0, 'Amarelo': 0, 'Cinza': 0}

  # Função p/ movimentação
  def mover(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and self.x > 0:
      self.x -= self.vel
    if keys[pygame.K_RIGHT] and self.x < largura_tela - 30:
      self.x += self.vel
    if keys[pygame.K_DOWN] and self.y < altura_tela - 30:
      self.y += self.vel
    if keys[pygame.K_UP] and self.y > 0:
      self.y -= self.vel

  def coletar_curativos(self, curativos):
    for curativo in curativos:
      if pygame.Rect(self.x, self.y, 30, 30).colliderect(pygame.Rect(curativo[0], curativo[1], 10, 10)):
        curativos.remove(curativo)
        if curativo[2] == azul:
          self.curativo_coletados['Azul'] += 1
        elif curativo[2] == amarelo:
          self.curativo_coletados['Amarelo'] += 1
        elif curativo[2] == cinza:
          self.curativo_coletados['Cinza'] += 1

  def verificar_colisao_obstaculos(self, obstaculos):
    for obstaculo in obstaculos:
      obstaculo_rect = pygame.Rect(obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[2])
      if pygame.Rect(self.x, self.y, 30, 30).colliderect(obstaculo_rect):
        return True
    return False

  def boost_speed(self):
    self.vel = energetico_boost

#Classe Refem
class Refem:

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.salvo = False

  # Verificar o inventário do jogador
  def verificar_jogador(self, jogador):
    cada_item = all(qtd > 0 for qtd in jogador.curativo_coletados.values())

    if cada_item:
      for x in jogador.curativo_coletados:
        jogador.curativo_coletados[x] -= 1

      jogador.refens_salvos += 1
      refens.remove(self)

#Classe Energético
class Energetico:

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.radius = 15
    self.pink = (255, 105, 180)
    self.visible = True

  def draw(self, screen):
    if self.visible:
      pygame.draw.circle(screen, self.pink, (self.x, self.y), self.radius)

  def check_collision(self, player):
    if self.visible and pygame.Rect(player.x, player.y, 30, 30).colliderect(
        pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)):
      self.visible = False
      player.boost_speed()

# Lista de posições diferentes para spawnar curativos
posicoes_curativos = [
  (100, 100), (200, 200), (300, 300), (400, 400), (500, 500), (100, 500),
  (200, 400), (300, 300), (400, 200), (500, 100), (600, 100), (700, 200),
  (700, 300), (700, 400), (600, 500), (100, 300), (200, 400), (300, 200),
  (400, 100), (500, 500)
]

# Lista de posições diferentes para spawnar obstáculos
posicoes_obstaculos = [(50, 50), (150, 150), (250, 250), (350, 350),
                       (450, 450), (50, 450), (150, 350), (250, 250),
                       (350, 150), (450, 50)]

def criar_objetos():
  global energetico_timer

  for _ in range(num_obstaculos):
    x, y = random.choice(posicoes_obstaculos)
    tamanho_obstaculo = random.randint(20, 40)
    obstaculos.append((x, y, tamanho_obstaculo))

  posicoes_curativos = [(100, 100), (200, 200), (300, 300), (400, 400),
                        (500, 500), (100, 500), (200, 400), (300, 300),
                        (400, 200), (500, 100), (600, 100), (700, 200),
                        (700, 300), (700, 400), (600, 500), (100, 300),
                        (200, 400), (300, 200), (400, 100), (500, 500)]

  # Escolha aleatória de posições para curativos
  curativo_azul_positions = random.sample(posicoes_curativos, num_refens)
  posicoes_curativos = [pos for pos in posicoes_curativos if pos not in curativo_azul_positions]
  curativo_azul = [(x, y, azul) for x, y in curativo_azul_positions]

  curativo_amarelo_positions = random.sample(posicoes_curativos, num_refens)
  posicoes_curativos = [pos for pos in posicoes_curativos if pos not in curativo_amarelo_positions]
  curativo_amarelo = [(x, y, amarelo) for x, y in curativo_amarelo_positions]

  curativo_cinza_positions = random.sample(posicoes_curativos, num_refens)
  posicoes_curativos = [pos for pos in posicoes_curativos if pos not in curativo_cinza_positions]
  curativo_cinza = [(x, y, cinza) for x, y in curativo_cinza_positions]

  # Criar energetico em posição aleatoria
  if not energetico_timer and random.random() < energetico_chanceDeSpawn:
    energetico = Energetico(random.randint(10, largura_tela - 10),
                            random.randint(10, altura_tela - 200))
    energeticos.append(energetico)
    energetico_timer = time.time() + energetico_duracao

  return curativo_azul, curativo_amarelo, curativo_cinza, energeticos, energetico_timer

for _ in range(num_refens):
  refens = [
    Refem(random.randint(10, largura_tela - 10),
          random.randint(10, altura_tela - 200)) for _ in range(num_refens)]

def main():
  global jogador_x, jogador_y, energetico_timer, nivel_concluido, tempo_restante
  nivel_concluido = False

  tela = pygame.display.set_mode((largura_tela, altura_tela))
  pygame.display.set_caption("D.S.S.T.R")

  curativo_azul, curativo_amarelo, curativo_cinza, energeticos, energetico_timer = criar_objetos()

  jogador = Player(jogador_x, jogador_y, 5)

  # Inicio do loop do jogo
  while not nivel_concluido:

    for evento in pygame.event.get():
      if evento.type == pygame.QUIT:
        pygame.quit()
        quit()

    jogador.mover()
    jogador.coletar_curativos(curativo_azul)
    jogador.coletar_curativos(curativo_amarelo)
    jogador.coletar_curativos(curativo_cinza)
    tela.fill(branco)

    # jogador toca no obstaculo vermelho
    if jogador.verificar_colisao_obstaculos(obstaculos):
      gameover_text = fonte.render("Você morreu!", True, vermelho)
      tela.blit(gameover_text, (300, 300))
      pygame.display.update()
      pygame.time.delay(2000)
      pygame.quit()
      quit()

    # ao resgatar todos os refens
    if jogador.refens_salvos == num_refens:
      win_text = fonte.render("Você passou de fase!", True, verde)
      tela.blit(win_text, (300, 300))
      pygame.display.update()
      pygame.time.delay(2000)
      nivel_concluido = True

    tempo_atual = time.time()
    tempo_restante = tempo_limite - (tempo_atual - tempo_inicial)
    if tempo_restante <= 0:
      texto_derrota = fonte.render("Você perdeu! Tempo esgotado.", True, vermelho)
      tela.blit(texto_derrota, (300, 300))
      pygame.display.update()
      pygame.time.delay(2000)
      pygame.quit()
      quit()

    # Resetar velocidade do player quando o tempo acabar
    if energetico_timer and time.time() >= energetico_timer:
      jogador.vel = 5
      energetico_timer = None

    # Checar colisão com energéticos
    for energetico in energeticos:
      energetico.draw(tela)
      energetico.check_collision(jogador)

    # Verifiquar o contato entre o jogador e os reféns --> método verificar_jogador
    for refem in refens:
      if pygame.Rect(jogador.x, jogador.y, 30, 30).colliderect(pygame.Rect(refem.x, refem.y, 10, 10)):
        refem.verificar_jogador(jogador)

    for obstaculo in obstaculos:
      pygame.draw.rect(tela, vermelho, (obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[2]))

    pygame.draw.rect(tela, (0, 0, 0), pygame.Rect(jogador.x, jogador.y, 30, 30))

    # Desenhar os reféns
    for refem in refens:
      pygame.draw.rect(tela, verde, pygame.Rect(refem.x, refem.y, 10, 10))

    # Desenhar os curativos
    for curativo in curativo_azul:
      pygame.draw.circle(tela, curativo[2], (curativo[0], curativo[1]), 10)

    for curativo in curativo_amarelo:
      pygame.draw.circle(tela, curativo[2], (curativo[0], curativo[1]), 10)

    for curativo in curativo_cinza:
      pygame.draw.circle(tela, curativo[2], (curativo[0], curativo[1]), 10)

    tempo_atual = time.time()
    texto_tempo = fonte.render("Tempo restante: {:.1f}".format(tempo_restante),True, (0, 0, 0))
    fase_atual_texto = fonte.render(("Fase 1"),True, (0, 0, 0))
    pontos_azuis = fonte.render(f"Pontos azuis: {jogador.curativo_coletados['Azul']}", True, azul)
    pontos_cinzas = fonte.render(f"Pontos amarelos: {jogador.curativo_coletados['Amarelo']}", True, azul)
    pontos_amarelos = fonte.render(f"Pontos cinzas: {jogador.curativo_coletados['Cinza']}", True, azul)
    refens_salvos = fonte.render(f"Reféns salvos: {jogador.refens_salvos}",True, azul)
    velocidadedoplayer = fonte.render(f"Velocidade: {jogador.vel}", True, azul)
    tela.blit(pontos_azuis, (10, 10))
    tela.blit(velocidadedoplayer, (500, 10))
    tela.blit(pontos_cinzas, (10, 40))
    tela.blit(fase_atual_texto, (20, 500))
    tela.blit(pontos_amarelos, (10, 70))
    tela.blit(refens_salvos, (10, 100))
    tela.blit(texto_tempo, (300, 10))

    pygame.display.update()
    clock.tick(60)