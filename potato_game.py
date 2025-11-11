import pygame, random, sys

# --- 기본 설정 ---
pygame.init()
W, H = 600, 800
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("감자 피하기")
clock = pygame.time.Clock()
dt = 0.0

# --- 이미지 로드 ---
background_image = pygame.image.load("./images/background.png").convert()
player_image = pygame.transform.scale(pygame.image.load("./images/player.png").convert_alpha(), (70, 70))
potato_image = pygame.transform.scale(pygame.image.load("./images/poisonous_potato.webp").convert_alpha(), (50, 50))

# --- BackGround 클래스 ---
class BackGround:
    def __init__(self, image):
        self.image = image

    def draw(self, surface):
        surface.blit(self.image, (0, 0))

# --- Player ---
class Player:
    def __init__(self, image, x, y, speed=500):
        self.base_image = image
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.facing_right = True

    def update(self, dt, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed * dt
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed * dt
            self.facing_right = True

        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > W: self.rect.right = W

        # 오른쪽 이미지만 사용해서 flip으로 방향 전환
        self.image = pygame.transform.flip(self.base_image, not self.facing_right, False)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# --- 감자 ---
class Potato:
    def __init__(self, image, speed, x, y=-60):
        self.image = image
        self.rect = self.image.get_rect(midtop=(x, y))
        self.speed = speed

    def update(self, dt):
        self.rect.y += self.speed * dt

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_out(self):
        return self.rect.top > H

# --- 감자 매니저 ---
class PotatoManager:
    def __init__(self, image, spawn_interval=1.0, speed_range=(240, 480), spawn_count=1):
        self.image = image
        self.spawn_interval = spawn_interval
        self.speed_range = speed_range
        self.spawn_count = spawn_count
        self.timer = 0.0
        self.potatoes = []

    def update(self, dt):
        self.timer += dt
        while self.timer >= self.spawn_interval:
            for _ in range(self.spawn_count):
                self.spawn()
            self.timer -= self.spawn_interval

        for p in self.potatoes:
            p.update(dt)
        self.potatoes = [p for p in self.potatoes if not p.is_out()]

    def spawn(self):
        x = random.randint(25, W - 25)
        speed = random.uniform(*self.speed_range)
        self.potatoes.append(Potato(self.image, speed, x))

    def draw(self, surface):
        for p in self.potatoes:
            p.draw(surface)

    def collide_with(self, rect):
        return any(p.rect.colliderect(rect) for p in self.potatoes)

# --- 객체 생성 ---
background = BackGround(background_image)
player = Player(player_image, W / 2, H / 2 + 300)
manager = PotatoManager(potato_image, spawn_interval=0.7, speed_range=(320, 700), spawn_count=3)

# --- 메인 루프 ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

    player.update(dt, keys)
    manager.update(dt)

    if manager.collide_with(player.rect):
        running = False

    background.draw(screen)
    manager.draw(screen)
    player.draw(screen)

    pygame.display.flip()
    dt = clock.tick(60) / 1000.0

pygame.quit()
sys.exit()