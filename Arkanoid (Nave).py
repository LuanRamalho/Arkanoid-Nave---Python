import pygame

pygame.init()

tamanho_tela = (800, 800)
tela = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption("Break Out")

tamanho_bola = 20
bola = pygame.Rect(100, 500, tamanho_bola, tamanho_bola)  # Ajuste o tamanho da bola
tamanho_jogador = 200
jogador = pygame.Rect(0, 700, tamanho_jogador, 20)

qtd_blocos_linha = 8
qtd_linhas = 7
qtd_total_blocos = qtd_blocos_linha * qtd_linhas

def criar_blocos(qtd_blocos_linha, qtd_linhas):
    altura_tela = tamanho_tela[1]
    largura_tela = tamanho_tela[0]
    distancia_blocos = 5
    largura_bloco = largura_tela / qtd_blocos_linha - distancia_blocos
    altura_bloco = 15
    distancia_linhas = altura_bloco + 10
    
    blocos = []  # Inicializa a lista de blocos
    for j in range(qtd_linhas):
        for i in range(qtd_blocos_linha):
            bloco = pygame.Rect(i * (largura_bloco + distancia_blocos), j * distancia_linhas, largura_bloco, altura_bloco)
            blocos.append(bloco)  # Adiciona o bloco à lista
    return blocos

cores = {
    "branco": (255, 255, 255),
    "preto": (0, 0, 0),
    "amarelo": (255, 255, 0),
    "azul": (0, 0, 255),
    "verde": (0, 255, 0)
}

fim_jogo = False
movimento_bola = [6, -6]  # Aumenta a velocidade da bola

def desenhar_inicio_jogo():
    tela.fill(cores["preto"])
    pygame.draw.rect(tela, cores["azul"], jogador)
    pygame.draw.ellipse(tela, cores["branco"], bola)  # Desenha a bola como uma elipse

def desenhar_blocos(blocos):
    for bloco in blocos:
        pygame.draw.rect(tela, cores["verde"], bloco)

def movimentar_jogador():
    keys = pygame.key.get_pressed()  # Obtém o estado atual das teclas
    if keys[pygame.K_RIGHT]:
        if (jogador.x + tamanho_jogador) < tamanho_tela[0]:
            jogador.x += 8
    if keys[pygame.K_LEFT]:
        if jogador.x > 0:
            jogador.x -= 8    

def movimentar_bola():
    global movimento_bola  # Define como global para modificar o movimento
    bola.x += movimento_bola[0]
    bola.y += movimento_bola[1]
    
    if bola.x <= 0 or bola.x + tamanho_bola >= tamanho_tela[0]:  # Verifica colisão com as paredes
        movimento_bola[0] = -movimento_bola[0]
    if bola.y <= 0:  # Verifica colisão com o teto
        movimento_bola[1] = -movimento_bola[1]
    if bola.y + tamanho_bola >= tamanho_tela[1]:  # Verifica se a bola caiu
        return False  # Retorna False se a bola cair

    if jogador.colliderect(bola):  # Colisão com o jogador
        movimento_bola[1] = -movimento_bola[1]

    for bloco in blocos[:]:  # Itera sobre uma cópia da lista para evitar modificações durante a iteração
        if bloco.colliderect(bola):
            blocos.remove(bloco)
            movimento_bola[1] = -movimento_bola[1]
            break  # Sai do loop após uma colisão para evitar múltiplas remoções

    return True  # Retorna True se a bola não caiu

def atualizar_pontuacao(pontuacao):
    fonte = pygame.font.Font(None, 30)
    texto = fonte.render(f"Pontuação: {pontuacao}", 1, cores["amarelo"])
    tela.blit(texto, (0, 780))
    return pontuacao >= qtd_total_blocos  # Retorna True se todas as blocos foram removidos

blocos = criar_blocos(qtd_blocos_linha, qtd_linhas)
while not fim_jogo:
    desenhar_inicio_jogo()
    desenhar_blocos(blocos)
    fim_jogo = atualizar_pontuacao(qtd_total_blocos - len(blocos))
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fim_jogo = True

    movimentar_jogador()
    if not movimentar_bola():  # Se a bola cair, o jogo acaba
        fim_jogo = True
    
    pygame.display.flip()  # Chama a função para atualizar a tela
    pygame.time.wait(10)  # Diminui a velocidade do loop

pygame.quit()
