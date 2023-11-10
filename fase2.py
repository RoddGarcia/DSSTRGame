import pygame
import random
import math
import time

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("Assets/SFX/Game On - Tricycle Riot.mp3")

pygame.mixer.music.set_volume(0.5)

pygame.mixer.music.play(-1)

largura_tela = 800
altura_tela = 600
branco = (255, 255, 255)
verde = (0, 255, 0)
vermelho = (255, 0, 0)
azul = (0, 0, 255)
amarelo = (255, 255, 0)
cinza = (128, 128, 128)
preto = (0, 0, 0)

jogador_x = 150
jogador_y = 555

refens = []
num_refens = 1

obstaculos = []
num_obstaculos = 20

paredes = []
num_paredes = 1

clock = pygame.time.Clock()

fonte = pygame.font.Font(None, 24)
tempo_inicial = time.time()
tempo_limite = 200

refens_salvos = 0

bar_x, bar_y = 180, 550
bar_width, bar_height = 400, 20
progress_color = (0, 255, 0)
cpr = 0
max_cpr = 100
progresso_enfaixamento = 0
progresso_tala = 0
em_acao = False
decremento_cpr = 5  # Valor a ser decrementado
limite_cpr = -1   # Limite mínimo
tempo_decremento = 1  # Tempo em segundos
tempo_ultimo_decremento = time.time()
pressed_space = False
mensagem = None

player_img = pygame.image.load("./Assets/Player/CharacterDown2.png")
player_img = pygame.transform.scale(player_img, (70, 70))

bg_img = pygame.image.load("./Assets/Mapa1.2.png")
bg_img = pygame.transform.scale(bg_img, (largura_tela, altura_tela))

curativo_azul_img = pygame.image.load("./Assets/compressa.png")
curativo_azul_img = pygame.transform.scale(curativo_azul_img, (70, 70))

curativo_amarelo_img = pygame.image.load("./Assets/bandage.png")
curativo_amarelo_img = pygame.transform.scale(curativo_amarelo_img, (70, 70))

curativo_cinza_img = pygame.image.load("./Assets/tala.png")
curativo_cinza_img = pygame.transform.scale(curativo_cinza_img, (70, 70))

npc_img = pygame.image.load("./Assets/npc.png")
npc_img = pygame.transform.scale(npc_img, (90, 90))

#Classe Player
class Player:

  def __init__(self, x, y, vel):
    self.x = x
    self.y = y
    self.vel = vel
    self.refens_salvos = 0
    self.velocidade = vel
    self.player_frames = []
    self.frames_index = 0
    self.direction = "down"
    self.frame = 0
    self.last_frame_update = pygame.time.get_ticks()
    self.down1 = pygame.image.load("./Assets/Player/CharacterDown1.png")
    self.down1 = pygame.transform.scale(self.down1, (70, 70))
    self.down2 = pygame.image.load("./Assets/Player/CharacterDown2.png")
    self.down2 = pygame.transform.scale(self.down2, (70, 70))

    self.up1 = pygame.image.load("./Assets/Player/CharacterUp1.png")
    self.up1 = pygame.transform.scale(self.up1, (70, 70))
    self.up2 = pygame.image.load("./Assets/Player/CharacterUp2.png")
    self.up2 = pygame.transform.scale(self.up2, (70, 70))

    self.left1 = pygame.image.load("./Assets/Player/CharacterLeft1.png")
    self.left1 = pygame.transform.scale(self.left1, (70, 70))
    self.left2 = pygame.image.load("./Assets/Player/CharacterLeft2.png")
    self.left2 = pygame.transform.scale(self.left2, (70, 70))

    self.right1 = pygame.image.load("./Assets/Player/CharacterRight1.png")
    self.right1 = pygame.transform.scale(self.right1, (70, 70))
    self.right2 = pygame.image.load("./Assets/Player/CharacterRight2.png")
    self.right2 = pygame.transform.scale(self.right2, (70, 70))
    # dicionário que representa o inventário
    self.curativo_coletados = {'Azul': 0, 'Amarelo': 0, 'Cinza': 0}

  player_frames_img = 0
  player_frames_delay = 5

  def mover(self):
    keys = pygame.key.get_pressed()
    frame_duration = 100 # duração da animação
    moving = any(keys[key] for key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN])

    if moving:
      if keys[pygame.K_LEFT] and self.x > 0:
        self.x -= self.vel
        self.direction = "left"
      elif keys[pygame.K_RIGHT] and self.x < largura_tela - 30:
        self.x += self.vel
        self.direction = "right"
      elif keys[pygame.K_DOWN] and self.y < altura_tela - 30:
        self.y += self.vel
        self.direction = "down"
      elif keys[pygame.K_UP] and self.y > 0:
        self.y -= self.vel
        self.direction = "up"

      # definindo a imagem e a duração dela
      current_time = pygame.time.get_ticks()
      if current_time - self.last_frame_update > frame_duration:
        self.frame = (self.frame + 1) % 2 
        self.last_frame_update = current_time
    else:
        self.frame = 1

  def desenhar(self, tela):
    if self.direction == "down":
      tela.blit(self.down1 if self.frame == 0 else self.down2, (self.x - 20, self.y - 20))
    elif self.direction == "up":
      tela.blit(self.up1 if self.frame == 0 else self.up2, (self.x - 20, self.y - 20))
    elif self.direction == "left":
      tela.blit(self.left1 if self.frame == 0 else self.left2, (self.x - 20, self.y - 20))
    elif self.direction == "right":
      tela.blit(self.right1 if self.frame == 0 else self.right2, (self.x - 20, self.y - 20))

  def coletar_curativos(self, curativos):
    for curativo in curativos:
      if pygame.Rect(self.x, self.y, 30, 30).colliderect(pygame.Rect(curativo[0], curativo[1], 10, 10)):
        curativos.remove(curativo)
        if curativo[2] == azul:
          resgate_item_sfx = pygame.mixer.Sound("Assets/SFX/resgate_item.mp3")
          resgate_item_sfx.play()
          self.curativo_coletados['Azul'] += 1
        elif curativo[2] == amarelo:
          resgate_item_sfx = pygame.mixer.Sound("Assets/SFX/resgate_item.mp3")
          resgate_item_sfx.play()
          self.curativo_coletados['Amarelo'] += 1
        elif curativo[2] == cinza:
          resgate_item_sfx = pygame.mixer.Sound("Assets/SFX/resgate_item.mp3")
          resgate_item_sfx.play()
          self.curativo_coletados['Cinza'] += 1

  def verificar_colisao_obstaculos(self, obstaculos):
    for obstaculo in obstaculos:
      obstaculo_rect = pygame.Rect(obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[2])
      if pygame.Rect(self.x, self.y, 30, 30).colliderect(obstaculo_rect):
        return True
    return False
  
  def verificar_colisao_paredes(self, paredes):
    for parede in paredes:
      # print(f"parede {parede}")
      parede_rect = pygame.Rect(parede)
      if pygame.Rect(self.x, self.y, 30, 30).colliderect(parede_rect):
        return True
    return False
  
#Classe Refem
class Refem:
  #Ajustar o que precisa ser feito em cada fase com base nas necessidades dos npc's
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.salvo = False
    self.pulso = False
    self.sangrando = True
    self.fraturado = True

  # verificar o inventário do jogador
  def verificar_jogador(self, jogador):
    cada_item = all(qtd > 0 for qtd in jogador.curativo_coletados.values())

    for refem in refens:
      if cada_item and refem.fraturado == False:
        for x in jogador.curativo_coletados:
          
          refem_salvo_sfx = pygame.mixer.Sound("Assets/SFX/refem_salvo.mp3")

          refem_salvo_sfx.play()
          jogador.curativo_coletados[x] -= 1

        jogador.refens_salvos += 1
        refens.remove(self)

def avancar_fase():
    if refens_salvos == num_refens:
      return True
    else:
      return False

# lista de posições diferentes para spawnar obstáculos
posicoes_obstaculos = [(95,380), (195,290), (205,75), 
                       (275,130), (545,80), (530,290), 
                       (670,120), (670,365), (540,445),
                       (305,480)]

posicoes_curativos = [
        (25,485), (25,420), (25,355), (135,355),
        (135,240), (135,135), (135,35), (315,165),
        (510,165), (595,40), (595,255), (595,365),
        (730,155), (730,330), (730,445), (730,500),
        (590,435), (450,395)]

posicoes_refens = [
        (150,430), (100,155),
        (610,80), (685,255),
        (655,435), (445,520),
]

# lista de posições para spawnar paredes
posicoes_paredes = [
  (0,545,70,50),
  (0,0,80,330),
  (235,0,290,130),
  (690,0,160,120),
  (230,215,300,140),
  (235,560,1070,20),
  (520,485,170,90),
  (300,440,120,40),
  (350,450,120,40),
  (420,460,120,40),
]

def criar_objetos():
  # criar obstaculos
  for _ in range(num_obstaculos):
    x, y = random.choice(posicoes_obstaculos)
    tamanho_obstaculo = random.randint(20, 40)
    obstaculos.append((x, y, tamanho_obstaculo))

  #   # criar paredes invisiveis
  for items in posicoes_paredes:
    paredes.append(items)

  # lista de posições diferentes para spawnar curativos
  posicoes_curativos = [
        (25,485), (25,420), (25,355), (135,355),
        (135,240), (135,135), (135,35), (315,165),
        (510,165), (595,40), (595,255), (595,365),
        (730,155), (730,330), (730,445), (730,500),
        (590,435), (450,395)]

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

  return curativo_azul, curativo_amarelo, curativo_cinza

random.shuffle(posicoes_refens)
refens = [Refem(x, y) for x, y in posicoes_refens[:num_refens]]

def main():
  global jogador_x, jogador_y, nivel_concluido, tempo_restante, cpr, max_cpr, em_acao, pressed_space, progresso_tala
  global tempo_decremento, decremento_cpr, limite_cpr, tempo_ultimo_decremento, mensagem, progresso_enfaixamento

  tela = pygame.display.set_mode((largura_tela, altura_tela))
  pygame.display.set_caption("D.S.S.T.R - Fase 1")

  ###FOGO
  fogo_animacao = pygame.image.load("./Assets/pixil-frame-0.png")
  fogo_animacao = pygame.transform.scale(fogo_animacao, (70, 70))

  fogo_animacao2 = pygame.image.load("./Assets/pixil-frame-1.png")
  fogo_animacao2 = pygame.transform.scale(fogo_animacao2, (70, 70))

  fogo_animacao_frames = [fogo_animacao, fogo_animacao2]  
  fogo_index = 0  
  fogo_duracao = 500  
  fogo_update = pygame.time.get_ticks() 

  curativo_azul, curativo_amarelo, curativo_cinza = criar_objetos()

  jogador = Player(jogador_x, jogador_y, 5)

  while True:
    for evento in pygame.event.get():
      if evento.type == pygame.QUIT:
        pygame.quit()
        quit()

    jogador.mover()
    jogador.coletar_curativos(curativo_azul)
    jogador.coletar_curativos(curativo_amarelo)
    jogador.coletar_curativos(curativo_cinza)
    tela.fill(branco)
    tempo_atual = time.time()

    # paredes invisiveis
    for carac in posicoes_paredes:
      pygame.draw.rect(tela, azul, (carac))

    tela.blit(bg_img, (0,0))
    
    keys = pygame.key.get_pressed()

    # # Apresentar pontos de spawn dos curativos
    # for x, y in posicoes_curativos:
    #   pygame.draw.rect(tela, verde, (x, y, 20, 20))

    # # Apresentar pontos de spawn dos reféns
    # for x, y in posicoes_refens:
      # pygame.draw.rect(tela, amarelo, (x, y, 20, 20))
    
    # # # Apresentar pontos de spawn dos obstáculos
    # for x, y in posicoes_obstaculos:
    #   pygame.draw.rect(tela, vermelho, (x, y, 20, 20))

    # verificar se jogador toca na parede 
    if jogador.verificar_colisao_paredes(paredes):
      if keys[pygame.K_LEFT] and jogador.x > 0:
        jogador.x += jogador.vel 
      if keys[pygame.K_RIGHT] and jogador.x < largura_tela - 30:
        jogador.x -= jogador.vel 
      if keys[pygame.K_DOWN] and jogador.y < altura_tela - 30:
        jogador.y -= jogador.vel 
      if keys[pygame.K_UP] and jogador.y > 0:
        jogador.y += jogador.vel 

    # jogador toca no obstaculo vermelho
    if jogador.verificar_colisao_obstaculos(obstaculos):
      pygame.mixer.music.stop()
      player_morte = pygame.mixer.Sound("Assets/SFX/morte.mp3")
      player_morte.play()

      gameover_text = fonte.render("Você morreu!", True, vermelho)
      tela.blit(gameover_text, (300, 300))
      pygame.display.update()
      pygame.time.delay(3000)
      pygame.quit()
      quit()

    # ao resgatar 3 refens
    if jogador.refens_salvos == num_refens:
      pygame.mixer.music.stop()
      win_text = fonte.render("Você passou de fase!", True, verde)
      tela.blit(win_text, (300, 300))
      pygame.display.update()
      pygame.time.delay(3000)
      pygame.quit()
      # quit()

    tempo_atual = time.time()
    tempo_restante = tempo_limite - (tempo_atual - tempo_inicial)
    if tempo_restante <= 0:
      pygame.mixer.music.stop()
      texto_derrota = fonte.render("Você perdeu! Tempo esgotado.", True, vermelho)
      player_morte = pygame.mixer.Sound("Assets/SFX/morte.mp3")
      player_morte.play()

      tela.blit(texto_derrota, (300, 300))
      pygame.display.update()
      pygame.time.delay(3000)
      pygame.quit()
      quit()

    # verificar o contato entre o jogador e os reféns --> método verificar_jogador
    for refem in refens:
      if pygame.Rect(jogador.x, jogador.y, 30, 30).colliderect(pygame.Rect(refem.x, refem.y, 10, 10)):
        if not refem.pulso:
          mensagem = fonte.render("A vítima está sem pulso! Pressione SPACE repetidamente para reanimá-la!", True, vermelho)
          mensagem_rect = mensagem.get_rect(center=(400, 525))
          tela.blit(mensagem, mensagem_rect)
          pygame.draw.rect(tela, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height))
          progress_width = (cpr / 100) * bar_width
          pygame.draw.rect(tela, progress_color, (bar_x, bar_y, progress_width, bar_height))

          for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:  # Verifica se houve um pressionamento de tecla
              if event.key == pygame.K_SPACE and not pressed_space:  # Verifica se é a tecla de espaço e se não estava previamente pressionada
                cpr += 10
                pressed_space = True  # Define que a tecla SPACE está pressionada
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:  # Verifica se a tecla de espaço foi liberada
              pressed_space = False

        elif refem.pulso and refem.sangrando:
            mensagem = fonte.render("A vítima está sangrando! Pressione E para enfaixá-la!", True, vermelho)
            mensagem_rect = mensagem.get_rect(center=(400, 525))
            tela.blit(mensagem, mensagem_rect)
            pygame.draw.rect(tela, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height))
            progress_width = (progresso_enfaixamento / 100) * bar_width
            pygame.draw.rect(tela, progress_color, (bar_x, bar_y, progress_width, bar_height))

            if keys[pygame.K_e]:
                progresso_enfaixamento += 0.3
                em_acao = True
                if progresso_enfaixamento >= 100:
                    refem.sangrando = False
                    refem.verificar_jogador(jogador)
                    progresso_enfaixamento = 0
            else:
                em_acao = False

        elif refem.pulso and refem.sangrando == False and refem.fraturado:
            mensagem = fonte.render("A vítima está fraturada! Pressione T para colocar uma Tala!", True, vermelho)
            mensagem_rect = mensagem.get_rect(center=(400, 525))
            tela.blit(mensagem, mensagem_rect)
            pygame.draw.rect(tela, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height))
            progress_width = (progresso_tala / 100) * bar_width
            pygame.draw.rect(tela, progress_color, (bar_x, bar_y, progress_width, bar_height))

            if keys[pygame.K_t]:
                progresso_tala += 0.5
                em_acao = True
                if progresso_tala >= 100:
                    refem.fraturado = False
                    refem.verificar_jogador(jogador)
                    progresso_tala = 0
            else:
                em_acao = False

        if cpr >= max_cpr:
            refem.pulso = True
            cpr = 0

        if tempo_atual - tempo_ultimo_decremento >= tempo_decremento and cpr > limite_cpr:
            cpr -= decremento_cpr
            tempo_ultimo_decremento = tempo_atual

    current_time = pygame.time.get_ticks()
    if current_time - fogo_update > fogo_duracao:
      fogo_index = (fogo_index + 1) % len(fogo_animacao_frames)
      fogo_update = current_time

    # TRABALHANDO
    for obstaculo in obstaculos:
      tela.blit(fogo_animacao_frames[fogo_index], (obstaculo[0], obstaculo[1]))
      # pygame.draw.rect(tela, vermelho, (obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[2]))

    # desenhar os reféns
    for refem in refens:
      tela.blit(npc_img, (refem.x-30, refem.y-30))

    # desenhar os curativos
    for curativo in curativo_azul:
      # Utilização de movimentos verticais suaves
      amplitude = 3  
      frequencia = 0.01
      vertical_offset = amplitude * math.sin(frequencia * pygame.time.get_ticks())

      xSin = curativo[0] - curativo_azul_img.get_width() // 2
      ySin = curativo[1] - curativo_azul_img.get_height() // 2 + vertical_offset
      tela.blit(curativo_azul_img, (xSin, ySin))

    for curativo in curativo_amarelo:
            # utilização de movimentos verticais suaves
      amplitude = 3  
      frequencia = 0.01
      vertical_offset = amplitude * math.sin(frequencia * pygame.time.get_ticks())

      xSin = curativo[0] - curativo_amarelo_img.get_width() // 2
      ySin = curativo[1] - curativo_amarelo_img.get_height() // 2 + vertical_offset
      tela.blit(curativo_amarelo_img, (xSin, ySin))

    for curativo in curativo_cinza:
            # utilização de movimentos verticais suaves
      amplitude = 3  
      frequencia = 0.01
      vertical_offset = amplitude * math.sin(frequencia * pygame.time.get_ticks())

      xSin = curativo[0] - curativo_cinza_img.get_width() // 2
      ySin = curativo[1] - curativo_cinza_img.get_height() // 2 + vertical_offset
      tela.blit(curativo_cinza_img, (xSin, ySin))
    
    jogador.desenhar(tela)
    pygame.draw.rect(tela, vermelho, pygame.Rect(jogador.x, jogador.y, 30, 30), 2)# verifica hitbox do jogador

    tempo_atual = time.time()
    texto_tempo = fonte.render("Tempo restante: {:.1f}".format(tempo_restante), True, (0, 0, 0))
    pontos_azuis = fonte.render(f"Pontos azuis: {jogador.curativo_coletados['Azul']}", True, branco)
    pontos_cinzas = fonte.render(f"Pontos amarelos: {jogador.curativo_coletados['Amarelo']}", True, branco)
    pontos_amarelos = fonte.render(f"Pontos cinzas: {jogador.curativo_coletados['Cinza']}", True, branco)
    refens_salvos = fonte.render(f"Reféns salvos: {jogador.refens_salvos}", True, branco)
    coord_do_jogador = fonte.render(f"Coordenadas Jogador: X={jogador.x}, Y={jogador.y}", True, preto)
    tela.blit(pontos_azuis, (10, 10))
    tela.blit(pontos_cinzas, (10, 40))
    tela.blit(pontos_amarelos, (10, 70))
    tela.blit(refens_salvos, (10, 100))
    tela.blit(texto_tempo, (300, 10))
    tela.blit(coord_do_jogador, (0, 500))

    pygame.display.update()
    clock.tick(60)