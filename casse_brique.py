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
paddle_width = 150
paddle_height = 10
paddle_x = (screen_width - paddle_width) // 2
paddle_y = screen_height - 30
paddle_speed = 2.5

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
    instructions_text = instructions_font.render("Appuyez sur espace pour commencer", True, text_color)
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

            # Vérifier si la collision est proche d'un angle
            if abs(ball_centerx - brick.left) < 5 or abs(ball_centerx - brick.right) < 5:
                ball_speed_x *= 1.1  # Augmenter légèrement la vitesse horizontale
            if abs(ball_centery - brick.top) < 5 or abs(ball_centery - brick.bottom) < 5:
                ball_speed_y *= 1.1  # Augmenter légèrement la vitesse verticale

            # Ajouter une légère randomisation à la direction
            import random
            ball_speed_x += random.uniform(-0.02, 0.02)
            ball_speed_y += random.uniform(-0.02, 0.02)

            # Calculer la nouvelle direction
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
# Fonction pour afficher l'écran de Game Over
def show_game_over_screen(final_score):
    screen.fill(background_color)
    game_over_font = pygame.font.Font('assets/fonts/SFAlienEncounters-Italic.ttf', 60)
    instructions_font = pygame.font.Font('assets/fonts/SFAlienEncountersSolid.ttf', 36)

    # Afficher "Game Over"
    game_over_text = game_over_font.render("Partie terminée", True, text_color)
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 4))
    screen.blit(game_over_text, game_over_rect)

    # Afficher le score final
    score_text = instructions_font.render(f"Score final : {final_score}", True, text_color)
    score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(score_text, score_rect)

    # Afficher les instructions pour rejouer ou quitter
    replay_text = instructions_font.render("Appuyez sur espace pour rejouer", True, text_color)
    replay_rect = replay_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    screen.blit(replay_text, replay_rect)

    quit_text = instructions_font.render("Appuyez sur Q pour quitter", True, text_color)
    quit_rect = quit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
    screen.blit(quit_text, quit_rect)

    pygame.display.flip()

    # Attendre l'entrée de l'utilisateur
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Rejouer
                    waiting_for_input = False
                    start_game()
                elif event.key == pygame.K_q:  # Quitter
                    pygame.quit()
                    sys.exit()
# Fonction pour afficher l'écran de fin de niveau
def show_level_complete_screen(current_level, score):
    screen.fill(background_color)
    level_complete_font = pygame.font.Font('assets/fonts/SFAlienEncounters-Italic.ttf', 60)
    instructions_font = pygame.font.Font('assets/fonts/SFAlienEncountersSolid.ttf', 36)

    # Afficher "Niveau Terminé"
    level_complete_text = level_complete_font.render(f"Niveau {current_level} Terminé !", True, text_color)
    level_complete_rect = level_complete_text.get_rect(center=(screen_width // 2, screen_height // 4))
    screen.blit(level_complete_text, level_complete_rect)

    # Afficher le score
    score_text = instructions_font.render(f"Score : {score}", True, text_color)
    score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(score_text, score_rect)

    # Afficher les instructions pour continuer
    next_level_text = instructions_font.render("Appuyez sur Espace pour continuer", True, text_color)
    next_level_rect = next_level_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    screen.blit(next_level_text, next_level_rect)

    pygame.display.flip()

    # Attendre l'entrée de l'utilisateur pour passer au niveau suivant
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Passer au niveau suivant
                    waiting_for_input = False


# Fonction pour générer un nouveau niveau
def generate_level(level):
    global ball_speed_x, ball_speed_y, bricks, brick_color

    # Augmenter la vitesse de la balle avec le niveau
    ball_speed_x = 0.25 + (level - 1) * 0.1
    ball_speed_y = 0.25 + (level - 1) * 0.1

    # Modifier les briques pour chaque niveau
    bricks = []
    num_rows = 5 + (level - 1)  # Ajouter des lignes de briques selon le niveau

    for row in range(num_rows):
        for col in range(num_columns):
            # Alterner les motifs selon le niveau
            if level == 1:
                brick_x = col * (brick_width + 10) + 35
                brick_y = row * (brick_height + 5) + 50
            elif level == 2:
                # Exemple de motif en quinconce
                brick_x = col * (brick_width + 10) + 35 + (row % 2) * 30
                brick_y = row * (brick_height + 5) + 50
            else:
                # Motifs supplémentaires pour les futurs niveaux
                brick_x = col * (brick_width + 10) + 35
                brick_y = row * (brick_height + 5) + 50

            bricks.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))

    # Changer les couleurs des briques selon le niveau
    if level == 2:
        brick_color = (255, 0, 0)  # Rouge
    elif level == 3:
        brick_color = (0, 0, 255)  # Bleu
    else:
        brick_color = (0, 255, 0)  # Vert par défaut


# Mise à jour de la fonction principale du jeu pour gérer plusieurs niveaux
def start_game():
    global paddle_x, paddle_y, ball_x, ball_y, ball_speed_x, ball_speed_y, score, bricks

    # Initialiser les variables
    current_level = 1
    paddle_x = (screen_width - paddle_width) // 2
    ball_x = screen_width // 2
    ball_y = screen_height // 2
    ball_speed_x = 0.25
    ball_speed_y = 0.25
    score = 0

    # Générer le premier niveau
    generate_level(current_level)

    running = True
    while running:
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
            ball_speed_x = -ball_speed_x
        if ball_y - ball_radius <= 0:
            ball_speed_y = -ball_speed_y

        # Vérifier si la balle touche le bas de l'écran (Game Over)
        if ball_y - ball_radius > screen_height:
            # pygame.mixer.Sound('assets/sounds/gameover.mp3').play()
            running = False
            show_game_over_screen(score)

        # Collision avec la raquette
        paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
        if ball_rect.colliderect(paddle_rect):
            ball_speed_y = -ball_speed_y

        # Gestion des collisions avec les briques et mise à jour du score
        ball_speed_x, ball_speed_y, score = handle_collision_with_bricks(ball_rect, ball_speed_x, ball_speed_y, bricks, score)

        # Vérifier si toutes les briques ont été détruites (niveau terminé)
        if not bricks:
            # pygame.mixer.Sound('assets/sounds/level_complete.mp3').play()
            show_level_complete_screen(current_level, score)
            current_level += 1  # Passer au niveau suivant
            generate_level(current_level)  # Générer le nouveau niveau

            # Réinitialiser la position de la balle et de la raquette
            ball_x = screen_width // 2
            ball_y = screen_height // 2
            paddle_x = (screen_width - paddle_width) // 2

        # Dessiner les éléments
        screen.fill(background_color)
        pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)
        pygame.draw.rect(screen, paddle_color, (paddle_x, paddle_y, paddle_width, paddle_height))
        for brick in bricks:
            pygame.draw.rect(screen, brick_color, brick)

        # Afficher le score et le niveau
        score_text = font.render(f"Score: {score}", True, text_color)
        level_text = font.render(f"Niveau: {current_level}", True, text_color)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (screen_width - 200, 10))

        # Mettre à jour l'affichage
        pygame.display.flip()

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
