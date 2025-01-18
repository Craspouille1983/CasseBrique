import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
screen_width = 800
screen_height = 600

# Créer la fenêtre de jeu
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Casse-Brique")

# Couleurs
background_color = (0, 0, 0)  # Noir
ball_color = (255, 255, 255)  # Blanc
paddle_color = (255, 20, 147)  # Deeppink
brick_color = (0, 255, 0)  # Vert
text_color = (255, 255, 255)  # Blanc

# Propriétés de la balle
ball_radius = 10
ball_x = screen_width // 2
ball_y = screen_height // 2
ball_speed_x = .25
ball_speed_y = .25

# Propriétés de la raquette
paddle_width = 100
paddle_height = 10
paddle_x = (screen_width - paddle_width) // 2
paddle_y = screen_height - 30
paddle_speed = 3

# Propriétés des briques
brick_width = 60
brick_height = 20
bricks = []
num_columns = 10
num_rows = 5

# Générer les briques
for row in range(num_rows):
    for col in range(num_columns):
        brick_x = col * (brick_width + 10) + 35  # Espace entre les briques
        brick_y = row * (brick_height + 5) + 50  # Espace entre les lignes de briques
        bricks.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))

# Score
score = 0
font = pygame.font.Font("assets/fonts/SFAlienEncounters.ttf", 36)

# Fonction pour afficher l'écran d'accueil
def show_start_screen():
    screen.fill(background_color)
    title_font = pygame.font.Font('assets/fonts/SFAlienEncounters-Italic.ttf', 60)
    instructions_font = pygame.font.Font('assets/fonts/SFAlienEncountersSolid.ttf', 36)

    # Afficher le titre
    title_text = title_font.render("Casse-Brique", True, text_color)
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))
    screen.blit(title_text, title_rect)

    # Afficher les instructions
    instructions_text = instructions_font.render("Appuyez sur Espace pour commencer", True, text_color)
    instructions_rect = instructions_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(instructions_text, instructions_rect)

    pygame.display.flip()

# Fonction pour gérer la collision avec les briques
def handle_collision_with_bricks(ball_rect, ball_speed_x, ball_speed_y, bricks, score):
    for brick in bricks[:]:
        if ball_rect.colliderect(brick):
            bricks.remove(brick)  # Supprimer la brique
            pygame.mixer.Sound('assets/sounds/pop.mp3').play()
            score += 10  # Ajouter des points au score

            # Calculer la direction du rebond
            brick_centerx = brick.centerx
            brick_centery = brick.centery
            ball_centerx = ball_rect.centerx
            ball_centery = ball_rect.centery

            if ball_centerx < brick_centerx:
                ball_speed_x = -abs(ball_speed_x)  # Rebond vers la gauche
            elif ball_centerx > brick_centerx:
                ball_speed_x = abs(ball_speed_x)  # Rebond vers la droite

            if ball_centery < brick_centery:
                ball_speed_y = -abs(ball_speed_y)  # Rebond vers le haut
            elif ball_centery > brick_centery:
                ball_speed_y = abs(ball_speed_y)  # Rebond vers le bas

            break  # Arrêter dès qu'une collision est détectée

    return ball_speed_x, ball_speed_y, score

# Fonction principale pour démarrer le jeu
def start_game():
    global paddle_x, paddle_y, ball_x, ball_y, ball_speed_x, ball_speed_y, score, bricks

    # Boucle principale du jeu
    running = True
    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Déplacer la raquette
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width:
            paddle_x += paddle_speed

        # Mettre à jour la position de la balle
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Créer le rectangle de la balle pour la détection de collision
        ball_rect = pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, 2 * ball_radius, 2 * ball_radius)

        # Collision avec les bords de la fenêtre
        if ball_x - ball_radius <= 0 or ball_x + ball_radius >= screen_width:
            ball_speed_x = -ball_speed_x  # Inverser la direction horizontale
            pygame.mixer.Sound('assets/sounds/toc.mp3').play()
        if ball_y - ball_radius <= 0:
            ball_speed_y = -ball_speed_y  # Inverser la direction verticale
            pygame.mixer.Sound('assets/sounds/toc.mp3').play()

        # Collision avec la raquette (gestion améliorée)
        paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
        if ball_rect.colliderect(paddle_rect):
            pygame.mixer.Sound('assets/sounds/barre.mp3').play()
            # Calculer la position d'impact et changer la direction
            if ball_x < paddle_x or ball_x > paddle_x + paddle_width:
                ball_speed_x = -ball_speed_x  # Rebond horizontal
            if ball_y + ball_radius > paddle_y:
                ball_speed_y = -ball_speed_y  # Rebond vertical

        # Gestion des collisions avec les briques et mise à jour du score
        ball_speed_x, ball_speed_y, score = handle_collision_with_bricks(ball_rect, ball_speed_x, ball_speed_y, bricks, score)

        # Remplir l'écran avec une couleur unie
        screen.fill(background_color)

        # Dessiner la balle
        pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)

        # Dessiner la raquette
        pygame.draw.rect(screen, paddle_color, (paddle_x, paddle_y, paddle_width, paddle_height))

        # Dessiner les briques
        for brick in bricks:
            pygame.draw.rect(screen, brick_color, brick)

        # Afficher le score
        score_text = font.render(f"Score: {score}", True, text_color)
        screen.blit(score_text, (10, 10))

        # Mettre à jour l'affichage
        pygame.display.flip()

    # Quitter Pygame
    pygame.quit()
    sys.exit()

# Boucle d'accueil
show_start_screen()

# Attente de l'entrée de l'utilisateur pour démarrer le jeu
waiting_for_input = True
while waiting_for_input:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Quand l'utilisateur appuie sur espace, démarrer le jeu
                show_start_screen()  # Réafficher l'écran de démarrage
                waiting_for_input = False
                start_game()
