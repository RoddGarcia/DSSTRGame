import pygame
import sys
import math
import threading

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("Assets/SFX/Play Me Like That Video Game - Josef Bel Habib.mp3")
pygame.mixer.music.set_volume(0.5)

tela = pygame.display.set_mode((800, 600))
pygame.display.set_caption("D.S.S.T.R")

branco = (255, 255, 255)
preto = (0, 0, 0)

font_size = 36
font = pygame.font.Font(None, font_size)

bg_img = pygame.image.load("./Assets/fundoMenu.jpg")
bg_img = pygame.transform.scale(bg_img, (800, 600))

instruc_img = pygame.image.load("./Assets/instrucoesMenu.jpg")
instruc_img = pygame.transform.scale(instruc_img, (800, 600))

icon_img = pygame.image.load("./Assets/iconFundo.png")

def printText(texto, cor, x, y):
    text_surface = font.render(texto, True, cor)
    text_rect = text_surface.get_rect(center=(x, y))
    tela.blit(text_surface, text_rect)

def botao(rect, texto, cor):
    pygame.draw.rect(tela, cor, rect, border_radius=15)
    printText(texto, preto, rect.centerx, rect.centery)

def main_menu():
    while True:
        tela.blit(bg_img, (0, 0))

        # Apply amplitude effect to the icon image scale
        amplitude = 20 * math.sin(0.01 * pygame.time.get_ticks())
        w_escalado = int(icon_img.get_width() + amplitude)
        h_escalado = int(icon_img.get_height() + amplitude)
        icon_escalado = pygame.transform.scale(icon_img, (w_escalado, h_escalado))

        icon_img_rect = icon_escalado.get_rect(center=(400, 100))
        tela.blit(icon_escalado, icon_img_rect.topleft)

        play_botao = pygame.Rect(200, 250, 400, 100)
        botao(play_botao, "Jogar", branco)

        botao_instrucoes = pygame.Rect(200, 400, 400, 100)
        botao(botao_instrucoes, "Instruções", branco)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if play_botao.collidepoint(mouse_pos):
                    click_sfx = pygame.mixer.Sound("Assets/SFX/click.mp3")
                    click_sfx.play()
                    return "Jogar"

                elif botao_instrucoes.collidepoint(mouse_pos):
                    instrucoes_do_jogo()

        pygame.display.flip()

def instrucoes_do_jogo():
    click_sfx = pygame.mixer.Sound("Assets/SFX/click.mp3")
    click_sfx.play()
    while True:
        tela.blit(instruc_img, (0, 0))

        printText("Instruções:", preto, 800 // 2, 100)
        printText("Resgate todos os reféns do mapa.", branco, 800 // 2, 200)
        printText("Busque todos os equipamentos necessários para curá-los.", branco, 800 // 2, 250)
        printText("Siga as instruções que aparecerão na tela.", branco, 800 // 2, 300)
        printText("Criadores: Daniel Aloia, Matheus Barbosa e Rodrigo Garcia.", branco, 800 // 2, 580)

        back_button = pygame.Rect(200, 450, 400, 100)
        botao(back_button, "Back to Menu", branco)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if back_button.collidepoint(mouse_pos):
                    click_sfx = pygame.mixer.Sound("Assets/SFX/click.mp3")
                    click_sfx.play()
                    return

        pygame.display.flip()
