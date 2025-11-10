import pygame

pygame.init()
screen = pygame.display.set_mode((600, 800))
pygame.display.set_caption("감자 피하기 게임")
clock = pygame.time.Clock()
running = True
dt = 0

# 이미지 가져오기
background_image = pygame.image.load("./images/background.png").convert()
potato_image = pygame.transform.scale(pygame.image.load("./images/potato.png").convert_alpha(), (50, 50))
player_image = pygame.transform.scale(pygame.image.load("./images/right_person.png").convert_alpha(), (50, 50))

class Player:
    def __init__(self, image, x, y, speed=300):
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.flipped = False

    def update(self, dt, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= 300 * dt
            self.flipped = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += 300 * dt
            self.flipped = False

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen.get_width():
            self.rect.right = screen.get_width()

        current_image = pygame.transform.flip(player_image, self.flipped, False)
        self.image = current_image

    def draw(self, surface):
        surface.blit(self.image, self.rect)

player = Player(player_image, screen.get_width() / 2, screen.get_height() / 2 + 165)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    player.update(dt, keys)

    screen.blit(background_image, (0, 0))
    player.draw(screen)
    screen.blit(potato_image, (screen.get_width() / 2, -50))

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()