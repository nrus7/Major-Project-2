import pygame
import sys

import pygame
import sys

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Soldier Fight")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (50, 100, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Player settings
PLAYER_WIDTH, PLAYER_HEIGHT = 60, 90
GROUND_LEVEL = HEIGHT - PLAYER_HEIGHT - 30
VEL = 5
JUMP_POWER = 15
GRAVITY = 1
MAX_HEALTH = 100


# Player class
class Soldier:
    def __init__(self, x, color, controls):
        self.rect = pygame.Rect(x, GROUND_LEVEL, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.color = color
        self.health = MAX_HEALTH
        self.vel_y = 0
        self.is_jumping = False
        self.controls = controls
        self.facing = 1 if x < WIDTH // 2 else -1
        self.attacking = False
        self.attack_cooldown = 0

    def handle_movement(self, keys):
        # Horizontal movement
        if keys[self.controls['left']] and self.rect.left > 0:
            self.rect.x -= VEL
            self.facing = -1
        if keys[self.controls['right']] and self.rect.right < WIDTH:
            self.rect.x += VEL
            self.facing = 1

        # Jump
        if not self.is_jumping and keys[self.controls['jump']]:
            self.is_jumping = True
            self.vel_y = -JUMP_POWER

    def apply_gravity(self):
        if self.is_jumping:
            self.vel_y += GRAVITY
            self.rect.y += self.vel_y

            if self.rect.y >= GROUND_LEVEL:
                self.rect.y = GROUND_LEVEL
                self.vel_y = 0
                self.is_jumping = False

    def attack(self):
        if self.attack_cooldown == 0:
            self.attacking = True
            self.attack_cooldown = 25  # cooldown (frames)

    def update_cooldown(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        else:
            self.attacking = False

    def draw(self, surface):
        # Draw player
        pygame.draw.rect(surface, self.color, self.rect)

        # Draw attack hitbox if attacking
        if self.attacking:
            attack_width = 30
            attack_height = 20
            if self.facing == 1:
                attack_rect = pygame.Rect(self.rect.right, self.rect.centery - 10, attack_width, attack_height)
            else:
                attack_rect = pygame.Rect(self.rect.left - attack_width, self.rect.centery - 10, attack_width, attack_height)
            pygame.draw.rect(surface, GREEN, attack_rect)
            return attack_rect
        return None

    def check_attack_hit(self, other, attack_rect):
        if attack_rect and attack_rect.colliderect(other.rect):
            other.health -= 5
            if other.health < 0:
                other.health = 0


def draw_health_bar(x, y, health, color):
    # Draw border
    pygame.draw.rect(screen, BLACK, (x - 2, y - 2, 204, 24))
    # Draw fill
    pygame.draw.rect(screen, color, (x, y, 2 * health, 20))


# Controls for both players
controls1 = {'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w, 'attack': pygame.K_SPACE}
controls2 = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP, 'attack': pygame.K_RETURN}

# Create players
player1 = Soldier(100, BLUE, controls1)
player2 = Soldier(700, RED, controls2)


def main():
    run = True
    while run:
        clock.tick(FPS)
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # Player actions
        player1.handle_movement(keys)
        player2.handle_movement(keys)
        player1.apply_gravity()
        player2.apply_gravity()

        # Attacks
        if keys[player1.controls['attack']]:
            player1.attack()
        if keys[player2.controls['attack']]:
            player2.attack()

        # Update cooldowns
        player1.update_cooldown()
        player2.update_cooldown()

        # Draw players and check for hits
        attack_rect1 = player1.draw(screen)
        attack_rect2 = player2.draw(screen)
        player1.check_attack_hit(player2, attack_rect1)
        player2.check_attack_hit(player1, attack_rect2)

        # Draw health bars
        draw_health_bar(50, 20, player1.health, BLUE)
        draw_health_bar(WIDTH - 250, 20, player2.health, RED)

        # Game over
        if player1.health <= 0 or player2.health <= 0:
            font = pygame.font.SysFont(None, 60)
            winner = "Red Wins!" if player1.health <= 0 else "Blue Wins!"
            text = font.render(winner, True, BLACK)
            screen.blit(text, (WIDTH // 2 - 120, HEIGHT // 2 - 30))
            pygame.display.flip()
            pygame.time.delay(2500)
            return

        pygame.display.flip()


if __name__ == "__main__":
    main()
