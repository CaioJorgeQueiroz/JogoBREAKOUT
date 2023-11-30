
import pygame
from pygame.locals import *

pygame.init()

# Configurações da tela
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout')

# Cores
bg = (234, 218, 184)
block_red = (242, 85, 96)
block_green = (86, 174, 87)
block_blue = (69, 177, 232)
paddle_col = (142, 135, 123)
paddle_outline = (100, 100, 100)
text_col = (78, 81, 139)

# Variáveis do jogo
cols = 6
rows = 6
clock = pygame.time.Clock()
fps = 60
live_ball = False
game_over = 0

# Configuração da fonte
font = pygame.font.SysFont('Constantia', 30)

# Função para desenhar texto
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Criação da parede
width = screen_width // cols
height = 50
blocks = []
for row in range(rows):
    block_row = []
    for col in range(cols):
        block_x = col * width
        block_y = row * height
        rect = pygame.Rect(block_x, block_y, width, height)

        if row < 2:
            strength = 3
        elif row < 4:
            strength = 2
        elif row < 6:
            strength = 1

        block_individual = [rect, strength]
        block_row.append(block_individual)

    blocks.append(block_row)

# Criação da raquete
paddle_height = 20
paddle_width = int(screen_width / cols)
paddle_x = int((screen_width / 2) - (paddle_width / 2))
paddle_y = screen_height - (paddle_height * 2)
paddle_speed = 10
paddle_rect = Rect(paddle_x, paddle_y, paddle_width, paddle_height)
paddle_direction = 0

# Criação da bola
ball_rad = 10
ball_x = paddle_x + (paddle_width // 2) - ball_rad
ball_y = paddle_y - paddle_height
ball_rect = Rect(ball_x, ball_y, ball_rad * 2, ball_rad * 2)
ball_speed_x = 4
ball_speed_y = -4
ball_speed_max = 5

run = True
while run:
    clock.tick(fps)
    screen.fill(bg)

    # Desenho da parede
    for row in blocks:
        for block in row:
            if block[1] == 3:
                block_col = block_blue
            elif block[1] == 2:
                block_col = block_green
            elif block[1] == 1:
                block_col = block_red
            pygame.draw.rect(screen, block_col, block[0])
            pygame.draw.rect(screen, bg, block[0], 2)

    # Desenho da raquete
    key = pygame.key.get_pressed()
    if key[K_LEFT] and paddle_rect.left > 0:
        paddle_rect.x -= paddle_speed
        paddle_direction = -1
    if key[K_RIGHT] and paddle_rect.right < screen_width:
        paddle_rect.x += paddle_speed
        paddle_direction = 1
    pygame.draw.rect(screen, paddle_col, paddle_rect)
    pygame.draw.rect(screen, paddle_outline, paddle_rect, 3)

    # Desenho da bola
    pygame.draw.circle(screen, paddle_col, (ball_rect.x + ball_rad, ball_rect.y + ball_rad), ball_rad)
    pygame.draw.circle(screen, paddle_outline, (ball_rect.x + ball_rad, ball_rect.y + ball_rad), ball_rad, 3)

    # Movimento da bola
    # Colisão com a parede
    for row in blocks:
        for block in row:
            if ball_rect.colliderect(block[0]):
                if abs(ball_rect.bottom - block[0].top) < 5 and ball_speed_y > 0:
                    ball_speed_y *= -1
                if abs(ball_rect.top - block[0].bottom) < 5 and ball_speed_y < 0:
                    ball_speed_y *= -1
                if abs(ball_rect.right - block[0].left) < 5 and ball_speed_x > 0:
                    ball_speed_x *= -1
                if abs(ball_rect.left - block[0].right) < 5 and ball_speed_x < 0:
                    ball_speed_x *= -1

                if block[1] > 1:
                    block[1] -= 1
                else:
                    block[0] = (0, 0, 0, 0)

    # Verifica colisão com as paredes
    if ball_rect.left < 0 or ball_rect.right > screen_width:
        ball_speed_x *= -1

    # Verifica colisão com o topo
    if ball_rect.top < 0:
        ball_speed_y *= -1

    # Verifica se a bola atingiu o fundo
    if ball_rect.bottom > screen_height:
        game_over = -1

    # Verifica a colisão com a raquete
    if ball_rect.colliderect(paddle_rect) and ball_speed_y > 0:
        ball_speed_y *= -1
        ball_speed_x += 0.2 * paddle_direction

    ball_rect.x += ball_speed_x
    ball_rect.y += ball_speed_y

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == MOUSEBUTTONDOWN and not live_ball:
            live_ball = True
            game_over = 0

pygame.quit()