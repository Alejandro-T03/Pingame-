import pygame

# Inicialización de Pygame
pygame.init()

# Definición de colores
black = (0, 0, 0)
white = (255, 255, 255)
screen_size = (800, 600)
player_width = 15
player_height = 90

# Configuración de la pantalla
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Estados del juego
class GameState:
    START = "start"
    PLAYING = "playing"
    GAME_OVER = "game_over"

# Inicialización de variables de juego
player_speed = 3
pelota_speed = [3, 3]
score = 0

# Inicialización de coordenadas y velocidad de los jugadores y la pelota
player1_x_coor, player2_x_coor = 50, 750 - player_width
player1_y_coor, player2_y_coor = 300 - player_height // 2, 300 - player_height // 2

pelota_x, pelota_y = 400, 300
game_state = GameState.START
collision_detected = False

# Función para mostrar un texto en la pantalla
def show_text(lines, y_offset=200):
    screen.fill(black)
    for i, line in enumerate(lines):
        text = font.render(line, True, white)
        screen.blit(text, (250, y_offset + i * 50))

# Función para manejar eventos de teclado en diferentes estados
def handle_key_events():
    global player1_y_coor, player2_y_coor, game_state

    keys = pygame.key.get_pressed()

    if game_state == GameState.START:
        if keys[pygame.K_SPACE]:
            game_state = GameState.PLAYING
    elif game_state == GameState.PLAYING:
        # Interacción Player 1
        player1_y_coor = max(0, min(player1_y_coor + (keys[pygame.K_s] - keys[pygame.K_w]) * player_speed, screen_size[1] - player_height))

        # Interacción Player 2
        player2_y_coor = max(0, min(player2_y_coor + (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * player_speed, screen_size[1] - player_height))
    elif game_state == GameState.GAME_OVER:
        if keys[pygame.K_1]:
            reset_game()
            game_state = GameState.PLAYING
        elif keys[pygame.K_2]:
            pygame.quit()
            exit()

# Función para reiniciar el juego
def reset_game():
    global pelota_x, pelota_y, pelota_speed, score
    pelota_x, pelota_y = 400, 300
    pelota_speed = [3, 3]
    score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    handle_key_events()

    if game_state == GameState.START:
        show_text(["¡Bienvenido al juego!", "Presiona ESPACIO para comenzar"])
    elif game_state == GameState.PLAYING:
        # Limitar movimiento de Player 1 y Player 2 dentro de los límites de la pantalla
        player1_y_coor = max(0, min(player1_y_coor, screen_size[1] - player_height))
        player2_y_coor = max(0, min(player2_y_coor, screen_size[1] - player_height))

        if pelota_y > 590 or pelota_y < 10:
            pelota_speed[1] *= -1
            collision_detected = False  # Restablecer la detección de colisiones al cambiar de dirección

        # Salida de la pelota / Derecho e Izquierdo
        if pelota_x > 800 or pelota_x < 0:
            if not collision_detected:
                show_text(["¡La pelota salió! ¿Qué quieres hacer?", "1. Iniciar nuevamente", "2. Salir del juego"], y_offset=200)
                pygame.display.flip()

                waiting_for_input = True
                while waiting_for_input:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_1:
                                reset_game()
                                waiting_for_input = False
                            elif event.key == pygame.K_2:
                                pygame.quit()
                                exit()

                collision_detected = True

        # Movimiento pelota con incremento de velocidad gradual
        pelota_x += pelota_speed[0]
        pelota_y += pelota_speed[1]

        # Aumentar la velocidad gradualmente
        pelota_speed = [speed * 1.0005 if abs(speed) < 10 else speed for speed in pelota_speed]

        screen.fill(black)

        # ------Zona de dibujo
        jugador1 = pygame.draw.rect(screen, white, (player1_x_coor, player1_y_coor, player_width, player_height))
        jugador2 = pygame.draw.rect(screen, white, (player2_x_coor, player2_y_coor, player_width, player_height))
        pelota = pygame.draw.circle(screen, white, (int(pelota_x), int(pelota_y)), 10)
        # ------Zona de dibujo

        # Coliciones
        if pelota.colliderect(jugador1) or pelota.colliderect(jugador2):
            if not collision_detected:
                pelota_speed[0] *= -1
                score += 1
                print("Número de toques:", score)  # Imprime el número de toques en la consola
                collision_detected = True  # Establecer la detección de colisiones después de cambiar la dirección

        # Mostrar el número de toques en la pantalla
        score_text = font.render(f"Número de toques: {score}", True, white)
        screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)