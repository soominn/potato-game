import pygame
import random

class BackGround:
    def __init__(self, image):
        self.image = image
        
    def draw(self, surface):
        surface.blit(self.image, (0, 0))

class Bucket:
    def __init__(self, image, x, y, speed = 520, world_w = 600):
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.world_w = world_w

    def update(self, dt, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed * dt
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed * dt
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > self.world_w: self.rect.right = self.world_w

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Potato:
    def __init__(self, image, speed, x, y = -60):
        self.image = image
        self.rect = self.image.get_rect(midtop=(x, y))
        self.speed = speed

    def update(self, dt):
        self.rect.y += self.speed * dt

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_out(self, H) -> bool:
        return self.rect.top > H

class PotatoManager:
    def __init__(self, image, W, H, spawn_interval = 0.9, speed_range = (280, 600), spawn_count = 1, max_count = 100):
        self.image = image
        self.W, self.H = W, H
        self.spawn_interval = spawn_interval
        self.speed_range = speed_range
        self.spawn_count = spawn_count
        self.max_count = max_count
        self.timer = 0.0
        self.potatoes: list[Potato] = []

    def update(self, dt):
        dt = min(dt, 0.05)

        self.timer += dt
        while self.timer >= self.spawn_interval:
            self._spawn_batch(self.spawn_count)
            self.timer -= self.spawn_interval

        for p in self.potatoes:
            p.update(dt)

        missed = 0
        kept = []
        for p in self.potatoes:
            if p.is_out(self.H):
                missed += 1
            else:
                kept.append(p)
        self.potatoes = kept
        return missed
    
    def _spawn_batch(self, n):
        for _ in range(n):
            if len(self.potatoes) >= self.max_count:
                break
            self.spawn()

    def spawn(self):
        x = random.randint(25, self.W - 25)
        speed = random.uniform(*self.speed_range)
        self.potatoes.append(Potato(self.image, speed, x))

    def draw(self, surface):
        for p in self.potatoes:
            p.draw(surface)

    def clear(self):
        self.potatoes.clear()
        self.timer = 0.0

class CatchScene:
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.next_scene = None

        self.background_image = pygame.image.load("./images/background.png").convert()
        self.bucket_image = pygame.transform.scale(
            pygame.image.load("./images/bucket.png").convert_alpha(), (70, 48)
        )
        self.potato_image = pygame.transform.scale(
            pygame.image.load("./images/potato.png").convert_alpha(), (29, 24)
        )

        self.background = BackGround(self.background_image)
        self.bucket = Bucket(self.bucket_image, W / 2, H - 120, world_w=W)
        self.manager = PotatoManager(
            self.potato_image, W, H,
            spawn_interval=0.9, speed_range=(280, 600),
            spawn_count=1, max_count=100
        )

        try:
            self.font = pygame.font.Font("./fonts/PretendardVariable.ttf", 36)
            self.title_font = pygame.font.Font("./fonts/PretendardVariable.ttf", 80)
            self.hint_font = pygame.font.Font("./fonts/PretendardVariable.ttf", 28)
        except FileNotFoundError:
            self.font = pygame.font.SysFont(None, 36)
            self.title_font = pygame.font.SysFont(None, 80)
            self.hint_font = pygame.font.SysFont(None, 28)

        self.score = 0
        self.lives = 3
        self.missed_total = 0
        self.elapsed = 0.0
        self.game_over = False
        self._modal_shown = False
        self._ignore_next_dt = False
        self.hint = self.font.render("ESC: 메뉴로", True, (0, 0, 0))

        for _ in range(3):
            self.manager.spawn()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.next_scene = "menu"

    def update(self, dt):
        if self.game_over:
            return

        if self._ignore_next_dt:
            dt = 0.0
            self._ignore_next_dt = False

        keys = pygame.key.get_pressed()
        self.bucket.update(min(dt, 0.05), keys)

        added_missed = self.manager.update(dt)

        if self.lives - added_missed <= 0:
            self.manager.clear()
            self.lives = 0
            self.game_over = True
            return

        if added_missed:
            self.lives -= added_missed
            self.missed_total += added_missed

        caught, kept = 0, []
        for p in self.manager.potatoes:
            if p.rect.colliderect(self.bucket.rect):
                caught += 1
            else:
                kept.append(p)
        self.manager.potatoes = kept
        self.score += caught

        self.elapsed += dt

    def draw(self, screen):
        self.background.draw(screen)
        self.manager.draw(screen)
        self.bucket.draw(screen)

        hud_left, hud_top, gap = 12, 12, 28
        screen.blit(self.hint, (hud_left, hud_top))
        txt = self.font.render(f"점수: {self.score}", True, (20, 20, 20))
        screen.blit(txt, (hud_left, hud_top + gap))
        self._draw_lives(screen)

        if self.game_over and not self._modal_shown:
            self._modal_shown = True
            self._run_game_over_modal(screen)

    def _draw_lives(self, screen):
        x, y, r, pad = self.W - 20, 20, 10, 26
        for i in range(3):
            color = (220, 40, 60) if i < self.lives else (200, 200, 200)
            pygame.draw.circle(screen, color, (x - i * pad, y), r)
            pygame.draw.circle(screen, (0, 0, 0), (x - i * pad, y), r, 2)

    def _draw_text_center(self, surface, text, font, color, y):
        s = font.render(text, True, color)
        rect = s.get_rect(center=(self.W//2, y))
        surface.blit(s, rect)

    def _run_game_over_modal(self, screen):
        overlay = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        card_w, card_h = 540, 360
        card = pygame.Rect(0, 0, card_w, card_h)
        card.center = (self.W//2, self.H//2)
        pygame.draw.rect(screen, (245, 245, 245), card, border_radius=18)
        pygame.draw.rect(screen, (220, 220, 220), card, 2, border_radius=18)

        top = card.top
        self._draw_text_center(screen, "GAME OVER", self.title_font, (30, 30, 30), top + 70)
        self._draw_text_center(screen, f"받은 개수 : {self.score}", self.font, (50, 50, 50), top + 140)
        self._draw_text_center(screen, f"놓친 개수 : {self.missed_total}", self.font, (50, 50, 50), top + 180)
        self._draw_text_center(screen, f"플레이 시간 : {self.elapsed:.2f}초", self.font, (50, 50, 50), top + 220)
        self._draw_text_center(screen, "R: 재시작   |   ESC: 메뉴", self.hint_font, (90, 90, 90), top + 270)
        pygame.display.flip()

        clock = pygame.time.Clock()
        waiting = True
        while waiting:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); raise SystemExit
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_r:
                        self.reset()
                        self._ignore_next_dt = True
                        pygame.event.clear()
                        waiting = False
                    elif e.key == pygame.K_ESCAPE:
                        self.next_scene = "menu"
                        waiting = False
            clock.tick(60)

    def reset(self):
        self.score = 0
        self.lives = 3
        self.missed_total = 0
        self.elapsed = 0.0
        self.game_over = False
        self._modal_shown = False
        self._ignore_next_dt = False

        self.manager.clear()
        for _ in range(3):
            self.manager.spawn()

        self.bucket.rect.centerx = self.W // 2
        self.bucket.rect.centery = self.H - 80
